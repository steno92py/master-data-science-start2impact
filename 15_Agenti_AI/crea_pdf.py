"""Relazione di consegna: architettura, prove osservate e video verificato."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse
from xml.sax.saxutils import escape
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--video-url', required=True, help='URL HTTPS già verificato')
args = parser.parse_args()
assert urlparse(args.video_url).scheme == 'https'
old = json.loads((ROOT/'evidenze/prove_reali.json').read_text())
demo = json.loads((ROOT/'evidenze/demo_video_2026-10-08.json').read_text())
tests = json.loads((ROOT/'evidenze/test_workflow.json').read_text())
workflow = json.loads((ROOT/'workflow.json').read_text())
assert len(old['executions']) == 9 and len(demo['executions']) == 2
assert all(x['execution']['status'] == 'success' for x in demo['executions'])
assert len(workflow['nodes']) == 14 and all(x['passed'] for x in tests['checks'])
FONTDIR = Path('/System/Library/Fonts/Supplemental')
for name, file in [('Body','Arial.ttf'),('Bold','Arial Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONTDIR/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
DEST = ROOT/'consegna/Progetto Agenti AI di Stefano Nocco.pdf'
DEST.parent.mkdir(parents=True, exist_ok=True)
W,H = 842,595
c = canvas.Canvas(str(DEST), pagesize=(W,H))
c.setTitle('Progetto Agenti AI di Stefano Nocco')
c.setAuthor('Stefano Nocco')
c.setSubject('Assistente Telegram, n8n, Airtable, Gmail e Google Calendar - relazione e prove reali')
INK = HexColor('#183b3b'); MUTED = HexColor('#516563'); ACCENT = HexColor('#177d69')
BG = HexColor('#f6f7f2'); PALE = HexColor('#e6eee7'); LINE = HexColor('#c9d8d0')
TOTAL = 10

def txt(body,x,y,width=746,size=12,color=INK,bold=False,leading=None):
    style=ParagraphStyle('p',fontName='Bold' if bold else 'Body',fontSize=size,
                         leading=leading or size*1.35,textColor=color)
    p=Paragraph(body,style); _,height=p.wrap(width,H)
    assert y-height >= 47, (body[:70], y-height)
    p.drawOn(c,x,y-height)
    return y-height

def page(n,kicker,title,subtitle):
    c.setFillColor(BG);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(ACCENT);c.rect(48,546,30,5,fill=1,stroke=0)
    txt(kicker.upper(),91,555,size=9.5,color=ACCENT,bold=True)
    txt(title,48,520,size=28,bold=True)
    txt(subtitle,48,476,size=11.5,color=MUTED)
    c.setStrokeColor(LINE);c.line(48,42,794,42)
    c.setFont('Body',8);c.setFillColor(MUTED)
    c.drawString(48,26,'STEFANO NOCCO  |  START2IMPACT  |  8 OTTOBRE 2026')
    c.drawRightString(794,26,f'{n:02d} / {TOTAL:02d}')
    c.bookmarkPage(f'p{n}');c.addOutlineEntry(title,f'p{n}',0,False)

def box(x,y,w,h,title,body,size=11):
    c.setFillColor(PALE);c.roundRect(x,y-h,w,h,9,fill=1,stroke=0)
    txt(title,x+15,y-13,w-30,14,bold=True)
    bottom=txt(body,x+15,y-42,w-30,size,color=MUTED)
    assert bottom >= y-h+10, (title, bottom, y-h)

def table(rows,y,widths,size=10.5,pad=6):
    styles=[ParagraphStyle('th',fontName='Bold',fontSize=size,leading=size*1.23,textColor=INK),
            ParagraphStyle('td',fontName='Body',fontSize=size,leading=size*1.23,textColor=INK)]
    cells=[[Paragraph(escape(str(v)),styles[int(i>0)]) for v in row] for i,row in enumerate(rows)]
    t=Table(cells,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#cfe2d8')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#ffffff'),HexColor('#edf2ed')]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),
        ('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),pad),
        ('BOTTOMPADDING',(0,0),(-1,-1),pad)]))
    _,h=t.wrap(sum(widths),H); assert y-h >= 49, ('table',h,y)
    t.drawOn(c,48,y-h);return y-h

def shot(file,x,y,w,h,crop=None):
    im=Image.open(ROOT/file)
    if crop: im=im.crop(crop)
    scale=min(w/im.width,h/im.height);iw,ih=im.width*scale,im.height*scale
    c.drawImage(ImageReader(im),x,y-ih,width=iw,height=ih,mask='auto')
    return y-ih

def link(label,url,x,y,width=746,size=12):
    return txt(f'<link href="{escape(url, {chr(34): "&quot;"})}" color="#177d69"><u>{escape(label)}</u></link>',x,y,width,size)

page(1,'Progetto Agenti AI','Un assistente personale in Telegram',
     'Email e calendario in linguaggio naturale, con rubrica verificata e memoria della conversazione.')
txt('DAL MESSAGGIO AL RISULTATO',48,434,size=10,color=ACCENT,bold=True)
txt('Il progetto collega una chat Telegram a un agente n8n capace di interpretare richieste scritte o vocali, '
    'recuperare un contatto da Airtable, inviare un’email con Gmail e creare un appuntamento in Google Calendar.',48,410,width=710,size=16)
for x,value,label in [(48,'14','nodi nel workflow'),(240,'11','esecuzioni reali'),(432,'12','controlli locali'),(624,'2:30','video finale')]:
    c.setFillColor(PALE);c.roundRect(x,234,170,84,8,fill=1,stroke=0)
    txt(value,x+15,307,140,29,bold=True);txt(label,x+15,265,140,10.5,color=MUTED)
box(48,211,363,132,'Obiettivo e criterio di progetto',
    'Ridurre i passaggi fra chat, rubrica, email e calendario. Una bozza resta in chat; un invio o un evento richiede '
    'una richiesta esplicita. Il risultato viene controllato anche nel servizio finale.',11.5)
box(431,211,363,132,'Guida alla lettura',
    'Pagine 2-5: architettura, nodi e regole.<br/>Pagine 6-7: dimostrazione email e calendario.<br/>'
    'Pagine 8-9: prove, risultati e limiti.<br/>Pagina 10: video, file e riferimenti.',11.5)
c.showPage()

page(2,'Architettura','Un flusso, tre tipi di ingresso',
     'Il percorso distingue preparazione dei dati, decisione dell’agente ed esecuzione degli strumenti.')
def node(x,y,w,title,detail):
    box(x,y,w,65,title,detail,9.4)
def arrow(x1,y1,x2,y2):
    c.setStrokeColor(ACCENT);c.setLineWidth(1.5);c.line(x1,y1,x2,y2)
    if x1==x2:
        d=1 if y2>y1 else -1;c.line(x2,y2,x2-3,y2-d*5);c.line(x2,y2,x2+3,y2-d*5)
    else:
        d=1 if x2>x1 else -1;c.line(x2,y2,x2-d*5,y2-3);c.line(x2,y2,x2-d*5,y2+3)
node(48,430,167,'Telegram','Trigger + chat autorizzata')
node(244,430,150,'Switch','Testo / voce / altro')
node(426,430,172,'Input uniforme','Testo o trascrizione')
node(630,430,164,'AI Agent','Modello + memoria')
arrow(215,398,244,398);arrow(394,398,426,398);arrow(598,398,630,398)
box(48,339,350,102,'Ramo vocale',
    'Get Voice File scarica il file Telegram. OpenAI lo trascrive; Normalizza input produce lo stesso campo '
    '<b>input_text</b> utilizzato dalle richieste testuali.',11)
box(418,339,376,102,'Ramo non supportato',
    'Sticker e altri formati ricevono una risposta che invita a usare testo o una nota vocale. '
    'Questo percorso termina prima dell’agente e non richiede una chiamata al modello.',11)
box(48,215,350,116,'Strumenti scelti dall’agente',
    '<b>Airtable:</b> lettura della rubrica.<br/><b>Gmail:</b> invio del messaggio richiesto.<br/>'
    '<b>Google Calendar:</b> creazione dell’evento.<br/>Sono collegamenti tool, non passaggi eseguiti sempre.',10.8)
box(418,215,376,116,'Risposta e contesto',
    'Telegram Send riporta l’esito nella chat d’origine. Il modello GPT-4o mini interpreta la richiesta; '
    'Window Buffer Memory mantiene il contesto recente separato per chat. Fuso: <b>Europe/Rome</b>.',11)
txt('Schema descrittivo del workflow. Nel video sono mostrate le aperture reali di ciascuno dei 14 nodi.',48,76,size=10,color=MUTED)
c.showPage()

page(3,'I 14 nodi','Funzione e motivo di ogni passaggio',
     'I nomi corrispondono a quelli mostrati nell’editor n8n e nella registrazione.')
rows=[['#','Nodo','Funzione e scelta progettuale'],
['01','Telegram Trigger','Riceve gli eventi message; è l’ingresso unico della conversazione.'],
['02','Solo Stefano','Filtra ID e tipo della chat prima di modello e strumenti.'],
['03','Switch','Instrada testo, note vocali e formati non supportati.'],
['04','Get Voice File','Scarica il file audio a partire dal file_id Telegram.'],
['05','OpenAI','Trascrive il contenuto binario audio in testo utilizzabile dall’agente.'],
['06','Normalizza input','Unifica testo e trascrizione; respinge input vuoto o oltre 12.000 caratteri.'],
['07','Formato non supportato','Chiede testo o voce senza coinvolgere il modello linguistico.'],
['08','AI Agent','Interpreta, applica le istruzioni e decide quali tool chiamare; massimo 8 iterazioni.'],
['09','OpenAI Chat Model','Fornisce GPT-4o mini per interpretazione e chiamate agli strumenti.'],
['10','Window Buffer Memory','Contesto recente per chat, con finestra impostata a 10.'],
['11','rubrica contatti','Legge Airtable per ricavare gli indirizzi associati ai nomi.'],
['12','invio email','Invia con Gmail destinatario, oggetto e corpo compilati dall’agente.'],
['13','calendario','Crea titolo, descrizione, inizio, fine ed eventuali invitati richiesti.'],
['14','Telegram Send','Invia l’output alla chat iniziale, con escape HTML e limite di lunghezza.']]
table(rows,433,[39,174,533],10.2,5)
c.showPage()

page(4,'Istruzioni e controllo','Il system prompt guida le decisioni',
     'Le regole linguistiche orientano il modello; i controlli in codice hanno un ruolo distinto.')
rows=[['Regola','Motivazione e comportamento previsto'],
['Contatto verificato nel turno corrente','Prima di ogni invio o evento, rileggere la rubrica anche se il contatto è in memoria. Usare solo indirizzi trovati; chiedere chiarimenti per nomi assenti o ambigui.'],
['Bozza, invio ed evento distinti','Una bozza non autorizza l’invio. L’agente può inviare o creare soltanto su richiesta esplicita; per eventi personali non aggiunge invitati non richiesti.'],
['Date e dati mancanti','Data corrente fornita da n8n, fuso Europe/Rome e offset ISO 8601. Oggetto, destinatario e orario mancanti richiedono chiarimenti; durata predefinita 60 minuti.'],
['Conferme dopo il tool','Confermare l’azione soltanto dopo il successo dello strumento. Segnalare i fallimenti e non ripetere automaticamente un invio con esito incerto.'],
['Dati esterni e risposta','Note della rubrica e messaggi sono dati, non istruzioni sostitutive. Rispondere in italiano, testo semplice, entro 3.000 caratteri.']]
y=table(rows,433,[188,558],11,7)
txt('<b>Correzione guidata dalle prove.</b> Nell’esecuzione 4 il destinatario era corretto, ma proveniva dalla memoria. '
    'Il prompt è stato rafforzato; nelle esecuzioni 10 e 11 è stata osservata una nuova chiamata Airtable prima di Gmail e Calendar.',48,y-17,size=11.5)
txt('<b>Limite:</b> il prompt non rende deterministici i tool. Il filtro della chat e la validazione dell’input sono invece '
    'controlli eseguiti in codice prima dell’agente.',48,101,size=10.8,color=MUTED)
c.showPage()

page(5,'Configurazione','Parametri, memoria e portabilità',
     'Le integrazioni sono collegate nell’istanza cloud; l’export consegnabile esclude le credenziali.')
rows=[['Componente','Configurazione rilevante','Perché conta'],
['Input','input_text + chat_id; massimo 12.000 caratteri','Testo e voce raggiungono lo stesso prompt con un formato coerente.'],
['Memoria','Chiave s2i:<chat_id>; finestra 10','Separa le conversazioni e permette richieste successive; non è archivio permanente.'],
['Gmail','To, Subject e Message tramite $fromAI','La rubrica determina l’indirizzo; la richiesta fornisce contenuto e oggetto.'],
['Calendar','Start/End ISO 8601; Summary/Description; Attendees','La data deve comprendere l’offset corretto. Una lista vuota evita invitati nella demo.'],
['Tempo','Data corrente con $now nel fuso Europe/Rome','Il modello riceve un riferimento esplicito per interpretare domani e altre date relative.'],
['Risposta','Prompt: 3.000 caratteri; invio: taglio a 3.900 ed escape HTML','Riduce problemi di formato; gli asterischi Markdown possono comunque restare visibili.']]
y=table(rows,433,[106,280,360],10.6,7)
txt('<b>Autenticazione.</b> Telegram usa Bot API; Airtable, Gmail e Calendar usano OAuth. Chat e trascrizione '
    'utilizzano i Gateway credits n8n disponibili nell’account.',48,y-17,size=11)
txt('<b>Nuova installazione.</b> Importare workflow.json inattivo, collegare le proprie credenziali, impostare l’ID '
    'della chat privata, base/tabella Airtable e calendario. Pubblicare dopo la verifica. Non sostituire con l’export '
    'portabile l’istanza personale già configurata.',48,104,size=10.7,color=MUTED)
c.showPage()

page(6,'Prova reale 10 / email','Dalla richiesta alla casella del destinatario',
     'Registrazione dell’8 ottobre 2026. Destinatario di prova: Contatto Prova S2I, presente in Airtable.')
box(48,435,746,84,'Richiesta in Telegram',
    'Inviare una sola email sul progetto start2impact con l’appuntamento del 9 ottobre, 16:00-16:30, '
    'fuso Europe/Rome. Per ora inviare soltanto l’email, senza creare eventi.',11)
shot('evidenze/email_ricevuta_2026-10-08.png',48,344,746,214,crop=(0,0,1736,570))
txt('<b>Sequenza osservata:</b> Airtable (indice 7) &gt; Gmail (indice 9) &gt; risposta Telegram. '
    'Esecuzione 10: <b>success</b>, 17:53:51-17:54:00 Europe/Rome. Ricezione verificata in Outlook alle 17:54.',48,123,size=11.3)
txt('Oggetto: “Demo Agenti AI - appuntamento 9 ottobre”. Una chiamata Gmail; nessuna creazione Calendar. '
    'Il corpo contiene il footer automatico n8n. Schermata reale ritagliata al messaggio.',48,78,size=9.7,color=MUTED)
c.showPage()

page(7,'Prova reale 11 / calendario','Lo stesso appuntamento nel calendario',
     'Seconda richiesta nella stessa chat: un evento personale, senza invitati e senza altre email.')
shot('evidenze/evento_calendario_2026-10-08.png',48,433,746,262,crop=(275,0,1715,660))
txt('<b>Titolo:</b> Demo Agenti AI - appuntamento.<br/><b>Quando:</b> 9 ottobre 2026, 16:00-16:30 Europe/Rome '
    '(UTC+02:00). L’interfaccia mostra 4:00-4:30 PM.<br/><b>Verifica:</b> rubrica prima di Calendar; '
    'evento creato una sola volta, senza invitati né invio di un’altra email.',48,152,size=11.6)
txt('Esecuzione 11: success, 17:55:18-17:55:26 Europe/Rome. Descrizione e orario corrispondono '
    'all’appuntamento comunicato nell’email. Conferma tramite output del tool e interfaccia Google Calendar.',48,80,size=9.7,color=MUTED)
c.showPage()

page(8,'Validazione','Undici esecuzioni, riscontri distinti',
     'Il successo tecnico del workflow viene confrontato con azioni, risultati e regole richieste.')
rows=[['ID','Caso','Risultato osservato'],
['1-2','Avvio e contatto','Risposta Telegram e indirizzo letto da Airtable.'],
['3','Bozza testuale','Bozza in chat; nessuna email o creazione evento.'],
['4','Invio e memoria','Email ricevuta; contatto riusato dalla memoria, poi prompt corretto.'],
['5','Evento personale','Rubrica prima di Calendar; 8 ottobre, 15:00-15:30, nessun invitato.'],
['6','Nota vocale','Trascrizione e bozza; nessun invio o evento.'],
['7-8','Contatto / orario assenti','Assenza segnalata o domanda di chiarimento; nessuna azione.'],
['9','Sticker','Fallback senza chiamata al modello.'],
['10','Email nella demo','Nuova lettura Airtable, una email ricevuta e mostrata in Outlook.'],
['11','Calendario nella demo','Nuova lettura Airtable, evento del 9 ottobre mostrato nel calendario.']]
y=table(rows,433,[48,158,540],10.6,5.5)
txt('<b>Totale osservato:</b> 11 esecuzioni con stato n8n success, 2 email ricevute e 2 eventi personali. '
    'Le due nuove operazioni della demo sono distinte dalle prove storiche del 7 ottobre.',48,y-17,size=11.5)
txt('<b>Controlli locali:</b> 12 verifiche con n8n 2.37.0 su schema e collegamenti, testo/voce, input vuoti o eccessivi, '
    'date, array invitati, escape Telegram, filtro chat ed export senza credenziali. Non sostituiscono i test cloud.',48,105,size=10.8,color=MUTED)
c.showPage()

page(9,'Comprensione e limiti','Cosa è dimostrato, cosa resta da estendere',
     'Il progetto documenta il comportamento osservato senza generalizzarlo a tutti i possibili input.')
shot('evidenze/telegram_prova_voce_2026-10-07.png',48,430,296,310)
txt('Esecuzione 6: nota vocale e bozza restituita.<br/>Trascrizione di 12 secondi di audio; nessun invio.',48,106,width=296,size=10,color=MUTED)
box(365,433,429,104,'Scelte dimostrate',
    'Ingresso testo/voce, contesto recente, rubrica, invio email e creazione evento funzionano nei casi provati. '
    'La verifica comprende messaggi ricevuti e calendario, oltre allo stato delle esecuzioni.',11.2)
box(365,313,429,109,'Limiti osservati',
    'Il prompt è probabilistico. La memoria non garantisce persistenza permanente. Alcune risposte conservano '
    'asterischi Markdown; la prima email storica era nello spam. L’operatività dipende da servizi, crediti e credenziali.',11.2)
box(365,188,429,111,'Estensioni da validare',
    'Omonimi, guasti dei servizi, inviti a terzi e operazioni concorrenti non sono stati provati online. '
    'Possibili sviluppi: validazione deterministica prima dei tool, protezione dai duplicati e suite di regressione '
    'su richieste variate. Non sono funzionalità già implementate.',10.9)
c.showPage()

page(10,'Video e materiali','La dimostrazione completa in 2 minuti e 30',
     'Riprese reali dei nodi e delle azioni; attese tagliate, avatar personale e voce generati con HeyGen.')
shot('evidenze/video_finale_loom_2026-10-08.png',48,431,414,269,crop=(20,110,1280,865))
link('GUARDA IL VIDEO SU LOOM',args.video_url,487,428,307,15)
txt('Durata misurata: <b>150,135 secondi</b>.<br/>Full HD, 1920 x 1080, 30 fps.<br/>'
    'Riproduzione verificata anche senza login.<br/><br/>Il video mostra ogni nodo, la richiesta Telegram, '
    'l’email ricevuta e l’evento nel calendario. La natura sintetica del presentatore è dichiarata a schermo.',487,389,307,11.5)
txt(escape(args.video_url),487,229,307,9,color=MUTED)
txt('<b>Materiali del progetto</b>',48,159,size=12.5)
txt('workflow.json: export portabile. GUIDA_SETUP.md: configurazione. RELAZIONE.md e CONFORMITA.md: '
    'documentazione. evidenze/: registri e schermate. video/heygen/: copione, tre segmenti avatar e script di montaggio.',48,137,size=10.7)
txt('<b>Fonti della verifica:</b> consegna ufficiale start2impact acquisita il 7 ottobre; workflow.json; '
    'evidenze/test_workflow.json; prove_reali.json (esecuzioni 1-9); demo_video_2026-10-08.json (10-11). '
    'Video e PDF preparati per la consegna; nessun invio alla piattaforma effettuato.',48,94,size=9.8,color=MUTED)
c.save()
print(DEST)
