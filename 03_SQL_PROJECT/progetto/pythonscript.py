# -*- coding: utf-8 -*-
# Grafici per le VIEW/SELECT di scriptSQL.txt (nessuna invenzione, solo logica SQL).
# File attesi: 
#   /mnt/data/world-data-2023.csv
#   /mnt/data/global-data-on-sustainable-energy.csv
#   /mnt/data/Global Missing Migrants Dataset.csv

import pandas as pd, numpy as np, matplotlib.pyplot as plt, os

# ---------- Helper coerenti con lo SQL ----------
def read_csv_any(path):
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1")

def to_num_strip(x, rm_chars=(',', '%', '$')):
    if pd.isna(x): return np.nan
    s = str(x)
    for ch in rm_chars: s = s.replace(ch, '')
    s = s.strip()
    if s == '' or s.lower() == 'nan': return np.nan
    try: return float(s)
    except: return np.nan

outdir = "/mnt/data"
os.makedirs(outdir, exist_ok=True)

# ---------- Load ----------
dfw_raw = read_csv_any("/mnt/data/world-data-2023.csv")
dfe_raw = read_csv_any("/mnt/data/global-data-on-sustainable-energy.csv")
dfm_raw = read_csv_any("/mnt/data/Global Missing Migrants Dataset.csv")

# ---------- VIEW: world_2023 (replica selezione/cast SQL) ----------
dfw = pd.DataFrame({
    "country_key": dfw_raw["Country"].astype(str).str.strip().str.lower(),
    "Country": dfw_raw["Country"].astype(str).str.strip(),
    "population": dfw_raw["Population"].apply(lambda x: to_num_strip(x, rm_chars=(',',))),
    "gdp_usd": dfw_raw["GDP"].apply(lambda x: to_num_strip(x, rm_chars=(',',))),
    "life_expectancy": pd.to_numeric(dfw_raw["Life expectancy"], errors="coerce"),
    "physicians_per_thousand": pd.to_numeric(dfw_raw["Physicians per thousand"], errors="coerce"),
    "gross_primary_enroll_pct": dfw_raw["Gross primary education enrollment (%)"].apply(lambda x: to_num_strip(x, rm_chars=('%',))),
    "gross_tertiary_enroll_pct": dfw_raw["Gross tertiary education enrollment (%)"].apply(lambda x: to_num_strip(x, rm_chars=('%',))),
    "oop_health_exp_pct": dfw_raw["Out of pocket health expenditure"].apply(lambda x: to_num_strip(x, rm_chars=('%',))),
    "co2_emissions_mt": dfw_raw["Co2-Emissions"].apply(lambda x: to_num_strip(x, rm_chars=(',',))),
    "unemployment_rate_pct": pd.to_numeric(dfw_raw["Unemployment rate"], errors="coerce"),
    "urban_population": dfw_raw["Urban_population"].apply(lambda x: to_num_strip(x, rm_chars=(',',)))
})

# ---------- VIEW: energy (replica selezione/cast SQL) ----------
rename_map = {
    "Entity": "entity",
    "Year": "year",
    "Access to electricity (% of population)": "access_electricity_pct",
    "Access to clean fuels for cooking": "clean_cooking_pct",
    "Renewable-electricity-generating-capacity-per-capita": "ren_capacity_per_capita",
    "Renewable energy share in the total final energy consumption (%)": "ren_share_tfec_pct",
    "Electricity from fossil fuels (TWh)": "elec_fossil_twh",
    "Electricity from nuclear (TWh)": "elec_nuclear_twh",
    "Electricity from renewables (TWh)": "elec_renewables_twh",
    "Low-carbon electricity (% electricity)": "low_carbon_elec_pct",
    "Primary energy consumption per capita (kWh/person)": "primary_energy_pc_kwh",
    "Energy intensity level of primary energy (MJ/$2017 PPP GDP)": "energy_intensity_mj_per_ppp",
    "Value_co2_emissions_kt_by_country": "co2_kt",
    "gdp_per_capita": "gdp_per_capita",
}
dfe = dfe_raw.rename(columns=rename_map).copy()
dfe["country_key"] = dfe["entity"].astype(str).str.strip().str.lower()
for c in ["year","access_electricity_pct","clean_cooking_pct","ren_capacity_per_capita","ren_share_tfec_pct",
          "elec_fossil_twh","elec_nuclear_twh","elec_renewables_twh","low_carbon_elec_pct",
          "primary_energy_pc_kwh","energy_intensity_mj_per_ppp","co2_kt","gdp_per_capita"]:
    dfe[c] = pd.to_numeric(dfe[c], errors="coerce")

# ---------- VIEW: missing_migrants_region_year (replica SQL) ----------
dfm = dfm_raw.copy()
dfm["year"] = pd.to_numeric(dfm["Incident year"], errors="coerce")
dfm["dead_missing"] = pd.to_numeric(dfm["Total Number of Dead and Missing"], errors="coerce")
mm_view = (dfm.dropna(subset=["year","dead_missing","Region of Incident"])
             .groupby(["Region of Incident","year"], as_index=False)["dead_missing"].sum()
             .rename(columns={"Region of Incident":"region_of_incident"}))

