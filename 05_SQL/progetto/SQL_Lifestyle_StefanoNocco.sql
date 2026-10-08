-- ============================================================
-- SQL LIFESTYLE – PIPELINE INTEGRATA (PostgreSQL)
-- ============================================================
-- STORY – Come leggere questi dati
-- Otto sezioni narrative (S1–S8) raggruppate in 5 filoni:
--   • SDG 7 – Accesso all’energia (S1–S3)
--   • SDG 7 – Energia → emissioni (S4–S5)
--   • SDG 10 – Salute e prezzi (S6)
--   • Missing Migrants e SDG 10.7.3 (S7)
--   • SDG 8 – Lavoro dignitoso e istruzione (S8)
-- Note di metodo:
-- - “Ultimo anno per Paese” evita medie spurie, ma gli anni non coincidono tra Paesi.
-- - TFEC include biomassa tradizionale: rinnovabili “alte” ≠ sempre “pulite moderne”.
-- - Correlazione ≠ causalità: i grafici suggeriscono ipotesi, non conclusioni definitive.
-- ============================================================

-- 0) SCHEMA DEDICATO (facoltativo ma consigliato)
CREATE SCHEMA IF NOT EXISTS lifestyle;
SET search_path = lifestyle, public;

-- 1) STAGING: import “come viene” (TEXT), per evitare errori in COPY.
-- Sono partito da tabelle di staging dove tutto è TEXT. 
-- Così posso importare senza panico anche se i CSV hanno simboli di dollaro, 
-- percentuali o separatori di migliaia. Poi creo viste “pulite” con i cast e le note sulle unità.
-- Questo passaggio è fondamentale per riconoscere che i dati grezzi sono sporchi e necessitano di rielaborazioni. 

DROP TABLE IF EXISTS stg_world_2023 CASCADE;
CREATE TABLE stg_world_2023 (
  "Country" TEXT,
  "Density\n(P/Km2)" TEXT,
  "Abbreviation" TEXT,
  "Agricultural Land( %)" TEXT,
  "Land Area(Km2)" TEXT,
  "Armed Forces size" TEXT,
  "Birth Rate" TEXT,
  "Calling Code" TEXT,
  "Capital/Major City" TEXT,
  "Co2-Emissions" TEXT,
  "CPI" TEXT,
  "CPI Change (%)" TEXT,
  "Currency-Code" TEXT,
  "Fertility Rate" TEXT,
  "Forested Area (%)" TEXT,
  "Gasoline Price" TEXT,
  "GDP" TEXT,
  "Gross primary education enrollment (%)" TEXT,
  "Gross tertiary education enrollment (%)" TEXT,
  "Infant mortality" TEXT,
  "Largest city" TEXT,
  "Life expectancy" TEXT,
  "Maternal mortality ratio" TEXT,
  "Minimum wage" TEXT,
  "Official language" TEXT,
  "Out of pocket health expenditure" TEXT,
  "Physicians per thousand" TEXT,
  "Population" TEXT,
  "Population: Labor force participation (%)" TEXT,
  "Tax revenue (%)" TEXT,
  "Total tax rate" TEXT,
  "Unemployment rate" TEXT,
  "Urban_population" TEXT,
  "Latitude" TEXT,
  "Longitude" TEXT
);

DROP TABLE IF EXISTS stg_energy CASCADE;
CREATE TABLE stg_energy (
  "Entity" TEXT,
  "Year" TEXT,
  "Access to electricity (% of population)" TEXT,
  "Access to clean fuels for cooking" TEXT,
  "Renewable-electricity-generating-capacity-per-capita" TEXT,
  "Financial flows to developing countries (US $)" TEXT,
  "Renewable energy share in the total final energy consumption (%)" TEXT,
  "Electricity from fossil fuels (TWh)" TEXT,
  "Electricity from nuclear (TWh)" TEXT,
  "Electricity from renewables (TWh)" TEXT,
  "Low-carbon electricity (% electricity)" TEXT,
  "Primary energy consumption per capita (kWh/person)" TEXT,
  "Energy intensity level of primary energy (MJ/$2017 PPP GDP)" TEXT,
  "Value_co2_emissions_kt_by_country" TEXT,
  "Renewables (% equivalent primary energy)" TEXT,
  "gdp_growth" TEXT,
  "gdp_per_capita" TEXT,
  "Density\n(P/Km2)" TEXT,
  "Land Area(Km2)" TEXT,
  "Latitude" TEXT,
  "Longitude" TEXT
);

