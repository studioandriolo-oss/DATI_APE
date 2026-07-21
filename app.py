import streamlit as st
import smtplib
import ssl
import mimetypes
from email.message import EmailMessage
from fpdf import FPDF # <-- NUOVO IMPORT

# ==========================================
# FUNZIONE CREAZIONE PDF
# ==========================================
def genera_pdf(testo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=11)
    
    # Puliamo eventuali caratteri markdown se presenti
    testo_pulito = testo.replace("**", "")
    
    # Alcuni caratteri speciali (come l'Euro) possono dare fastidio al font base di FPDF
    testo_pulito = testo_pulito.replace("€", "EUR")
    
    pdf.multi_cell(0, 6, text=testo_pulito)
    
    #convertiamo esplicitamente l'output in 'bytes' per Streamlit
    return bytes(pdf.output())

# ==========================================
# 1. SISTEMA DI LOGIN MULTI-UTENTE
# ==========================================
if "agente_loggato" not in st.session_state:
    st.session_state.agente_loggato = None

if not st.session_state.agente_loggato:
    st.title("🔒 Accesso Riservato")
    st.markdown("Inserisci le tue credenziali per accedere al modulo APE.")
    
    # Campi di input
    id_inserito = st.text_input("ID Agente")
    pwd_inserita = st.text_input("Password", type="password")
    
    if st.button("Accedi", type="primary"):
        # Controlliamo se l'ID esiste nei secrets e se la password combacia
        agenti = st.secrets["agenti"]
        if id_inserito in agenti and agenti[id_inserito] == pwd_inserita:
            # Salviamo il nome in memoria
            st.session_state.agente_loggato = id_inserito
            st.rerun() # Ricarica sbloccando la pagina
        else:
            st.error("Credenziali errate. Riprova.")
            
    st.stop() # Blocca l'esecuzione del resto del codice se non sei loggato

# ==========================================
# 2. SE L'ACCESSO E' ESEGUITO, MOSTRA LA PAGINA
# ==========================================
st.set_page_config(page_title="Acquisizione Dati APE", layout="wide")

col_titolo, col_agente = st.columns([3, 1])

with col_titolo:
    st.title("Acquisizione Dati per APE")
    st.markdown("Modulo di raccolta dati per redazione Attestato di Prestazione Energetica.")

with col_agente:
    st.markdown("<br>", unsafe_allow_html=True)
    # Mostriamo il nome in sola lettura
    st.info(f"👤 Agente: **{st.session_state.agente_loggato}**")
    
    # Tasto di logout
    if st.button("Esci / Logout", use_container_width=True):
        st.session_state.agente_loggato = None
        st.rerun() # Riavvia l'app e riporta alla schermata di login
    
    # Assegniamo la variabile per il riepilogo
    nome_agente = st.session_state.agente_loggato

# ==========================================
# FUNZIONE INVIO EMAIL
# ==========================================
def invia_email_studio(riepilogo, nome_agente, nome_proprietario, file_singoli, file_foto):
    email_studio = "studioandriolo@gmail.com"
    password_studio = st.secrets["mail_password"]
    
    msg = EmailMessage()
    msg.set_content(riepilogo)
    msg['Subject'] = f"APE {nome_agente} | {nome_proprietario}"
    msg['From'] = email_studio
    msg['To'] = email_studio

    # Combiniamo tutti i file caricati (scartando quelli vuoti)
    tutti_i_file = [f for f in file_singoli if f is not None]
    if file_foto:
        tutti_i_file.extend(file_foto)

    # Alleghiamo i file all'email
    for f in tutti_i_file:
        file_data = f.read()
        file_name = f.name
        
        mime_type, _ = mimetypes.guess_type(file_name)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        maintype, subtype = mime_type.split('/', 1)
        
        msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)
        f.seek(0)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_studio, password_studio)
        server.send_message(msg)

