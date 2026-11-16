import streamlit as st
import os
import sys

# Aggiunge il path corrente per individuare i moduli
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from text import UI_STRINGS
except ImportError:
    UI_STRINGS = {"landing_subtitle": "Simulazione Clinica Multidisciplinare 2gether"}

st.set_page_config(
    page_title="2getSIM — Corso 2gether",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inizializzazione Session State
if "station_name" not in st.session_state:
    st.session_state.station_name = ""
if "current_case_key" not in st.session_state:
    st.session_state.current_case_key = None
if "current_node_id" not in st.session_state:
    st.session_state.current_node_id = "start"
if "vitalita" not in st.session_state:
    st.session_state.vitalita = 100
if "oncologico" not in st.session_state:
    st.session_state.oncologico = 100
if "qol" not in st.session_state:
    st.session_state.qol = 75
if "history" not in st.session_state:
    st.session_state.history = []

def load_clinical_cases():
    """
    Carica dinamicamente tutti i moduli .py all'interno della cartella 'casi_clinici'.
    Ogni file deve esporre un dizionario strutturato CASE_DATA.
    """
    cases = {}
    cases_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "casi_clinici")
    
    if os.path.exists(cases_dir):
        for fname in os.listdir(cases_dir):
            if fname.endswith(".py") and not fname.startswith("__"):
                mod_name = fname[:-3]
                try:
                    mod = __import__(f"casi_clinici.{mod_name}", fromlist=["CASE_DATA"])
                    if hasattr(mod, "CASE_DATA"):
                        cases[mod_name] = mod.CASE_DATA
                except Exception as e:
                    st.error(f"Errore nel caricamento del caso clinico {mod_name}: {e}")
                    
    return cases

def main():
    st.sidebar.title("2getSIM • Control Room")
    st.sidebar.markdown("---")
    
    # Caricamento dinamico dei casi dalla cartella
    cases = load_clinical_cases()
    
    if not cases:
        st.error("Nessun caso clinico trovato nella cartella 'casi_clinici/'. Aggiungi almeno un file .py con CASE_DATA.")
        return

    # Seleziona il caso corrente se non impostato
    if st.session_state.current_case_key not in cases:
        st.session_state.current_case_key = list(cases.keys())[0]

    # Schermata di configurazione postazione (Landing)
    if not st.session_state.station_name:
        st.title("Configurazione Postazione Tablet")
        st.markdown("Inserisci l'identificativo del partecipante o del centro ospedaliero per accedere alla simulazione.")
        
        with st.form("landing_form"):
            station_input = st.text_input("Identificativo Partecipante / Centro Ospedaliero", placeholder="Es. Centro 1 / Dr. Rossi")
            
            case_keys = list(cases.keys())
            case_labels = [cases[k].get("title", k) for k in case_keys]
            selected_case_label = st.selectbox("Seleziona Caso Clinico", case_labels)
            
            submitted = st.form_submit_button("Avvia Simulazione Clinica →")
            
            if submitted:
                if station_input:
                    st.session_state.station_name = station_input
                    for k, v in cases.items():
                        if v.get("title") == selected_case_label:
                            st.session_state.current_case_key = k
                            break
                    # Reset stato clinico del caso
                    active_case = cases[st.session_state.current_case_key]
                    st.session_state.current_node_id = active_case.get("start_node", "start")
                    st.session_state.vitalita = 100
                    st.session_state.oncologico = 100
                    st.session_state.qol = 75
                    st.session_state.history = []
                    st.rerun()
                else:
                    st.error("Inserisci un identificativo postazione valido.")
        return

    # Sidebar Postazione e Indicatori Live
    st.sidebar.success(f"Postazione: {st.session_state.station_name}")
    if st.sidebar.button("↺ Cambia Postazione / Caso"):
        st.session_state.station_name = ""
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("Indicatori Clinici Live")
    st.sidebar.progress(st.session_state.vitalita / 100, text=f"Vitalità Paziente: {st.session_state.vitalita}%")
    st.sidebar.progress(st.session_state.oncologico / 100, text=f"Controllo Oncologico: {st.session_state.oncologico}%")
    st.sidebar.progress(st.session_state.qol / 100, text=f"Qualità di Vita (QoL): {st.session_state.qol}%")

    # Recupero dati del caso e del nodo corrente
    active_case = cases.get(st.session_state.current_case_key, {})
    nodes = active_case.get("nodes", {})
    node_data = nodes.get(st.session_state.current_node_id, None)

    if not node_data:
        st.error(f"Errore: Nodo clinico '{st.session_state.current_node_id}' non trovato nel caso.")
        if st.button("Torna all'inizio del caso"):
            st.session_state.current_node_id = active_case.get("start_node", "start")
            st.rerun()
        return

    # UI Principale della Simulazione
    st.title(active_case.get("title", "Simulazione Clinica"))
    st.markdown(f"### {node_data.get('step_label', 'SNODO CLINICO')}")
    st.subheader(node_data.get("title", ""))
    st.write(node_data.get("clinical_text", ""))

    if node_data.get("labs"):
        st.info(f"**Esami / Reperti:** {node_data['labs']}")

    # Se il nodo è terminale (Fine caso)
    if node_data.get("is_end", False):
        st.balloons()
        if st.button("Riavvia il Caso dall'Inizio"):
            st.session_state.current_node_id = active_case.get("start_node", "start")
            st.session_state.vitalita = 100
            st.session_state.oncologico = 100
            st.session_state.qol = 75
            st.session_state.history = []
            st.rerun()
        return

    st.markdown("---")
    st.markdown("#### Scegli la strategia clinica (Scelta secca One-Shot):")
    
    for opt in node_data.get("options", []):
        btn_label = f"Opzione {opt['letter']}: {opt['text']}"
        if st.button(btn_label, key=f"btn_{opt['letter']}_{st.session_state.current_node_id}"):
            st.session_state.history.append(f"[{node_data['step_label']}] {opt['text']}")
            st.session_state.vitalita = max(0, min(100, st.session_state.vitalita + opt.get("delta_vit", 0)))
            st.session_state.oncologico = max(0, min(100, st.session_state.oncologico + opt.get("delta_onc", 0)))
            st.session_state.qol = max(0, min(100, st.session_state.qol + opt.get("delta_qol", 0)))
            st.session_state.current_node_id = opt["next"]
            st.rerun()

    if st.session_state.history:
        with st.expander("Tracciato storico delle decisioni"):
            for h in st.session_state.history:
                st.write(f"- {h}")

if __name__ == "__main__":
    main()
