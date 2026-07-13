import streamlit as st

# Configurazione della pagina (Layout largo per ospitare 4 colonne)
st.set_page_config(page_title="Acquisizione Dati APE", layout="wide")

st.title("Acquisizione Dati per APE")
st.markdown("Modulo di raccolta dati per redazione Attestato di Prestazione Energetica.")

with st.form("ape_form"):
    # ==========================================
    # 1. DATI GENERALI E PROPRIETARIO
    # ==========================================
    st.header("1. Dati Generali e Proprietario")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        data_sopralluogo = st.date_input("Data sopralluogo")
        motivazione = st.selectbox("Motivazione", ["Vendita", "Affitto", "Altro"])
        destinazione_uso = st.text_input("Destinazione Uso")
    
    with c2:
        nome_prop = st.text_input("Nome Proprietario")
        cognome_prop = st.text_input("Cognome Proprietario")
        
    with c3:
        residenza_prop = st.text_input("Residenza (Comune)")
        cap_prop = st.text_input("CAP")
        
    with c4:
        via_prop = st.text_input("Via/Piazza (Proprietario)")
        num_prop = st.text_input("N. (Proprietario)")

    st.markdown("---")

    # ==========================================
    # 2. IMMOBILE E CONFINANTI
    # ==========================================
    st.header("2. Immobile")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        comune_imm = st.text_input("Comune Immobile")
        via_imm = st.text_input("Via/Piazza Immobile")
        num_imm = st.text_input("N. Immobile")
    
    with c2:
        foglio = st.text_input("Foglio")
        mappale = st.text_input("Mappale (mn)")
        sub = st.text_input("Sub")
        
    with c3:
        anno_costr = st.text_input("Anno Costruzione")
        anno_imp = st.text_input("Anno Impianti")
        valore_imm = st.text_input("Valore (k€)")
        
    with c4:
        n_unita = st.text_input("N. Unità edificio")
        piano_ingr = st.text_input("Piano di ingresso")
        n_piani = st.text_input("N. Piani totali")

    st.subheader("Destinazione d'uso dei confinanti")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        conf_sopra = st.selectbox("Sopra", ["Abitazione", "Sottotetto", "Cielo", "Altro", "Non specificato"])
        conf_sotto = st.selectbox("Sotto", ["Abitazione", "Garage", "Terreno", "Altro", "Non specificato"])
    with c2:
        conf_nord = st.text_input("A fianco Nord")
    with c3:
        conf_sud = st.text_input("A fianco Sud")
        conf_est = st.text_input("A fianco Est")
    with c4:
        conf_ovest = st.text_input("A fianco Ovest")

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
        vetro = st.selectbox("Vetro (Tipologia)", ["Singolo", "Doppio", "Triplo", "Basso emissivo", "Non specificato"])
        
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
    st.header("4. Impianti (Centrali Termiche / Stufe)")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        caldaia_tipo = st.selectbox("Caldaia", ["Standard", "A condensazione", "Non presente"])
        caldaia_marca = st.text_input("Marca Caldaia")
        caldaia_modello = st.text_input("Modello Caldaia")
        caldaia_anno = st.text_input("Anno Caldaia")
        
    with c2:
        alim_caldaia = st.selectbox("Alimentazione", ["Metano", "GPL", "Gasolio", "Altro", "Non specificato"])
        ubicazione_caldaia = st.selectbox("Ubicazione", ["Interno", "Esterno", "Centrale Termica"])
        terminali = st.selectbox("Terminali", ["Radiatori acciaio", "Radiatori ghisa", "Radiatori alluminio", "A pavimento", "A soffitto", "Altro"])
        
    with c3:
        sistema_tipo = st.multiselect("Tipo Sistema (Caldaia)", ["Risc.", "ACS"])
        n_termostati = st.text_input("N. Termostati")
        manutentore = st.text_input("Manutentore")
        contatto_manut = st.text_input("Contatto Manutentore")

    with c4:
        st.markdown("**Eventuale Stufa**")
        stufa_tipo = st.selectbox("Tipo Stufa", ["Nessuna", "Legna", "Pellet"])
        stufa_marca = st.text_input("Marca / Modello Stufa")
        stufa_anno = st.text_input("Anno Stufa")
        stufa_sistema = st.multiselect("Tipo Sistema (Stufa)", ["Risc.", "ACS"])

    # Codice CIRCE e Chiave su una sola riga
    st.subheader("Registrazione Impianto")
    cc1, cc2, cc3, cc4 = st.columns(4)
    with cc1:
        codice_circe = st.text_input("Codice CIRCE")
    with cc2:
        chiave_circe = st.text_input("Chiave")

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

    # Pulsante di salvataggio
    submitted = st.form_submit_button("Genera Riepilogo per Copia-Incolla")

# ==========================================
# GENERAZIONE RIEPILOGO (DOPO IL SUBMIT)
# ==========================================
if submitted:
    st.success("Dati compilati con successo! Copia il blocco sottostante.")
    
    # Costruzione stringa di riepilogo
    riepilogo = f"""
### 1. DATI GENERALI E PROPRIETARIO
- Data: {data_sopralluogo}
- Motivazione: {motivazione} | Destinazione Uso: {destinazione_uso}
- Proprietario: {nome_prop} {cognome_prop}
- Residenza: {via_prop} {num_prop}, {cap_prop} {residenza_prop}

### 2. IMMOBILE E CONFINANTI
- Ubicazione Immobile: {via_imm} {num_imm}, {comune_imm}
- Dati Catastali: Foglio {foglio}, Mappale {mappale}, Sub {sub}
- Anni / Valore: Costruzione {anno_costr}, Impianti {anno_imp}, Valore {valore_imm}k€
- Geometria: N. Unità {n_unita}, Piano ingresso {piano_ingr}, N. Piani {n_piani}
- Confinanti:
  Sopra: {conf_sopra} | Sotto: {conf_sotto}
  Nord: {conf_nord} | Sud: {conf_sud} | Est: {conf_est} | Ovest: {conf_ovest}

### 3. STRUTTURE E INVOLUCRO
- Muratura EXT: {muro_ext} (Spessore: {spessore_muro} cm)
- Solai: Sopra -> {solaio_sopra} | Sotto -> {solaio_sotto}
- Serramenti: {serramento}, Telaio {telaio}, Vetro {vetro}
- Oscuramento: {oscuramento} (Materiale: {mat_osc})
- Dettagli: Nicchie sottofinestra: {nicchie} | Cassonetti: {cassonetti}

### 4. IMPIANTI
- Caldaia: {caldaia_tipo} | Marca: {caldaia_marca} | Modello: {caldaia_modello} | Anno: {caldaia_anno}
- Impianto: {alim_caldaia} | Ubicazione: {ubicazione_caldaia} | Terminali: {terminali}
- Gestione: Sistema {sistema_tipo}, N. Termostati: {n_termostati}
- Stufa: {stufa_tipo} ({stufa_marca} - {stufa_anno}) - Sistema: {stufa_sistema}
- Codice CIRCE: {codice_circe} | Chiave: {chiave_circe}
- Manutentore: {manutentore} | Contatto: {contatto_manut}

### 5. NOTE
{note}
    """
    
    st.code(riepilogo, language="markdown")