DROP TABLE IF EXISTS stg_missing_migrants CASCADE;
CREATE TABLE stg_missing_migrants (
  "Incident Type" TEXT,
  "Incident year" TEXT,
  "Reported Month" TEXT,
  "Region of Origin" TEXT,
  "Region of Incident" TEXT,
  "Country of Origin" TEXT,
  "Number of Dead" TEXT,
  "Minimum Estimated Number of Missing" TEXT,
  "Total Number of Dead and Missing" TEXT,
  "Number of Survivors" TEXT,
  "Number of Females" TEXT,
  "Number of Males" TEXT,
  "Number of Children" TEXT,
  "Cause of Death" TEXT,
  "Migration route" TEXT,
  "Location of death" TEXT,
  "Information Source" TEXT,
  "Coordinates" TEXT,
  "UNSD Geographical Grouping" TEXT
);

-- 2) IMPORT: Path assoluti sul server Postgres
COPY stg_world_2023 FROM '/world-data-2023.csv' WITH (FORMAT csv, HEADER true);
COPY stg_energy FROM '/global-data-on-sustainable-energy.csv' WITH (FORMAT csv, HEADER true);
COPY stg_missing_migrants FROM '/Global Missing Migrants Dataset.csv' WITH (FORMAT csv, HEADER true);

-- 3) VIEW “PULITE”: cast coerenti, normalizzazioni, country_key per JOIN robuste.
CREATE OR REPLACE VIEW world_2023 AS
SELECT
  lower(trim("Country")) AS country_key,
  "Country",
  NULLIF(replace("Population", ',', ''), '')::BIGINT AS population,
  NULLIF(replace("GDP", ',', ''), '')::NUMERIC AS gdp_usd,
  NULLIF("Life expectancy", '')::NUMERIC AS life_expectancy,
  NULLIF("Physicians per thousand", '')::NUMERIC AS physicians_per_thousand,
  NULLIF(replace("Gross primary education enrollment (%)", '%', ''), '')::NUMERIC AS gross_primary_enroll_pct,
  NULLIF(replace("Gross tertiary education enrollment (%)", '%', ''), '')::NUMERIC AS gross_tertiary_enroll_pct,
  NULLIF(replace("Out of pocket health expenditure", '%', ''), '')::NUMERIC AS oop_health_exp_pct,
  NULLIF(replace("Co2-Emissions", ',', ''), '')::NUMERIC AS co2_emissions_mt,
  NULLIF("Unemployment rate", '')::NUMERIC AS unemployment_rate_pct,
  NULLIF(replace("Urban_population", ',', ''), '')::BIGINT AS urban_population,
  NULLIF("Minimum wage",'')::NUMERIC AS minimum_wage,
  NULLIF("CPI",'')::NUMERIC AS cpi,
  NULLIF(replace("CPI Change (%)", '%',''),'')::NUMERIC AS cpi_change_pct,
  NULLIF(replace("Population: Labor force participation (%)",'%',''),'')::NUMERIC AS labor_force_pct
FROM stg_world_2023;

CREATE OR REPLACE VIEW energy AS
SELECT
  lower(trim("Entity")) AS country_key,
  NULLIF("Entity",'') AS entity,
  NULLIF("Year",'')::INT AS year,
  NULLIF("Access to electricity (% of population)",'')::NUMERIC AS access_electricity_pct,
  NULLIF("Access to clean fuels for cooking",'')::NUMERIC AS clean_cooking_pct,
  NULLIF("Renewable-electricity-generating-capacity-per-capita",'')::NUMERIC AS ren_capacity_per_capita,
  NULLIF("Financial flows to developing countries (US $)",'')::NUMERIC AS financial_flows_usd,
  NULLIF("Renewable energy share in the total final energy consumption (%)",'')::NUMERIC AS ren_share_tfec_pct,
  NULLIF("Electricity from fossil fuels (TWh)",'')::NUMERIC AS elec_fossil_twh,
  NULLIF("Electricity from nuclear (TWh)",'')::NUMERIC AS elec_nuclear_twh,
  NULLIF("Electricity from renewables (TWh)",'')::NUMERIC AS elec_renewables_twh,
  NULLIF("Low-carbon electricity (% electricity)",'')::NUMERIC AS low_carbon_elec_pct,
  NULLIF("Primary energy consumption per capita (kWh/person)",'')::NUMERIC AS primary_energy_pc_kwh,
  NULLIF("Energy intensity level of primary energy (MJ/$2017 PPP GDP)",'')::NUMERIC AS energy_intensity_mj_per_ppp,
  NULLIF("Value_co2_emissions_kt_by_country",'')::NUMERIC AS co2_kt,
  NULLIF("Renewables (% equivalent primary energy)",'')::NUMERIC AS renewables_equiv_pct,
  NULLIF("gdp_growth",'')::NUMERIC AS gdp_growth,
  NULLIF("gdp_per_capita",'')::NUMERIC AS gdp_per_capita
