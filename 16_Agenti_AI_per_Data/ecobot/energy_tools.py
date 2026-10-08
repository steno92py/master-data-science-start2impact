"""Calcoli EcoBot: energia oraria in kWh, timestamp locali Europe/Rome.

I valori mancanti restano sconosciuti: mai convertiti implicitamente in zero.
Il confronto fra azienda e famiglia è uno scenario tecnico, non una bolletta CER.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd

TZ = "Europe/Rome"
COLUMNS = {"production": "kwh_produced", "consumption": "kwh_consumed"}


def local_timestamp(value):
    timestamp = pd.Timestamp(value)
    if pd.isna(timestamp):
        raise ValueError("Data non valida.")
    try:
        return timestamp.tz_localize(TZ) if timestamp.tzinfo is None else timestamp.tz_convert(TZ)
    except Exception as exc:
        raise ValueError("Data ambigua o inesistente al cambio dell'ora: specifica l'offset.") from exc


def load_and_clean(raw: bytes, kind: str):
    """Carica un CSV orario; scarta timestamp invalidi e segnala le correzioni."""
    if kind not in COLUMNS:
        raise ValueError("Tipo di dataset non riconosciuto.")
    if len(raw) > 20_000_000:
        raise ValueError("Il CSV supera 20 MB.")
    try:
        text = raw.decode("utf-8-sig")
        header = next(csv.reader(io.StringIO(text)))
        if len(header) != len(set(header)) or any(not h.strip() for h in header):
            raise ValueError("Intestazioni vuote o duplicate.")
        df = pd.read_csv(io.StringIO(text))
    except (UnicodeError, pd.errors.ParserError, pd.errors.EmptyDataError, StopIteration) as exc:
        raise ValueError("CSV UTF-8 con separatore virgola non leggibile.") from exc
    col = COLUMNS[kind]
    if not {"timestamp", col}.issubset(df.columns):
        raise ValueError(f"Colonne richieste: timestamp, {col}. Unità attesa: kWh per ora.")
    if not 1 <= len(df) <= 100_000 or len(df.columns) > 100:
        raise ValueError("Sono ammesse da 1 a 100.000 righe e al massimo 100 colonne.")
    report = {"input_rows": len(df), "sha256": hashlib.sha256(raw).hexdigest(),
              "ignored_columns": [str(c) for c in df.columns if c not in {"timestamp", col}],
              "unit": "kWh per intervallo orario", "timezone": TZ}
    times = []
    rounded_timestamps = 0
    for value in df["timestamp"]:
        try:
            if not isinstance(value, str):
                raise ValueError("Timestamp non testuale.")
            # Prima UTC per gestire anche il cambio dell'ora senza perdere l'offset.
            original = local_timestamp(value).tz_convert("UTC")
            rounded = original.floor("h")
            rounded_timestamps += int(original != rounded)
            times.append(rounded.tz_convert(TZ))
        except (ValueError, TypeError, OverflowError):
            times.append(pd.NaT)
    values = pd.to_numeric(df[col], errors="coerce").astype(float)
    report.update(missing_or_non_numeric=int(values.isna().sum()),
                  negative_values=int((values < 0).sum()),
                  infinite_values=int(np.isinf(values).sum()),
                  invalid_timestamps=int(pd.isna(times).sum()),
                  rounded_timestamps=rounded_timestamps)
    values = values.where(np.isfinite(values) & (values >= 0))
    clean = pd.DataFrame({"timestamp": times, col: values}).dropna(subset=["timestamp"])
    if clean.empty:
        raise ValueError("Nessun timestamp valido nel CSV.")
    report["duplicate_hours"] = int(clean.duplicated("timestamp").sum())
    # Duplicati coerenti: una sola misura. Conflitti: dato sconosciuto, non media inventata.
    grouped = clean.groupby("timestamp")[col]
    conflicts = grouped.nunique(dropna=True) > 1
    series = grouped.first().mask(conflicts).sort_index()
    report["conflicting_hours"] = int(conflicts.sum())
    expected = int((series.index[-1] - series.index[0]).total_seconds() / 3600) + 1
    if expected > 100_000:
        raise ValueError("Intervallo temporale troppo ampio: massimo 100.000 ore.")
    grid = pd.date_range(series.index[0], series.index[-1], freq="h")
    report["missing_intervals"] = len(grid) - len(series)
    series = series.reindex(grid)
    report.update(expected_hours=len(series), valid_hours=int(series.notna().sum()),
                  unknown_hours=int(series.isna().sum()),
                  start_inclusive=series.index[0].isoformat(),
                  end_exclusive=(series.index[-1] + pd.Timedelta(hours=1)).isoformat(),
                  policy="Timestamp ricondotti all'ora; negativi, infiniti e conflitti resi NaN; nessuna imputazione.")
    series.index.name = "timestamp"
    return series.rename(col), report


def finite(value):
    return None if pd.isna(value) or not np.isfinite(value) else float(value)


class EnergyTools:
    def __init__(self, production: bytes, consumption: bytes, output_dir: str | Path = "grafici"):
        prod, prod_report = load_and_clean(production, "production")
        cons, cons_report = load_and_clean(consumption, "consumption")
        self.frame = pd.concat([prod, cons], axis=1).sort_index()
        if (self.frame.index[-1] - self.frame.index[0]).total_seconds() / 3600 >= 100_000:
            raise ValueError("I due CSV coprono un intervallo complessivo superiore a 100.000 ore.")
        # Anche le ore assenti in ENTRAMBI i file devono comparire nell'export.
        grid = pd.date_range(self.frame.index[0], self.frame.index[-1], freq="h", name="timestamp")
        self.frame = self.frame.reindex(grid)
        self.reports = {"production": prod_report, "consumption": cons_report}
        self.fingerprint = hashlib.sha256(production + b"\0" + consumption).hexdigest()
        self.output_dir = Path(output_dir)

    def quality(self):
        return {"datasets": self.reports, "fingerprint": self.fingerprint,
                "available_start_inclusive": self.frame.index[0].isoformat(),
                "available_end_exclusive": (self.frame.index[-1] + pd.Timedelta(hours=1)).isoformat(),
                "full_dataset_arguments": {"start": None, "end": None, "hour_start": 0, "hour_end": 24},
                "interval_semantics": "Ogni timestamp segna l'inizio di un'ora. L'ultima misura è inclusa fino a end_exclusive. Per tutto il dataset usa full_dataset_arguments, anche nei grafici mensili.",
                "limitations": "Dati sintetici. Produzione aziendale e consumo familiare; nessuna tariffa, batteria o quota CER disponibile. Anomalie compatibili con errori sensore, non diagnosi certa di guasto."}

    def window(self, start=None, end=None, hour_start=0, hour_end=24):
        if not (isinstance(hour_start, int) and isinstance(hour_end, int) and 0 <= hour_start < hour_end <= 24):
            raise ValueError("Fascia oraria richiesta: 0 <= hour_start < hour_end <= 24.")
        low = local_timestamp(start) if start else self.frame.index[0]
        high = local_timestamp(end) if end else self.frame.index[-1] + pd.Timedelta(hours=1)
        if low >= high:
            raise ValueError("La data iniziale deve precedere la finale (esclusa).")
        if any((t.minute, t.second, t.microsecond, t.nanosecond) != (0, 0, 0, 0) for t in (low, high)):
            raise ValueError("Usa estremi all'ora esatta: i dati sono orari.")
        hours = int((high - low).total_seconds() / 3600)
        if hours > 100_000:
            raise ValueError("Periodo troppo ampio: massimo 100.000 ore.")
        grid = pd.date_range(low, high, freq="h", inclusive="left")
        grid = grid[(grid.hour >= hour_start) & (grid.hour < hour_end)]
        data = self.frame.reindex(grid)
        return data, {"start_inclusive": low.isoformat(), "end_exclusive": high.isoformat(),
                      "hour_start": hour_start, "hour_end": hour_end, "expected_hours": len(data)}

    def total(self, kind, start=None, end=None, hour_start=0, hour_end=24):
        if kind not in COLUMNS:
            raise ValueError("Scegli production o consumption.")
        frame, period = self.window(start, end, hour_start, hour_end)
        values = frame[COLUMNS[kind]]
        return {**period, "kind": kind, "total_kwh_observed": finite(values.sum(min_count=1)),
                "valid_hours": int(values.notna().sum()), "unknown_hours": int(values.isna().sum()),
                "complete": bool(len(values) and values.notna().all()), "imputation": False}

    def production_total(self, start=None, end=None, hour_start=0, hour_end=24):
        return self.total("production", start, end, hour_start, hour_end)

    def consumption_total(self, start=None, end=None, hour_start=0, hour_end=24):
        return self.total("consumption", start, end, hour_start, hour_end)

    def compare_energy(self, start=None, end=None, hour_start=0, hour_end=24):
        frame, period = self.window(start, end, hour_start, hour_end)
        paired = frame.dropna()
        prod, cons = paired["kwh_produced"], paired["kwh_consumed"]
        hourly = paired.groupby(paired.index.hour).mean()
        surplus = (hourly.kwh_produced - hourly.kwh_consumed).clip(lower=0)
        best = [int(h) for h in surplus[surplus > 0].nlargest(3).index]
        correlation = finite(prod.corr(cons)) if len(paired) >= 3 and prod.nunique() > 1 and cons.nunique() > 1 else None
        return {**period, "paired_hours": len(paired), "unknown_pair_hours": len(frame) - len(paired),
                "production_kwh_paired": finite(prod.sum(min_count=1)),
                "consumption_kwh_paired": finite(cons.sum(min_count=1)),
                "potential_coincidence_kwh": finite(pd.Series(np.minimum(prod, cons)).sum(min_count=1)),
                "potential_surplus_kwh": finite((prod - cons).clip(lower=0).sum(min_count=1)),
                "potential_shortfall_kwh": finite((cons - prod).clip(lower=0).sum(min_count=1)),
                "hours_with_highest_mean_surplus": best,
                "peak_mean_consumption_hour": int(hourly.kwh_consumed.idxmax()) if len(hourly) else None,
                "pearson": correlation,
                "advice": "Se compatibile con le abitudini, valuta lo spostamento dei carichi flessibili nelle ore con surplus medio positivo. Verifica tariffe e disponibilità effettiva nella CER prima di stimare risparmi.",
                "limits": "Confronto sulle sole coppie valide. Coincidenza teorica azienda/famiglia, non autoconsumo misurato o energia fatturata. Nessuna stima in euro o indicazione di acquisto batterie. Correlazione non implica causalità."}

    def trend(self, frequency="day", start=None, end=None, hour_start=0, hour_end=24):
        if frequency not in {"day", "month", "hour_of_day"}:
            raise ValueError("Frequenza ammessa: day, month, hour_of_day.")
        frame, period = self.window(start, end, hour_start, hour_end)
        group = frame.index.hour if frequency == "hour_of_day" else frame.index.strftime("%Y-%m" if frequency == "month" else "%Y-%m-%d")
        rows = []
        for label, subset in frame.groupby(group):
            row = {"period": str(label), "expected_hours": len(subset)}
            if frequency != "hour_of_day":
                boundary = local_timestamp(str(label))
                following = boundary + (pd.DateOffset(months=1) if frequency == "month" else pd.DateOffset(days=1))
                calendar_hours = int((following - boundary).total_seconds() / 3600)
                row["calendar_hours"] = calendar_hours
                row["covers_full_calendar_period"] = len(subset) == calendar_hours
            for col in COLUMNS.values():
                values = subset[col]
                row[col] = finite(values.mean() if frequency == "hour_of_day" else values.sum(min_count=1))
                row[col + "_valid_hours"] = int(values.notna().sum())
            rows.append(row)
        shown = rows[-90:]
        note = "NaN esclusi, nessuna imputazione. I totali possono essere parziali: controllare le ore valide."
        if frequency != "hour_of_day" and any(not row["covers_full_calendar_period"] for row in shown):
            note += " Alcuni giorni/mesi sono coperti solo in parte dall'intervallo o dalla fascia selezionata: ore attese si riferisce alla selezione, non al periodo di calendario completo."
        if len(rows) > 90:
            note += f" Mostrati solo gli ultimi 90 di {len(rows)} periodi: da {shown[0]['period']} a {shown[-1]['period']}. Restringi l'intervallo per vedere i periodi precedenti."
        return {**period, "frequency": frequency, "operation": "mean" if frequency == "hour_of_day" else "sum",
                "data": shown, "total_periods": len(rows), "truncated": len(rows) > 90,
                "note": note}

    def energy_chart(self, frequency="day", start=None, end=None, hour_start=0, hour_end=24):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        result = self.trend(frequency, start, end, hour_start, hour_end)
        rows = result["data"]
        if not rows:
            raise ValueError("Nessun intervallo da rappresentare.")
        fig = Figure(figsize=(10, 4.5), layout="constrained")
        FigureCanvasAgg(fig)
        ax = fig.subplots()
        for col, label, color in [("kwh_produced", "Produzione azienda", "#158269"), ("kwh_consumed", "Consumo famiglia", "#d57839")]:
            ax.plot([r["period"] for r in rows], [np.nan if r[col] is None else r[col] for r in rows], label=label, color=color, marker=".")
        ax.set(title="EcoBot · " + {"day":"Energia giornaliera", "month":"Energia mensile", "hour_of_day":"Profilo medio per ora"}[frequency],
               ylabel="kWh medi per intervallo" if frequency == "hour_of_day" else "kWh osservati", xlabel="Ora locale" if frequency == "hour_of_day" else "Periodo")
        ax.legend(); ax.grid(alpha=.18)
        step = max(1, len(rows) // 8)
        ax.set_xticks(range(0, len(rows), step), [r["period"] for r in rows][::step], rotation=30, ha="right")
        footer = "Europe/Rome · dati demo / CSV caricati · totali parziali se mancano misure"
        if any(not row.get("covers_full_calendar_period", True) for row in rows):
            footer += "\nGiorni/mesi ai margini o filtrati possono essere incompleti: confrontare la copertura."
        if result["truncated"]:
            footer += f"\nSolo gli ultimi 90 di {result['total_periods']} periodi; restringere l'intervallo per i precedenti."
        fig.supxlabel(footer, fontsize=8)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        ident = hashlib.sha256((self.fingerprint + json.dumps(result, sort_keys=True)).encode()).hexdigest()[:20]
        path = self.output_dir / f"energia_{ident}.png"
        fig.savefig(path, dpi=140)
        return {**result, "chart_path": str(path.resolve())}

    def execute(self, name, arguments):
        allowed = {"quality", "production_total", "consumption_total", "compare_energy", "trend", "energy_chart"}
        if name not in allowed:
            raise ValueError("Strumento non consentito.")
        return getattr(self, name)(**arguments)
