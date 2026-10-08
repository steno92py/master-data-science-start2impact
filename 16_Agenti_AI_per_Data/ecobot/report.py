"""Report offline con evidenze e grafici incorporati; nessuna API key."""
import base64
import html
import json
from pathlib import Path


def make_report(data, turns, chart_paths=()):
    escape = html.escape
    sections = ["<h1>EcoBot · EcoGrid Solutions</h1><p>Stefano Nocco · Agenti AI per Data</p>",
                "<p>Le analisi locali non dimostrano l'accuratezza di un modello AI. Dati mancanti non imputati; nessuna stima di bolletta.</p>",
                "<h2>Qualità e provenienza</h2><details><summary>Mostra dati, copertura e regole di pulizia</summary><pre>" + escape(json.dumps(data.quality(), ensure_ascii=False, indent=2)) + "</pre></details>"]
    charts = set(chart_paths)
    rendered = set()

    def chart_html(value):
        path = Path(value).resolve()
        # Esporta solo i PNG creati dai tool nell'apposita cartella.
        if (path in rendered or path.parent != data.output_dir.resolve()
                or not path.name.startswith("energia_") or path.suffix != ".png" or not path.is_file()):
            return ""
        rendered.add(path)
        return '<img alt="Grafico energia" src="data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode() + '">'

    for turn in turns:
        sections.append("<h2>Domanda</h2><p>" + escape(turn["question"]) + "</p><h3>Risposta</h3><p>" + escape(turn["answer"]).replace("\n", "<br>") + "</p>")
        for step in turn.get("trace", []):
            if "chart_path" in step["result"]:
                sections.append(chart_html(step["result"]["chart_path"]))
        sections.append("<details><summary>Operazioni, risultati e consumo API</summary><pre>" + escape(json.dumps({k: v for k, v in turn.items() if k not in {"question", "answer"}}, ensure_ascii=False, indent=2)) + "</pre></details>")
    for value in sorted(charts):
        sections.append(chart_html(value))
    return '<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Report EcoBot</title><style>body{font:16px system-ui;line-height:1.55;max-width:1050px;margin:40px auto;padding:20px;color:#213c34}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f2f6f3;padding:18px;font-size:12px}img{width:100%}summary{cursor:pointer;padding:10px;background:#f2f6f3}details{margin:16px 0}h1,h2{color:#157c62}</style><body>' + "\n".join(sections) + "</body></html>"