FROM stg_energy;

CREATE OR REPLACE VIEW missing_migrants_region_year AS
SELECT
  NULLIF("Region of Incident",'') AS region_of_incident,
  NULLIF("Incident year",'')::INT AS year,
  SUM(NULLIF("Total Number of Dead and Missing",'')::INT) AS dead_missing
FROM stg_missing_migrants
WHERE "Region of Incident" IS NOT NULL
GROUP BY 1,2;

-- 4) SCHEMA RELAZIONALE: dimensione Paese + fatti
DROP TABLE IF EXISTS dim_country CASCADE;
CREATE TABLE dim_country (
  country_id        BIGSERIAL PRIMARY KEY,
  country_key       TEXT UNIQUE NOT NULL,
  country_name      TEXT NOT NULL,
  population_2023   BIGINT,
  gdp_usd_2023      NUMERIC,
  life_expectancy_2023 NUMERIC,
  physicians_per_thousand_2023 NUMERIC,
  gross_primary_enroll_pct_2023 NUMERIC,
  gross_tertiary_enroll_pct_2023 NUMERIC,
  oop_health_exp_pct_2023 NUMERIC,
  co2_emissions_mt_2023 NUMERIC,
  unemployment_rate_pct_2023 NUMERIC,
  urban_population_2023 BIGINT,
  minimum_wage_2023 NUMERIC,
  cpi_2023 NUMERIC,
  cpi_change_pct_2023 NUMERIC,
  labor_force_pct_2023 NUMERIC
);

INSERT INTO dim_country (
  country_key, country_name, population_2023, gdp_usd_2023,
  life_expectancy_2023, physicians_per_thousand_2023,
  gross_primary_enroll_pct_2023, gross_tertiary_enroll_pct_2023,
  oop_health_exp_pct_2023, co2_emissions_mt_2023,
  unemployment_rate_pct_2023, urban_population_2023,
  minimum_wage_2023, cpi_2023, cpi_change_pct_2023, labor_force_pct_2023
)
SELECT
  country_key, "Country", population, gdp_usd,
  life_expectancy, physicians_per_thousand,
  gross_primary_enroll_pct, gross_tertiary_enroll_pct,
  oop_health_exp_pct, co2_emissions_mt,
  unemployment_rate_pct, urban_population,
  minimum_wage, cpi, cpi_change_pct, labor_force_pct
FROM world_2023;

-- ENERGIA ANNUALE (2000–2020)
DROP TABLE IF EXISTS fact_energy_yearly CASCADE;
CREATE TABLE fact_energy_yearly (
  country_id               BIGINT NOT NULL REFERENCES dim_country(country_id),
  year                     INT NOT NULL,
  access_electricity_pct   NUMERIC,
  clean_cooking_pct        NUMERIC,
  ren_capacity_per_capita  NUMERIC,
  financial_flows_usd      NUMERIC,
  ren_share_tfec_pct       NUMERIC,
  elec_fossil_twh          NUMERIC,
  elec_nuclear_twh         NUMERIC,
  elec_renewables_twh      NUMERIC,
  low_carbon_elec_pct      NUMERIC,
  primary_energy_pc_kwh    NUMERIC,
  energy_intensity_mj_per_ppp NUMERIC,
  co2_kt                   NUMERIC,
  renewables_equiv_pct     NUMERIC,
  gdp_growth               NUMERIC,
  gdp_per_capita           NUMERIC,
  CONSTRAINT fact_energy_yearly_pk PRIMARY KEY (country_id, year)
);