# ============================================================
# GRAFICI per VIEW world_2023 (W1–W4)
# ============================================================

# W1 — (VIEW world_2023) Top-15 GDP
w1 = dfw.dropna(subset=["gdp_usd"]).sort_values("gdp_usd", ascending=False).head(15)
w1[["Country","gdp_usd"]].to_csv(f"{outdir}/W1_world_top15_gdp.csv", index=False)
plt.figure(figsize=(11,6)); plt.bar(w1["Country"], w1["gdp_usd"]); plt.xticks(rotation=45, ha='right')
plt.ylabel("GDP (USD, totale)"); plt.title("VIEW world_2023 — W1: Top-15 GDP")
plt.tight_layout(); plt.savefig(f"{outdir}/W1_world_top15_gdp.png", dpi=150); plt.close()

# W2 — (VIEW world_2023) Life expectancy vs Physicians/1000
w2 = dfw.dropna(subset=["life_expectancy","physicians_per_thousand"])
w2[["Country","life_expectancy","physicians_per_thousand"]].to_csv(f"{outdir}/W2_world_life_vs_phys.csv", index=False)
plt.figure(figsize=(8,6)); plt.scatter(w2["physicians_per_thousand"], w2["life_expectancy"])
plt.xlabel("Physicians per thousand"); plt.ylabel("Life expectancy (years)")
plt.title("VIEW world_2023 — W2: Life expectancy vs Physicians/1000")
plt.tight_layout(); plt.savefig(f"{outdir}/W2_world_life_vs_phys.png", dpi=150); plt.close()

# W3 — (SELECT Urbanizzazione vs CO2 nello script)
w3 = dfw.dropna(subset=["urban_population","population","co2_emissions_mt"]).copy()
w3["urban_pct"] = (w3["urban_population"] / w3["population"]) * 100.0
w3[["Country","urban_pct","co2_emissions_mt"]].to_csv(f"{outdir}/W3_world_urban_vs_co2.csv", index=False)
plt.figure(figsize=(8,6)); plt.scatter(w3["urban_pct"], w3["co2_emissions_mt"])
plt.xlabel("Popolazione urbana (%)"); plt.ylabel("CO₂ 2023 (Mt)")
plt.title("VIEW world_2023 — W3: Urbanizzazione vs CO₂")
plt.tight_layout(); plt.savefig(f"{outdir}/W3_world_urban_vs_co2.png", dpi=150); plt.close()

# W4 — (SELECT Life expectancy vs Out-of-pocket)
w4 = dfw.dropna(subset=["life_expectancy","oop_health_exp_pct"])
w4[["Country","life_expectancy","oop_health_exp_pct"]].to_csv(f"{outdir}/W4_world_life_vs_oop.csv", index=False)
plt.figure(figsize=(8,6)); plt.scatter(w4["oop_health_exp_pct"], w4["life_expectancy"])
plt.xlabel("Out-of-pocket health expenditure (%)"); plt.ylabel("Life expectancy (years)")
plt.title("VIEW world_2023 — W4: Life expectancy vs OOP (%)")
plt.tight_layout(); plt.savefig(f"{outdir}/W4_world_life_vs_oop.png", dpi=150); plt.close()

# ============================================================
# GRAFICI per VIEW energy (E1–E4) — generalizzati a TUTTI i paesi
# ============================================================

# E1 — Top-10 % rinnovabili (ultimo anno con dato) — SELECT con DISTINCT ON nello script
ren_nonnull = dfe.dropna(subset=["ren_share_tfec_pct"])
idx_ren = ren_nonnull.groupby("country_key")["year"].idxmax()
latest_ren = ren_nonnull.loc[idx_ren, ["country_key","year","ren_share_tfec_pct"]]
e1 = latest_ren.merge(dfw[["country_key","Country","population"]], on="country_key", how="inner")\
               .sort_values("ren_share_tfec_pct", ascending=False).head(10)
e1[["Country","year","ren_share_tfec_pct","population"]].to_csv(f"{outdir}/E1_energy_top10_ren.csv", index=False)
plt.figure(figsize=(10,6)); plt.bar(e1["Country"], e1["ren_share_tfec_pct"]); plt.xticks(rotation=45, ha='right')
plt.ylabel("% rinnovabili su TFEC"); plt.title("VIEW energy — E1: Top-10 quota rinnovabili (ultimo anno con dato)")
plt.tight_layout(); plt.savefig(f"{outdir}/E1_energy_top10_ren.png", dpi=150); plt.close()