# ==========================================
# 1. DATI GENERALI E PROPRIETARIO
# ==========================================
st.header("1. Dati Generali e Proprietario")
c1, c2, c3, c4 = st.columns(4)

with c1:
    data_sopralluogo = st.text_input("Data sopralluogo")
    motivazione = st.selectbox("Motivazione", ["Vendita", "Affitto", "Altro"])
    destinazione_uso = st.text_input("Destinazione Uso")

with c2:
    nome_prop = st.text_input("Nome Proprietario")
    cognome_prop = st.text_input("Cognome Proprietario")
    cf_prop = st.text_input("Codice Fiscale")
    
with c3:
    data_nascita = st.text_input("Data di nascita (gg/mm/aaaa)")
    luogo_nascita = st.text_input("Luogo di nascita")
        
with c4:
    residenza_prop = st.text_input("Residenza (Comune)")
    cap_prop = st.text_input("CAP")
    via_prop = st.text_input("Via/Piazza (Proprietario)")
    num_prop = st.text_input("Civico (Proprietario)")

st.markdown("---")

# ==========================================
# 2. IMMOBILE E CONFINANTI
# ==========================================
st.header("2. Immobile")
c1, c2, c3, c4 = st.columns(4)

with c1:
    comune_imm = st.text_input("Comune Immobile")
    via_imm = st.text_input("Via/Piazza Immobile")
    num_imm = st.text_input("Civico Immobile")
    valore_imm = st.text_input("Valore (k€) - solo a fini statistici")

with c2:
    foglio = st.text_input("Foglio")
    mappale = st.text_input("Mappale (mn)")
    sub = st.text_input("Sub")
    
with c3:
    anno_costr = st.text_input("Anno Costruzione")
    anno_imp = st.text_input("Anno Impianti")
    
with c4:
    n_unita = st.text_input("N. Unità edificio")
    piano_ingr = st.text_input("Piano di ingresso")
    n_piani = st.text_input("N. Piani totali")

st.subheader("Destinazione d'uso dei confinanti")
c1, c2, c3, c4 = st.columns(4)
with c1:
    conf_sopra = st.selectbox("Sopra", ["Abitazione", "Sottotetto", "Cielo", "Altro", "Non specificato"])
with c2:
    conf_sotto = st.selectbox("Sotto", ["Abitazione", "Garage", "Terreno", "Altro", "Non specificato"])

st.markdown("---")

# ==========================================
# 3. STRUTTURE (INVOLUCRO)
# ==========================================
st.header("3. Involucro e Serramenti")
c1, c2, c3, c4 = st.columns(4)

with c1:
    muro_ext = st.text_input("Muratura EXT (descrizione)")
    spessore_muro = st.text_input("Spessore Muratura (cm)")
    solaio_sopra = st.text_input("Solaio Sopra (descrizione)")
    solaio_sotto = st.text_input("Solaio Sotto (descrizione)")
    
with c2:
    serramento = st.selectbox("Serramento", ["Singolo", "Doppio", "Triplo", "Non specificato"])
    telaio = st.selectbox("Telaio", ["Legno", "PVC", "Metallo", "Taglio termico", "Non specificato"])
    vetro = st.selectbox("Vetro (Tipologia)", ["Singolo", "Doppio", "Triplo", "Non specificato"])
    
with c3:
    oscuramento = st.selectbox("Oscuramento", ["Tapparelle", "Balconi/Scuri", "Tende oscuranti", "Lamelle orientabili", "Nessuno"])
    mat_osc = st.selectbox("Materiale Oscuramento", ["PVC", "Legno", "Alluminio", "Altro", "Non specificato"])
    
with c4:
    nicchie = st.radio("Ci sono nicchie sottofinestra?", ["SI", "NO"], horizontal=True)
    cassonetti = st.radio("Ci sono cassonetti (avvolgibili)?", ["SI", "NO"], horizontal=True)

st.markdown("---")

# ==========================================
# 4. IMPIANTI E CENTRALI TERMICHE
# ==========================================
st.header("4. Impianti")