INSERT INTO fact_energy_yearly (
  country_id, year,
  access_electricity_pct, clean_cooking_pct, ren_capacity_per_capita,
  financial_flows_usd, ren_share_tfec_pct, elec_fossil_twh, elec_nuclear_twh,
  elec_renewables_twh, low_carbon_elec_pct, primary_energy_pc_kwh,
  energy_intensity_mj_per_ppp, co2_kt, renewables_equiv_pct,
  gdp_growth, gdp_per_capita
)
SELECT
  dc.country_id, e.year,
  e.access_electricity_pct, e.clean_cooking_pct, e.ren_capacity_per_capita,
  e.financial_flows_usd, e.ren_share_tfec_pct, e.elec_fossil_twh, e.elec_nuclear_twh,
  e.elec_renewables_twh, e.low_carbon_elec_pct, e.primary_energy_pc_kwh,
  e.energy_intensity_mj_per_ppp, e.co2_kt, e.renewables_equiv_pct,
  e.gdp_growth, e.gdp_per_capita
FROM energy e
JOIN dim_country dc USING (country_key);

-- MIGRANTI (regionale, anno)
DROP TABLE IF EXISTS fact_missing_migrants_region_year CASCADE;
CREATE TABLE fact_missing_migrants_region_year (
  region_of_incident TEXT NOT NULL,
  year               INT NOT NULL,
  dead_missing       INT NOT NULL,
  CONSTRAINT fact_mmry_pk PRIMARY KEY (region_of_incident, year)
);

INSERT INTO fact_missing_migrants_region_year (region_of_incident, year, dead_missing)
SELECT region_of_incident, year, dead_missing
FROM missing_migrants_region_year;

-- 5) “TABELLA PONTE”: collega dimensione Paese a id energia per join flessibili.
-- Qui non ho un id_sustainable_energy nativo: uso la chiave (country_id, year) come surrogato.
--    Serve solo per allineare al pattern del primo lavoro; nella pratica la fact sopra è sufficiente.
DROP TABLE IF EXISTS sustainable_countries_bridge CASCADE;
CREATE TABLE sustainable_countries_bridge (
  id BIGSERIAL PRIMARY KEY,
  country_id BIGINT NOT NULL REFERENCES dim_country(country_id),
  year INT NOT NULL,
  UNIQUE (country_id, year)
);
INSERT INTO sustainable_countries_bridge (country_id, year)
SELECT country_id, year FROM fact_energy_yearly;

-- 6) QUERY ANALITICHE

-- ============================================================
-- STORY S1 – La luce che manca / La cucina che fuma (SDG 7)
-- ============================================================
-- Ultimo anno disponibile per Paese (spesso 2020):
--   Accesso elettricità bottom-5: South Sudan ~7,2%, Chad ~11,1%,
--   Burundi ~11,7%, Malawi ~14,9%, Central African Republic ~15,5%.
--   Clean cooking bottom-5: South Sudan 0,0%, Burundi 0,2%,
--   Liberia 0,4%, Uganda 0,5%, Central African Republic 0,8%.
-- Traduzione “umana”: scuola serale che non parte, cliniche senza frigo,
-- cucine che fumano dentro casa → salute peggiore e tempo perso.
-- Le due SELECT (6.1 e 6.11) danno la foto e, volendo, il film (serie storiche) di tutto questo.

--    6.1 SDG 7 – Paesi con minore accesso a elettricità e clean cooking (ULTIMO anno disponibile)
WITH last_access AS (
  SELECT DISTINCT ON (country_id)
         country_id, year, access_electricity_pct, clean_cooking_pct
  FROM fact_energy_yearly
  WHERE access_electricity_pct IS NOT NULL OR clean_cooking_pct IS NOT NULL
  ORDER BY country_id, year DESC
)
SELECT d.country_name AS country,
       la.year,
       ROUND(la.access_electricity_pct,1) AS access_electricity_pct,
       ROUND(la.clean_cooking_pct,1)      AS clean_cooking_pct
FROM last_access la
JOIN dim_country d USING (country_id)
ORDER BY access_electricity_pct ASC NULLS LAST, clean_cooking_pct ASC NULLS LAST
LIMIT 25;

--    6.11 Accesso elettricità: bottom-5 (ultimo anno) + serie storiche
WITH last_access AS (
  SELECT DISTINCT ON (country_id) country_id, year, access_electricity_pct
  FROM fact_energy_yearly
  WHERE access_electricity_pct IS NOT NULL
  ORDER BY country_id, year DESC
),
bottom5 AS (
  SELECT country_id
  FROM last_access
  ORDER BY access_electricity_pct ASC
  LIMIT 5
)
SELECT d.country_name AS country, f.year, ROUND(f.access_electricity_pct,1) AS access_electricity_pct
FROM fact_energy_yearly f
JOIN bottom5 b USING (country_id)
JOIN dim_country d USING (country_id)
WHERE f.access_electricity_pct IS NOT NULL
ORDER BY d.country_name, f.year;
-- ============================================================

