"""streamlit run app.py --server.address 127.0.0.1"""
import json
import os
from dataclasses import asdict
from pathlib import Path

from dotenv import load_dotenv
import pandas as pd
import streamlit as st

from energy_tools import EnergyTools
from ecobot_agent import ask, make_model
from report import make_report

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env", override=False)
st.set_page_config(page_title="EcoBot · EcoGrid", page_icon="🌱", layout="wide")
st.title("EcoBot")
st.caption("EcoGrid Solutions · Stefano Nocco · Capire l’energia, una domanda alla volta")
with st.sidebar:
    st.header("I due dataset")
    production_upload = st.file_uploader("Produzione solare aziendale", type="csv", key="production")
    consumption_upload = st.file_uploader("Consumo domestico", type="csv", key="consumption")
    st.caption("CSV orari: timestamp e kwh_produced / kwh_consumed. Date locali Europe/Rome, energia in kWh.")
    st.divider()
    st.header("Chat AI")
    key = st.text_input("API key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    model_name = st.text_input("Modello", value=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    consent = st.checkbox("Invia a OpenAI domande, contesto e risultati dei calcoli", value=False)
    st.caption("Analisi locali senza chiave; chat API a consumo. La chiave non entra nei report.")
if bool(production_upload) != bool(consumption_upload):
    st.warning("Carica entrambi i CSV per confrontare una coppia coerente di dati.")
    st.stop()
try:
    prod = production_upload.getvalue() if production_upload else (ROOT / "data/solar_production_raw.csv").read_bytes()
    cons = consumption_upload.getvalue() if consumption_upload else (ROOT / "data/household_consumption.csv").read_bytes()
    data = EnergyTools(prod, cons, ROOT / "grafici")
except (ValueError, OSError) as exc:
    st.error(str(exc)); st.stop()
if st.session_state.get("fingerprint") != data.fingerprint:
    st.session_state.update(fingerprint=data.fingerprint, turns=[], chart_paths=[])
if not production_upload:
    st.info("Demo sintetica generata con lo script della consegna: un’azienda produttrice e una famiglia. Le anomalie dei sensori sono intenzionali.")
quality = data.quality()
st.caption(f"Periodo disponibile: {quality['available_start_inclusive']} — {quality['available_end_exclusive']} (fine esclusa) · Europe/Rome")
production = data.production_total(); consumption = data.consumption_total()
cols = st.columns(3)
for target, label, result in [(cols[0], "Produzione osservata", production), (cols[1], "Consumo osservato", consumption)]:
    value = result["total_kwh_observed"]
    target.metric(label, "N/D" if value is None else f"{value:,.2f} kWh")
    target.caption(f"{result['valid_hours']}/{result['expected_hours']} ore valide")
cols[2].metric("Misure orarie mancanti", production["unknown_hours"] + consumption["unknown_hours"])
cols[2].caption("Somma sui due sensori nel periodo comune di analisi; nessuna imputazione")
overview, chat, export = st.tabs(["Dati e analisi", "Chat con EcoBot", "Report e prove"])
with overview:
    st.subheader("Controlla prima la qualità")
    with st.expander("Anomalie e regole di pulizia"):
        st.json(quality)
    st.dataframe(data.frame.head(30), width="stretch")
    st.download_button("Scarica dati puliti", data.frame.to_csv().encode(), "energia_pulita.csv", "text/csv")
    frequency = st.selectbox("Raggruppamento", ["day", "month", "hour_of_day"], format_func=lambda v: {"day":"Giorno", "month":"Mese", "hour_of_day":"Ora del giorno (media)"}[v])
    chart = data.energy_chart(frequency)
    st.image(chart["chart_path"], width="stretch")
    st.caption(chart["note"])
    st.download_button("Scarica grafico PNG", Path(chart["chart_path"]).read_bytes(), "ecobot_energia.png", "image/png")
    if chart["chart_path"] not in st.session_state.chart_paths:
        st.session_state.chart_paths.append(chart["chart_path"])
    with st.expander("Dati del grafico e copertura"):
        st.dataframe(pd.DataFrame(chart["data"]), width="stretch")
    comparison = data.compare_energy()
    st.subheader("Indicazioni dai dati")
    hours = comparison["hours_with_highest_mean_surplus"]
    st.write("Ore con maggiore surplus medio osservato: " + (", ".join(f"{h:02d}:00" for h in hours) if hours else "nessuna disponibile"))
    st.write(comparison["advice"])
    st.caption(comparison["limits"])
with chat:
    st.write("Chiedi, per esempio: «Ci sono anomalie nei sensori?» oppure «Mostra il confronto mensile con un grafico».")
    if st.button("Nuova conversazione"):
        st.session_state.turns = []
        st.session_state.chart_paths = [chart["chart_path"]]
        st.rerun()
    for turn in st.session_state.turns:
        with st.chat_message("user"):
            st.write(turn["question"])
        with st.chat_message("assistant"):
            st.markdown(turn["answer"])
            for step in turn.get("trace", []):
                path = step["result"].get("chart_path")
                if path:
                    st.image(path, width="stretch")
            with st.expander("Operazioni, risultati e consumo API"):
                st.json({k:v for k,v in turn.items() if k not in {"question", "answer"}})
    prompt = st.chat_input("Che cosa vuoi sapere sui tuoi consumi?", disabled=not (key and consent), max_chars=4000)
    if not key or not consent:
        st.info("Per attivare la chat configura la chiave e il consenso nella barra laterale.")
    if prompt:
        with st.spinner("EcoBot controlla i dati e sceglie i calcoli…"):
            try:
                answer = ask(make_model(key, model_name), prompt, data, st.session_state.turns)
                record = asdict(answer)
                record["answer"] = record.pop("text")
                record.update(question=prompt, model=model_name, validation="Sessione API reale; correttezza da verificare sulle evidenze")
            except Exception:
                record = {"question":prompt, "answer":"La chiamata API non è riuscita. Verifica connessione, chiave, credito e modello. Nessuna risposta AI disponibile.", "trace":[], "completed":False, "validation":"Errore API; consumo eventualmente addebitato non disponibile"}
        st.session_state.turns.append(record)
        for step in record.get("trace", []):
            chart_path = step["result"].get("chart_path")
            if chart_path and chart_path not in st.session_state.chart_paths:
                st.session_state.chart_paths.append(chart_path)
        st.rerun()
with export:
    st.write(f"{len(st.session_state.turns)} scambi in questa sessione")
    st.download_button("Scarica report HTML", make_report(data, st.session_state.turns, st.session_state.chart_paths), "report_ecobot.html", "text/html")
    evidence = {"dataset": data.fingerprint, "quality": quality, "turns": st.session_state.turns}
    st.download_button("Scarica evidenze JSON", json.dumps(evidence, ensure_ascii=False, indent=2), "evidenze_ecobot.json", "application/json")
    st.caption("Le evidenze distinguono richieste reali e calcoli locali. Una risposta del modello non certifica da sola la correttezza.")