st.subheader("Registrazione Impianto")
cc1, cc2, cc3, cc4 = st.columns(4)
with cc1:
    codice_circe = st.text_input("Codice CIRCE")
with cc2:
    chiave_circe = st.text_input("Chiave")
with cc3:
    manutentore = st.text_input("Manutentore")
with cc4:
    contatto_manut = st.text_input("Contatto Manutentore")

st.subheader("Impianto Principale")
cc1, cc2, cc3 = st.columns(3)

with cc1:
    caldaia_tipo = st.selectbox("Caldaia", ["Standard", "A condensazione", "Non lo so", "Non presente"])
    caldaia_marca = st.text_input("Marca Caldaia")
    caldaia_modello = st.text_input("Modello Caldaia")
    
with cc2:
    alim_caldaia = st.selectbox("Alimentazione", ["Metano", "GPL", "Gasolio", "Altro", "Non specificato"])
    ubicazione_caldaia = st.selectbox("Ubicazione", ["Interno", "Esterno", "Centrale Termica"])
    terminali = st.selectbox("Terminali", ["Radiatori acciaio", "Radiatori ghisa", "Radiatori alluminio", "A pavimento", "A soffitto", "Altro"])
    
with cc3:
    sistema_tipo = st.multiselect("Tipo Sistema (Caldaia)", ["Risc.", "ACS"])
    n_termostati = st.text_input("N. Termostati")
    caldaia_anno = st.text_input("Anno Caldaia")

# ==========================================
# ALTRI IMPIANTI (A SCOMPARSA)
# ==========================================
st.subheader("Altri impianti (seleziona se presenti)")

t1, t2, t3 = st.columns(3)
with t1:
    mostra_fotovoltaico = st.toggle("Fotovoltaico presente")
with t2:
    mostra_stufa = st.toggle("Stufa a legna/pellet presente")
with t3:
    mostra_PDC = st.toggle("Pompa di Calore/Climatizzatore presente")

fotovoltaico, esposizione = "", ""
stufa_tipo, stufa_marca, stufa_anno, stufa_sistema = "Nessuna", "", "", []

if mostra_fotovoltaico or mostra_stufa:
    cc1, cc2, cc3 = st.columns(3)
    
    with cc1:
        if mostra_fotovoltaico:
            st.markdown("**Impianto Fotovoltaico**")
            fotovoltaico = st.text_input("Potenza impianto fotovoltaico (kW)")
            esposizione = st.selectbox("Esposizione", ["Sud", "Est", "Ovest", "Non lo so"])
            
    with cc2:
        if mostra_stufa:
            st.markdown("**Stufa**")
            stufa_tipo = st.selectbox("Tipo Stufa", ["Nessuna", "Legna", "Pellet"])
            stufa_marca = st.text_input("Marca / Modello Stufa")
            
    with cc3:
        if mostra_stufa:
            st.markdown("**Dettagli Stufa**")
            stufa_anno = st.text_input("Anno Stufa")
            stufa_sistema = st.multiselect("Tipo Sistema (Stufa)", ["Risc.", "ACS"])
    
if mostra_PDC:
    st.markdown("**Pompa di Calore/Climatizzatore**")
    cc1, cc2, cc3 = st.columns(3)
    with cc1:            
            PDC_riscaldamento = st.text_input("Potenza riscaldamento COP")
    with cc2:
            PDC_raffrescamento = st.text_input("Potenza raffrescamento EER")
    with cc3:
            PDC_elementi_radianti = st.selectbox("Elementi radianti", ["Split", "Consolle/Mobiletti ad aria", "Consolle/Mobiletti ad acqua", "Fancoil"])
            
st.markdown("---")

# ==========================================
# 5. NOTE E UPLOAD DOCUMENTI
# ==========================================
st.header("5. Note e Documentazione")

note = st.text_area("Note aggiuntive (inserisci qui qualsiasi altra informazione utile)", height=150)