-- ============================================================
-- STORY S2 – Pandemia e scale energetiche (SDG 7)
-- ============================================================
-- Dal 2020 in poi si vedono scosse su consumo pro capite, CO₂ e crescita:
-- arresti, rimbalzi e divergenze tra Paesi.
-- Questa sezione (6.2) serve per contestualizzare il “dopo 2020” senza
-- mescolare trend pre-pandemici.
--    6.2 SDG 7 – Consumo energia pro capite, CO₂ totale, crescita e PIL pro capite (periodo 2020+)

SELECT d.country_name AS country, f.year,
       ROUND(f.primary_energy_pc_kwh,0) AS primary_energy_pc_kwh,
       ROUND(f.co2_kt,0) AS co2_kt,
       ROUND(f.gdp_growth,2) AS gdp_growth,
       ROUND(f.gdp_per_capita,0) AS gdp_per_capita
FROM fact_energy_yearly f
JOIN dim_country d USING (country_id)
WHERE f.year >= 2020
ORDER BY country;
-- ============================================================

-- ============================================================
-- STORY S3 – Quando il mix diventa low-carbon (SDG 7)
-- ============================================================
-- Nel 2011–2019 il dataset registra anni con ~100% di elettricità low-carbon
-- per Islanda (es. 2013, 2018) e Lesotho (es. 2014–2017).
-- Messaggio: il settore elettrico può “diventare pulito” quando idroelettrico/geotermia
-- o nucleare sono sostanziosi. La 6.3 trova i “campioni”; la 6.4 ne mostra il mix.
--    6.3 SDG 7 – Top-50 per % low-carbon electricity (2011–2019)
SELECT d.country_name AS country, f.year, f.low_carbon_elec_pct
FROM fact_energy_yearly f
JOIN dim_country d USING (country_id)
WHERE f.year > 2010 AND f.year < 2020
ORDER BY f.low_carbon_elec_pct DESC NULLS LAST
LIMIT 50;

--    6.4 SDG 7 – Mix fonti elettriche dei top-50 (fossile/nucleare/rinnovabili)
WITH top50 AS (
  SELECT d.country_id, f.year
  FROM fact_energy_yearly f
  JOIN dim_country d USING (country_id)
  WHERE f.year > 2010 AND f.year < 2020
  ORDER BY f.low_carbon_elec_pct DESC NULLS LAST
  LIMIT 50
)
SELECT d.country_name AS country, f.year,
       f.elec_fossil_twh, f.elec_nuclear_twh, f.elec_renewables_twh, f.low_carbon_elec_pct
FROM fact_energy_yearly f
JOIN top50 t ON t.country_id = f.country_id AND t.year = f.year
JOIN dim_country d ON d.country_id = f.country_id
ORDER BY f.low_carbon_elec_pct DESC NULLS LAST;

--    6.5 SDG 7 – Ultimi 50 per low-carbon e relativi flussi finanziari alle rinnovabili
SELECT d.country_name AS country, f.year,
       f.financial_flows_usd, f.elec_fossil_twh, f.elec_nuclear_twh, f.elec_renewables_twh, f.low_carbon_elec_pct
FROM fact_energy_yearly f
JOIN dim_country d USING (country_id)
WHERE f.year > 2010 AND f.year < 2020
ORDER BY f.low_carbon_elec_pct ASC NULLS LAST
LIMIT 50;
-- ============================================================

-- ============================================================
-- STORY S4 – TFEC vs CO₂: la direzione del legame (SDG 7)
-- ============================================================
-- Nota: la CO₂ pro capite è calcolata con population_2023; anni diversi tra Paesi restano possibili.
-- Ultimo anno per Paese: più alta quota rinnovabili nel TFEC tende ad associarsi
-- a minore CO₂ pro capite (corr ≈ −0,55). Non è causalità, ma la direzione è chiara.
-- Avvertenza: TFEC include biomassa tradizionale → “rinnovabile” non sempre = “pulito”.
-- 6.12 per lo scatter (dataset riga-per-Paese), 6.12b per la correlazione sintetica.
--    6.12 Rinnovabili (TFEC) vs CO₂ t/capite: ultimo anno in cui entrambe disponibili
WITH both AS (
  SELECT DISTINCT ON (f.country_id) f.country_id, f.year, f.ren_share_tfec_pct, f.co2_kt
  FROM fact_energy_yearly f
  WHERE f.ren_share_tfec_pct IS NOT NULL AND f.co2_kt IS NOT NULL
  ORDER BY f.country_id, f.year DESC
)
SELECT d.country_name AS country, b.year,
       ROUND(b.ren_share_tfec_pct,2) AS ren_share_tfec_pct,
       ROUND((b.co2_kt * 1000.0) / NULLIF(d.population_2023,0), 3) AS co2_t_per_capita
