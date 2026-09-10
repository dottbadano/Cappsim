import streamlit as st
import json
import os
import re

# Configurazione Pagina
st.set_page_config(page_title="Cappsim Engine", layout="wide", initial_sidebar_state="collapsed")

# Styling personalizzato (Sfondo nero, pulsanti con bordo rosso granata e testo giallo ocra)
st.markdown("""
<style>
    .stApp {
        background-color: #000000;
    }
    div[data-testid="stColumn"] button {
        width: 100%;
        height: 75px;
        font-size: 17px !important;
        font-weight: 600;
        border-radius: 12px;
        border: 2px solid #6B1226;
        background-color: #000000;
        color: #D4AF37;
        text-align: left;
        padding-left: 20px;
    }
    div[data-testid="stColumn"] button:hover, 
    div[data-testid="stColumn"] button:focus,
    div[data-testid="stColumn"] button:active {
        color: #FFFFFF !important;
        border-color: #FFFFFF !important;
        background-color: #1A0505 !important;
    }
    .question-box {
        background-color: #121212;
        padding: 22px;
        border-radius: 10px;
        border-left: 6px solid #6B1226;
        margin-bottom: 25px;
        font-size: 20px;
        color: #FFFFFF;
    }
    .feedback-box {
        background-color: #112233;
        padding: 18px;
        border-radius: 10px;
        border-left: 6px solid #00E676;
        margin-bottom: 25px;
        font-size: 17px;
        color: #E0E0E0;
    }
</style>
""", unsafe_allow_html=True)

# 1. Mappatura Categorie per Range Numerico
CATEGORIES = {
    (1, 99): "🩸 Vescica",
    (100, 199): "🎯 Prostata",
    (200, 299): "🧬 Rene",
    (300, 399): "🌊 Alta Via Urinaria",
    (400, 499): "⚾ Testicolo"
}

def get_category_by_id(case_id):
    for (start, end), label in CATEGORIES.items():
        if start <= case_id <= end:
            return label
    return "📁 Altri Casi Clinici"