st.subheader("Caricamento File")
c1, c2, c3 = st.columns(3)
with c1:
    file_visura = st.file_uploader("Carica Visura Catastale (PDF/Img)")
    file_planimetria = st.file_uploader("Carica Planimetria Catastale (PDF/Img)")
with c2:
    file_doc_identita = st.file_uploader("Carica Documento Identità")
    file_libretti = st.file_uploader("Carica Libretti Impianto / Accesso Atti")
with c3:
    file_foto = st.file_uploader("Carica Fotografie (Dall'esterno, Serramenti, Caldaia, Termostato, Radiatori)", accept_multiple_files=True)

# ---------------------------------------------------------
# PRENOTIAMO LO SPAZIO PER I BOTTONI
# ---------------------------------------------------------
spazio_bottoni = st.container()

# Inseriamo il toggle, che apparirà VISIVAMENTE sotto lo spazio dei bottoni
st.markdown("---")
col_testo_toggle, col_bottone_toggle = st.columns([4, 1])

with col_testo_toggle:
    st.subheader("FATTURARE DIRETTAMENTE AL CLIENTE")
    
with col_bottone_toggle:
    # Aggiungiamo un piccolo margine invisibile per allineare l'interruttore al testo grande
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    
    # Creiamo il toggle nascondendo la sua etichetta standard (che ora è il subheader a sinistra)
    fatt_cliente = st.toggle("Attiva", label_visibility="collapsed")

# ==========================================
# PREPARAZIONE DATI (Riepilogo) E PULSANTI
# ==========================================
st.markdown("", unsafe_allow_html=True)

# 1. Compiliamo il testo in automatico per passarlo al PDF e alla mail
txt_foto = f"- Fotovoltaico: Potenza {fotovoltaico} - Esposizione: {esposizione}" if mostra_fotovoltaico else "- Fotovoltaico: Non presente"
txt_stufa = f"- Stufa: {stufa_tipo} - {stufa_marca} - Anno {stufa_anno} - Sistema: {', '.join(stufa_sistema)}" if mostra_stufa else "- Stufa: Non presente"
txt_pompa_di_calore = f"- PDC: COP {PDC_riscaldamento} - EER {PDC_raffrescamento} - Elementi Radianti: {PDC_elementi_radianti}" if mostra_PDC else "- PDC: Non presente"
txt_fattura = "SI" if fatt_cliente else "NO"

# Ho rimosso gli '###' per far uscire il PDF più pulito e formattato come un vero modulo
riepilogo = f"""
1. DATI GENERALI E PROPRIETARIO
- Agente incaricato: {nome_agente}
- Data sopralluogo: {data_sopralluogo}
- Motivazione: {motivazione} | Destinazione Uso: {destinazione_uso}
- Proprietario: {nome_prop} {cognome_prop} (CF: {cf_prop})
- Nato a: {luogo_nascita} | Il: {data_nascita}
- Residenza: {via_prop} {num_prop}, {cap_prop} {residenza_prop}

2. IMMOBILE E CONFINANTI
- Ubicazione Immobile: {via_imm} {num_imm}, {comune_imm}
- Dati Catastali: Foglio {foglio}, Mappale {mappale}, Sub {sub}
- Anni / Valore: Costruzione {anno_costr}, Impianti {anno_imp}, Valore {valore_imm}
- Geometria: N. Unità {n_unita}, Piano ingresso {piano_ingr}, N. Piani {n_piani}
- Confinanti: Sopra: {conf_sopra} | Sotto: {conf_sotto}

3. STRUTTURE E INVOLUCRO
- Muratura EXT: {muro_ext} (Spessore: {spessore_muro} cm)
- Solai: Sopra -> {solaio_sopra} | Sotto -> {solaio_sotto}
- Serramenti: {serramento}, Telaio {telaio}, Vetro {vetro}
- Oscuramento: {oscuramento} (Materiale: {mat_osc})
- Dettagli: Nicchie sottofinestra: {nicchie} | Cassonetti: {cassonetti}

4. IMPIANTI
- Codice CIRCE: {codice_circe} | Chiave: {chiave_circe}
- Manutentore: {manutentore} | Contatto: {contatto_manut}
- Caldaia: {caldaia_tipo} | Marca/Modello: {caldaia_marca} {caldaia_modello} | Anno: {caldaia_anno}
- Impianto: {alim_caldaia} | Ubicazione: {ubicazione_caldaia} | Terminali: {terminali}
- Gestione: Sistema {', '.join(sistema_tipo)}, N. Termostati: {n_termostati}

ALTRI IMPIANTI
{txt_foto}
{txt_stufa}
{txt_pompa_di_calore}

5. NOTE
{note}

6.FATTURA CLIENTE
Fatturare direttamente al cliente: {txt_fattura}
"""