FROM both b
JOIN dim_country d USING (country_id)
WHERE d.population_2023 IS NOT NULL;

--    6.12b Correlazione TFEC vs CO₂ t/capite (ultimo anno per Paese)
WITH both AS (
  SELECT DISTINCT ON (f.country_id)
         f.country_id, f.year, f.ren_share_tfec_pct, f.co2_kt
  FROM fact_energy_yearly f
  WHERE f.ren_share_tfec_pct IS NOT NULL
    AND f.co2_kt IS NOT NULL
  ORDER BY f.country_id, f.year DESC
),
ds AS (
  SELECT
    b.country_id,
    b.ren_share_tfec_pct,
    (b.co2_kt * 1000.0) / NULLIF(d.population_2023,0) AS co2_t_per_capita
  FROM both b
  JOIN dim_country d USING (country_id)
  WHERE d.population_2023 IS NOT NULL
)
SELECT corr(ren_share_tfec_pct, co2_t_per_capita) AS corr_tfec_vs_co2_tcap
FROM ds;

-- ============================================================
-- STORY S4b – Classifica composita (rinnovabili↑, accesso↑, CO₂↓)
-- ============================================================
-- Perché: serve un “punteggio sintetico” che premi Paesi con quota rinnovabili alta,
-- accesso elettrico ampio e basse emissioni pro capite. È una lettura rapida su “chi sta andando meglio”.
-- Metodo: media dei rank (RANK) sulle tre dimensioni, con direzione coerente (CO₂ al contrario).
-- Lettura: score_avg più basso = migliore. Ordina la short list per confronto tra pari.
-- Caveat: pesi = 1/3 ciascuno, non normalizza scale; per sensibilità diverse cambia i pesi
-- o usa z-score/min–max. RANK gestisce i pari merito. Dati mancanti → Paese escluso.

--    6.13 Indice composito semplice (rinnovabili↑, elettricità↑, CO₂ pro capite↓) – ultimo anno
WITH last_ren AS (
  SELECT DISTINCT ON (country_id) country_id, year, ren_share_tfec_pct
  FROM fact_energy_yearly WHERE ren_share_tfec_pct IS NOT NULL
  ORDER BY country_id, year DESC
),
last_acc AS (
  SELECT DISTINCT ON (country_id) country_id, year AS y_acc, access_electricity_pct
  FROM fact_energy_yearly WHERE access_electricity_pct IS NOT NULL
  ORDER BY country_id, year DESC
),
last_co2 AS (
  SELECT DISTINCT ON (country_id) country_id, year AS y_co2, co2_kt
  FROM fact_energy_yearly WHERE co2_kt IS NOT NULL
  ORDER BY country_id, year DESC
),
joined AS (
  SELECT d.country_name AS country, d.country_id,
         lr.ren_share_tfec_pct, la.access_electricity_pct,
         (lc.co2_kt * 1000.0) / NULLIF(d.population_2023,0) AS co2_t_per_capita
  FROM dim_country d
  JOIN last_ren lr USING (country_id)
  JOIN last_acc la USING (country_id)
  JOIN last_co2 lc USING (country_id)
  WHERE d.population_2023 IS NOT NULL
),
ranks AS (
  SELECT *,
         RANK() OVER (ORDER BY ren_share_tfec_pct DESC) AS r_ren,
         RANK() OVER (ORDER BY access_electricity_pct DESC) AS r_acc,
         RANK() OVER (ORDER BY co2_t_per_capita ASC) AS r_co2
  FROM joined
)
SELECT country,
       ROUND(ren_share_tfec_pct,1) AS ren_share_tfec_pct,
       ROUND(access_electricity_pct,1) AS access_electricity_pct,
       ROUND(co2_t_per_capita,3) AS co2_t_per_capita,
       (r_ren + r_acc + r_co2) AS score_sum,
       ROUND(((r_ren + r_acc + r_co2)::NUMERIC)/3.0, 1) AS score_avg
FROM ranks
ORDER BY score_avg ASC
LIMIT 25;
-- ============================================================

