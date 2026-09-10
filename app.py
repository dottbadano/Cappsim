# 2. Scansione Automatica Cartelle con Percorso Assoluto
def discover_cases():
    cases = []
    # Ottiene la cartella esatta in cui si trova app.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    casi_dir = os.path.join(base_dir, "casi")
    
    if not os.path.exists(casi_dir):
        st.error(f"❌ ERRORE: La cartella 'casi' non esiste in: {base_dir}")
        return cases
    
    subfolders = os.listdir(casi_dir)
    
    for folder_name in subfolders:
        folder_path = os.path.join(casi_dir, folder_name)
        
        if os.path.isdir(folder_path):
            scenario_path = os.path.join(folder_path, "scenario.json")
            
            if os.path.exists(scenario_path):
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
                    except Exception as e:
                        st.error(f"⚠️ Errore di lettura nel file `{scenario_path}`: {e}")
            else:
                # Mostra quali cartelle dentro 'casi' non hanno il file json
                st.info(f"ℹ️ La cartella `{folder_name}` non contiene un file `scenario.json`.")
                
    return sorted(cases, key=lambda x: x["id"])