# E2 — CO2 t/capita vs % rinnovabili (ultimo anno con entrambe) — SELECT both
both_nonnull = dfe.dropna(subset=["ren_share_tfec_pct","co2_kt"])
idx_both = both_nonnull.groupby("country_key")["year"].idxmax()
both_latest = both_nonnull.loc[idx_both, ["country_key","year","ren_share_tfec_pct","co2_kt"]]
e2 = both_latest.merge(dfw[["country_key","Country","population"]], on="country_key", how="inner")
e2["co2_t_per_capita"] = (e2["co2_kt"]*1000) / e2["population"]
e2[["Country","year","ren_share_tfec_pct","co2_t_per_capita"]].dropna().to_csv(f"{outdir}/E2_energy_ren_vs_co2pc.csv", index=False)
plt.figure(figsize=(8,6)); plt.scatter(e2["ren_share_tfec_pct"], e2["co2_t_per_capita"])
# retta OLS su punti finiti
mask = np.isfinite(e2["ren_share_tfec_pct"]) & np.isfinite(e2["co2_t_per_capita"])
if mask.sum() > 2:
    m, b = np.polyfit(e2.loc[mask,"ren_share_tfec_pct"], e2.loc[mask,"co2_t_per_capita"], 1)
    xs = np.linspace(e2["ren_share_tfec_pct"].min(), e2["ren_share_tfec_pct"].max(), 200)
    plt.plot(xs, m*xs + b)
plt.xlabel("% rinnovabili su TFEC (ultimo anno con entrambe)"); plt.ylabel("CO₂ pro capite (t)")
plt.title("VIEW energy — E2: CO₂ pc vs % rinnovabili")
plt.tight_layout(); plt.savefig(f"{outdir}/E2_energy_ren_vs_co2pc.png", dpi=150); plt.close()

# E3 — Serie storica accesso elettricità per bottom-5 — SELECT last_access + bottom5
acc_nonnull = dfe.dropna(subset=["access_electricity_pct"])
idx_acc = acc_nonnull.groupby("country_key")["year"].idxmax()
last_acc = acc_nonnull.loc[idx_acc, ["country_key","year","access_electricity_pct"]]
bottom5_keys = last_acc.sort_values("access_electricity_pct", ascending=True).head(5)["country_key"].tolist()
ts_bottom5 = dfe.loc[dfe["country_key"].isin(bottom5_keys), ["country_key","entity","year","access_electricity_pct"]]\
                .dropna(subset=["year","access_electricity_pct"]).sort_values(["entity","year"])
ts_bottom5.to_csv(f"{outdir}/E3_energy_access_timeseries_bottom5.csv", index=False)
plt.figure(figsize=(10,6))
for ent, g in ts_bottom5.groupby("entity"):
    plt.plot(g["year"], g["access_electricity_pct"], label=ent)
plt.xlabel("Anno"); plt.ylabel("% popolazione con accesso all'elettricità")
plt.title("VIEW energy — E3: Trend accesso elettricità (bottom-5)")
plt.legend(); plt.tight_layout(); plt.savefig(f"{outdir}/E3_energy_access_timeseries_bottom5.png", dpi=150); plt.close()

# E4 — Life expectancy (2023) vs GDP pro capite (ultimo anno) — SELECT last_gdp + pairs
gdp_nonnull = dfe.dropna(subset=["gdp_per_capita"])
idx_gdp = gdp_nonnull.groupby("country_key")["year"].idxmax()
last_gdp_pc = gdp_nonnull.loc[idx_gdp, ["country_key","gdp_per_capita"]]
pairs = last_gdp_pc.merge(dfw[["country_key","Country","life_expectancy"]], on="country_key", how="inner")\
                   .dropna(subset=["life_expectancy","gdp_per_capita"])
pairs[["Country","life_expectancy","gdp_per_capita"]].to_csv(f"{outdir}/E4_energy_life_vs_gdppc.csv", index=False)
corr_val = float(np.corrcoef(pairs["life_expectancy"], pairs["gdp_per_capita"])[0,1])
plt.figure(figsize=(8,6)); plt.scatter(pairs["gdp_per_capita"], pairs["life_expectancy"])
plt.xlabel("GDP pro capite (ultimo anno)"); plt.ylabel("Life expectancy (anni, 2023)")
plt.title(f"VIEW energy/world_2023 — E4: Life expectancy vs GDP pc (r = {corr_val:.2f})")
plt.tight_layout(); plt.savefig(f"{outdir}/E4_energy_life_vs_gdppc.png", dpi=150); plt.close()

# ============================================================
# GRAFICI per VIEW missing_migrants_region_year (M1)
# ============================================================
if len(mm_view):
    max_y = int(mm_view["year"].max())
    mm_last5 = mm_view[(mm_view["year"] >= max_y - 4) & (mm_view["year"] <= max_y)].copy()
    mm_last5.sort_values(["region_of_incident","year"]).to_csv(f"{outdir}/M1_migrants_regions_last5y.csv", index=False)
    plt.figure(figsize=(11,6))
    for reg, g in mm_last5.groupby("region_of_incident"):
        g = g.sort_values("year")
        plt.plot(g["year"], g["dead_missing"], label=reg)
    plt.xlabel("Anno"); plt.ylabel("Deceduti e dispersi (totale)")
    plt.title("VIEW missing_migrants_region_year — M1: Tendenza per regione (ultimi 5 anni)")
    plt.legend(); plt.tight_layout(); plt.savefig(f"{outdir}/M1_migrants_regions_last5y.png", dpi=150); plt.close()
else:
    print("VIEW missing_migrants_region_year: nessun dato aggregabile per il periodo considerato.")

print("OK: PNG/CSV salvati in", outdir)