-- ============================================================
-- STORY S5 – Ricchi, ma con mix a basse emissioni ancora ridotto (SDG 7)
-- ============================================================
-- Alcuni Paesi ad alto reddito restano bassi sul TFEC rinnovabile (ultimo anno):
-- esempi nel dataset: Qatar (~0,04%), Singapore (~0,84%), USA (~10,4%),
-- Paesi Bassi (~8,5%), Australia (~10,1%).
-- Traduzione: il settore elettrico conta, ma anche trasporti e calore fossili pesano.
-- La 6.15 isola questi casi per un’azione “policy mirata”.
--    6.15 SDG 7 – Outlier: alto reddito ma bassa quota rinnovabili (ultimo anno per Paese)
WITH latest AS (
  SELECT DISTINCT ON (f.country_id)
         f.country_id, f.year, f.ren_share_tfec_pct, f.gdp_per_capita
  FROM fact_energy_yearly f
  WHERE f.gdp_per_capita IS NOT NULL
    AND f.ren_share_tfec_pct IS NOT NULL
  ORDER BY f.country_id, f.year DESC
)
SELECT d.country_name AS country,
       latest.year,
       ROUND(latest.gdp_per_capita, 0) AS gdp_per_capita,
       ROUND(latest.ren_share_tfec_pct, 2) AS ren_share_tfec_pct
FROM latest
JOIN dim_country d USING (country_id)
WHERE latest.gdp_per_capita > 40000   -- soglia “alto reddito”
  AND latest.ren_share_tfec_pct < 15  -- soglia “basse rinnovabili”
ORDER BY latest.gdp_per_capita DESC, country;
-- ============================================================

-- ============================================================
-- STORY S6 – Curva di Preston: più reddito, più anni di vita… ma con rendimenti decrescenti (SDG 10)
-- ============================================================
-- Incrociando aspettativa di vita (2023) e PIL pro capite (ultimo anno per Paese)
-- emerge la classica relazione: corr ≈ +0,64. Il salto è forte da povero a medio,
-- poi i guadagni rallentano. Per aumentare gli anni di vita, oltre al reddito,
-- servono sistemi sanitari equi (OOP bassa), istruzione, infrastrutture di base.
-- La 6.9 calcola la correlazione (e puoi estrarre i punti per lo scatter).
--    6.9 SDG 10 – Relazione aspettativa di vita (2023) e PIL pro capite (ultimo anno): curva di Preston
-- Nota: qui uso life_expectancy_2023 e l’ultimo gdp_per_capita disponibile per Paese.

WITH last_gdp AS (
  SELECT DISTINCT ON (country_id) country_id, gdp_per_capita
  FROM fact_energy_yearly
  WHERE gdp_per_capita IS NOT NULL
  ORDER BY country_id, year DESC
),
pairs AS (
  SELECT d.country_name, d.life_expectancy_2023::FLOAT8 AS life_exp, lg.gdp_per_capita::FLOAT8 AS gdp_pc
  FROM dim_country d
  JOIN last_gdp lg USING (country_id)
  WHERE d.life_expectancy_2023 IS NOT NULL
)
SELECT corr(life_exp, gdp_pc) AS pearson_corr_lifeexp_gdppc FROM pairs;

--    6.10 CPI sotto media con PIL totale e PIL pro capite (join con ultimo gdp_pc disponibile)
WITH avg_cpi AS (
  SELECT AVG(cpi_2023) AS c FROM dim_country WHERE cpi_2023 IS NOT NULL
),
last_gdp_pc AS (
  SELECT DISTINCT ON (country_id) country_id, gdp_per_capita
  FROM fact_energy_yearly
  WHERE gdp_per_capita IS NOT NULL
  ORDER BY country_id, year DESC
)
SELECT d.country_id, d.country_name, d.cpi_2023, d.cpi_change_pct_2023,
       d.gdp_usd_2023, lg.gdp_per_capita
FROM dim_country d
CROSS JOIN avg_cpi a
LEFT JOIN last_gdp_pc lg ON lg.country_id = d.country_id
WHERE d.cpi_2023 IS NOT NULL AND d.cpi_2023 < a.c
ORDER BY d.country_name;
-- ============================================================