# 2. Scansione Automatica Cartelle con Percorso Assoluto
def discover_cases():
    cases = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    casi_dir = os.path.join(base_dir, "casi")
    
    if not os.path.exists(casi_dir):
        return cases
    
    for folder_name in os.listdir(casi_dir):
        folder_path = os.path.join(casi_dir, folder_name)
        scenario_path = os.path.join(folder_path, "scenario.json")
        
        if os.path.isdir(folder_path) and os.path.exists(scenario_path):
            case_num = None
            if folder_name.isdigit():
                case_num = int(folder_name)
            else:
                match = re.match(r"^(\d+)", folder_name)
                if match:
                    case_num = int(match.group(1))
            
            if case_num is not None:
                category = get_category_by_id(case_num)
                try:
                    with open(scenario_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    cases.append({
                        "id": case_num,
                        "folder": folder_name,
                        "title": data.get("titolo", f"Caso #{case_num:03d}"),
                        "category": category,
                        "path": scenario_path
                    })
                except Exception:
                    pass
    return sorted(cases, key=lambda x: x["id"])

# 3. Caricamento Scenario
def load_scenario(scenario_path):
    with open(scenario_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Session State
if "active_case" not in st.session_state:
    st.session_state.active_case = None

# ==============================================================================
# MENU ACCESSO CASI
# ==============================================================================
if st.session_state.active_case is None:
    st.title("🩺 CAPPSIM — Seleziona Caso Clinico")
    st.caption("Piattaforma di Simulazione Decisionale Urologica")
    st.divider()

    available_cases = discover_cases()

    if not available_cases:
        st.warning("⚠️ Nessun caso clinico trovato nella cartella `casi/`. Assicurati di aver inserito `scenario.json` dentro la cartella del caso (es: `casi/001/scenario.json`).")
    else:
        categorized = {}
        for c in available_cases:
            categorized.setdefault(c["category"], []).append(c)

        selected_cat = st.selectbox("📌 Seleziona Distretto Urologico:", list(categorized.keys()))

        st.subheader(f"Casi Disponibili in {selected_cat}")
        for c in categorized[selected_cat]:
            col_info, col_btn = st.columns([3, 1])
            with col_info:
                st.markdown(f"**Caso #{c['id']:03d}:** {c['title']}")
            with col_btn:
                if st.button("AVVIA SIMULAZIONE ➔", key=f"start_{c['id']}"):
                    st.session_state.scenario = load_scenario(c["path"])
                    st.session_state.active_case = c["id"]
                    st.session_state.current_node_id = st.session_state.scenario["nodo_iniziale"]
                    st.session_state.selected_option = None
                    st.session_state.last_feedback = None
                    st.rerun()

# ==============================================================================
# MOTORE SIMULATORE
# ==============================================================================
else:
    scenario = st.session_state.scenario
    node = scenario["nodi"][st.session_state.current_node_id]

    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        st.title("🩺 CAPPSIM — Simulator")
        st.caption(f"Caso #{st.session_state.active_case:03d}: **{scenario['titolo']}**")
    with top_col2:
        if st.button("🚪 Esci al Menu"):
            st.session_state.active_case = None
            st.rerun()

    st.divider()

    if st.session_state.last_feedback:
        st.markdown(f"""
        <div class="feedback-box">
            {st.session_state.last_feedback}
        </div>
        """, unsafe_allow_html=True)

    st.subheader(f"📍 {node.get('titolo_fase', 'Quadro Clinico')}")
    with st.expander("📋 CONSULTA REFERTI E QUADRO CLINICO", expanded=True):
        t1, t2, t3 = st.tabs(["Anamnesi", "Esame Obiettivo", "Esami Ematici / Imaging"])
        with t1:
            st.write(node["quadro_clinico"].get("anamnesi", "Nessun dato."))
        with t2:
            st.write(node["quadro_clinico"].get("esame_obiettivo", "Nessun dato."))
        with t3:
            if "esami_ematici" in node["quadro_clinico"]:
                st.table(node["quadro_clinico"]["esami_ematici"])

    st.markdown("<br>", unsafe_allow_html=True)

    if node.get("is_epilogo", False):
        st.error(f"🛑 {node['domanda']}")
        st.success("Simulazione conclusa per questo percorso.")
        col_end1, col_end2 = st.columns(2)
        with col_end1:
            if st.button("🔄 Riavvia questo Caso", type="primary", use_container_width=True):
                st.session_state.current_node_id = scenario["nodo_iniziale"]
                st.session_state.selected_option = None
                st.session_state.last_feedback = None
                st.rerun()
        with col_end2:
            if st.button("📋 Torna al Menu Casi", use_container_width=True):
                st.session_state.active_case = None
                st.rerun()

    else:
        st.markdown(f"""
        <div class="question-box">
            ❓ <b>QUESITO CLINICO:</b><br>{node['domanda']}
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        labels = ["A", "B", "C", "D"]

        for idx, opt in enumerate(node["opzioni"]):
            target_col = col1 if idx % 2 == 0 else col2
            with target_col:
                is_selected = (st.session_state.selected_option is not None) and (st.session_state.selected_option["id"] == opt["id"])
                label_text = f"{'▶ ' if is_selected else ''}{labels[idx]}: {opt['testo']}"
                if st.button(label_text, key=f"opt_{opt['id']}"):
                    st.session_state.selected_option = opt
                    st.rerun()

        if st.session_state.selected_option:
            st.divider()
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                if st.button("PROCEDI ➔", type="primary", use_container_width=True):
                    st.session_state.last_feedback = st.session_state.selected_option.get("feedback", "")
                    st.session_state.current_node_id = st.session_state.selected_option["prossimo_nodo"]
                    st.session_state.selected_option = None
                    st.rerun()