# ---------------------------------------------------------
# INSERIAMO I BOTTONI NELLO SPAZIO PRENOTATO IN ALTO
# ---------------------------------------------------------
with spazio_bottoni:
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_vuota = st.columns([2, 2, 6])
    
    with col_btn1:
        # Generiamo il PDF in background
        pdf_bytes = genera_pdf(riepilogo)
    
        # Download button (scarica il file automaticamente senza mostrare il testo a schermo)
        st.download_button(
            label="📄 Scarica PDF Riepilogo",
            data=pdf_bytes,
            file_name=f"APE_{cognome_prop}_{nome_agente}.pdf",
            mime="application/pdf"
            )

    with col_btn2:
        inviato = st.button("Invia al professionista", type="primary")

# 3. Logica per l'invio mail
if inviato:
    with st.spinner("Compilazione email e caricamento allegati in corso..."):
        try:
            nome_completo_prop = f"{nome_prop} {cognome_prop}".strip()
            file_singoli = [file_visura, file_planimetria, file_doc_identita, file_libretti]
            
            invia_email_studio(riepilogo, nome_agente, nome_completo_prop, file_singoli, file_foto)
            
            st.success("🚀 Dati e allegati inviati con successo allo studio!")
        except Exception as e:
            st.error(f"Si è verificato un errore durante l'invio dell'email: {e}")
            st.info("Assicurati di aver inserito `mail_password` nei Secrets di Streamlit.")

st.markdown("---")

# ==========================================
# PIANO COMMERCIALE E SCONTISTICA
# ==========================================
st.header("Piano Commerciale per unità fino a 200 mq")
st.subheader("💰 Riservato agli agenti")
st.markdown(" Iva inclusa - Fatturazione annuale")
    
with st.info("📉 **Scontistica applicata per scaglioni di pratiche inviate:**"):
        st.markdown("""
        | Scaglione | Prezzo Unitario | Totale Pacchetto |
        | :--- | :---: | :---: |
        | **Da 1 a 7 APE** | 100,00 € | 700,00 € |
        | **Da 8 a 14 APE** | 80,00 € | 1.260,00 € |
        | **Da 15 a 28 APE** | 65,00 € | 2.170,00 € |
        | **Da 29 a 56 APE** | 55,00 € | 3.710,00 € |
        """)
        
# Un tocco visivo in più usando le metriche native di Streamlit
c1, c2, c3, c4 = st.columns(4)
c1.metric(label="Fino a 7 APE", value="100 €/cad")
c2.metric(label="Fino a 14 APE", value="80 €/cad", delta="-20% sul pacchetto", delta_color="normal")
c3.metric(label="Fino a 28 APE", value="65 €/cad", delta="-35% sul pacchetto", delta_color="normal")
c4.metric(label="Fino a 56 APE", value="55 €/cad", delta="-45% sul pacchetto", delta_color="normal")

st.markdown("Per unità superiori a 200mq verrà comunicato preventivo specifico.")

st.markdown("---")
st.subheader("💰 Direttamente al cliente, se richiesto: fatturazione a prezzo fisso 150 euro iva inclusa!")