-- ============================================================
-- STORY S7 – Rotte di chi parte e non arriva (Missing Migrants)
-- ============================================================
-- Ho anche fatto un notebook Kaggle sul fenomeno: 
-- https://www.kaggle.com/code/snocco/missing-migrants-deaths-in-the-mediterranean-sea
-- Ultimi 5 anni disponibili: nel 2023 il Mediterraneo registra ~1.931 morti/scomparsi,
-- in calo di ~475 rispetto al 2022 (“minimo noto” OIM: ciò che non si riporta non entra).
-- La serie non scende in linea retta: contano conflitti, politiche e rotte.
-- La 6.14 produce la tabella per un grafico ad area impilata per regione.
--    6.14 Missing Migrants: ultimi 5 anni per regione
WITH max_y AS (
  SELECT MAX(year) AS y FROM fact_missing_migrants_region_year
),
subset AS (
  SELECT mm.*
  FROM fact_missing_migrants_region_year mm, max_y
  WHERE mm.year BETWEEN (max_y.y - 4) AND max_y.y
)
SELECT region_of_incident, year, dead_missing
FROM subset
ORDER BY region_of_incident, year;

-- ============================================================
-- STORY S8 – Sotto i 2$ e la scuola che non continua (SDG 8)
-- ============================================================
-- Il 2023 incrocia 15 Paesi con salario minimo < 2 USD/ora e istruzione critica
-- (primaria <50% o terziaria <5%). Esempi nell’output: Chad (~0,60 USD, terziaria ~3,3%),
-- Equatorial Guinea (~1,05 USD, terziaria ~1,9%). È la trappola “redditi bassi + bassa prosecuzione”.
-- Le 6.6 e 6.8 danno la lista operativa per priorità di intervento.
--    6.6 SDG 8 – Paesi con salario minimo < 2 USD/ora (dal dataset 2023)
SELECT country_id, country_name AS name
FROM dim_country
WHERE minimum_wage_2023 IS NOT NULL AND minimum_wage_2023 < 2
ORDER BY name;

--    6.7 SDG 8 – Disoccupazione > 15% o forza lavoro < 50%
SELECT country_id, country_name AS name, unemployment_rate_pct_2023, labor_force_pct_2023
FROM dim_country
WHERE (unemployment_rate_pct_2023 > 15) OR (labor_force_pct_2023 < 50)
ORDER BY name;

--    6.8 SDG 8 – Salario minimo <2 con bassa iscrizione primaria (<50%) o terziaria (<5%)
SELECT country_id, country_name AS name,
       minimum_wage_2023, gross_primary_enroll_pct_2023, gross_tertiary_enroll_pct_2023
FROM dim_country
WHERE minimum_wage_2023 < 2
  AND (
       gross_primary_enroll_pct_2023 < 50 OR
       gross_tertiary_enroll_pct_2023 < 5
  )
ORDER BY name;
-- ============================================================

-- 7) INDICI CONSIGLIATI (in pratica, quelli che servono davvero)
-- Obiettivo: rendere veloci le cose che faccio più spesso in questo file,
-- senza riempire il DB di indici inutili.

-- 1) DIMENSIONE PAESI
-- Ordinare/ricercare per nome Paese è comodo in molte tabelle finali.
CREATE INDEX IF NOT EXISTS idx_dim_country_name ON dim_country (country_name);

-- 2) SERIE STORICHE ENERGIA
-- Moltissime query chiedono “l’ultimo anno per Paese” (DISTINCT ON + ORDER BY year DESC).
-- Questo indice accoppia Paese+Anno nell’ordine giusto e velocizza quei casi.
CREATE INDEX IF NOT EXISTS idx_fey_country_year_desc
  ON fact_energy_yearly (country_id, year DESC);

-- Alcune query filtrano per anno e poi ordinano per % low-carbon (top/bottom con LIMIT).
-- Questo indice aiuta proprio quel pattern.
CREATE INDEX IF NOT EXISTS idx_fey_year_lowcarbon
  ON fact_energy_yearly (year, low_carbon_elec_pct);

-- Nota:
-- - Non serve specificare DESC sugli altri indici: Postgres sa leggere un B-Tree anche al contrario.
-- - Evito indici duplicati: se in alto (sezione 4) ho creato indici su (year), (ren_share_tfec_pct) o (co2_kt),
-- - Li rimuovo o li commento: i due composti qui sopra coprono già i casi che mi interessano.

-- 3) MIGRANTI (REGIONE/ANNO)
-- La tabella ha già una PRIMARY KEY su (region_of_incident, year): basta e avanza per le query.
-- Nessun indice in più qui.


-- ============================================================
-- FINE
-- GRAZIE PER LA LETTURA!
-- STEFANO NOCCO
-- ============================================================
