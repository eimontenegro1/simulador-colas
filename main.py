import streamlit as st
import random
from fifo_queue import FIFOQueue
from pq_queue import PQQueue
from wfq_queue import WFQQueue
from cbwfq_queue import CBWFQQueue

# Diccionario colores con etiquetas en español e inglés y color hex
priority_colors = {
    0: {"etiqueta_es": "Alta prioridad", "etiqueta_en": "High priority", "color": "#e63946"},  # Rojo
    1: {"etiqueta_es": "Media prioridad", "etiqueta_en": "Medium priority", "color": "#f1fa8c"}, # Amarillo
    2: {"etiqueta_es": "Baja prioridad", "etiqueta_en": "Low priority", "color": "#2a9d8f"},    # Verde
    3: {"etiqueta_es": "Sin prioridad", "etiqueta_en": "No priority", "color": "#a8dadc"}       # Celeste
}

def generar_paquetes(n):
    paquetes = []
    for i in range(n):
        prioridad = random.randint(0, 3)
        data = priority_colors[prioridad]
        paquetes.append({
            "id": i + 1,
            "prioridad": prioridad,
            "etiqueta_es": data["etiqueta_es"],
            "etiqueta_en": data["etiqueta_en"],
            "color": data["color"]
        })
    return paquetes

def mostrar_paquetes_tabla(paquetes, titulo, icono, idioma):
    st.subheader(f"{icono} {titulo}")
    if not paquetes:
        st.write("No hay paquetes para mostrar." if idioma=="es" else "No packets to show.")
        return

    html_table = "<table style='width:100%; border-collapse: collapse;'>"
    html_table += "<thead><tr>"
    headers = ["ID", "Prioridad (Num)", "Etiqueta", "Color"] if idioma=="es" else ["ID", "Priority (Num)", "Label", "Color"]
    for col in headers:
        html_table += f"<th style='border:1px solid #ddd; padding:8px; background-color:#023047; color:white; text-align:center;'>{col}</th>"
    html_table += "</tr></thead><tbody>"
    for p in paquetes:
        etiqueta = p["etiqueta_es"] if idioma == "es" else p["etiqueta_en"]
        html_table += (
            f"<tr style='background-color:#f9f9f9;'>"
            f"<td style='border:1px solid #ddd; padding:8px; text-align:center; color:#000000;'>Paquete {p['id']}</td>"
            f"<td style='border:1px solid #ddd; padding:8px; text-align:center; color:#000000;'>{p['prioridad']}</td>"
            f"<td style='border:1px solid #ddd; padding:8px; text-align:center; color:#000000;'>{etiqueta}</td>"
            f"<td style='border:1px solid #ddd; padding:8px; text-align:center;'>"
            f"<div style='width:25px; height:25px; background-color:{p['color']}; margin:auto; border-radius:6px;' title='{etiqueta}'></div>"
            f"</td>"
            f"</tr>"
        )
    html_table += "</tbody></table>"
    st.markdown(html_table, unsafe_allow_html=True)

def mostrar_comparacion_tabla(paquetes_orig, paquetes_proc, idioma):
    st.subheader("🔄 " + ("Comparación con Paquetes Originales" if idioma=="es" else "Comparison with Original Packets"))
    if not paquetes_orig or not paquetes_proc:
        st.write("No hay datos para comparar." if idioma=="es" else "No data to compare.")
        return

    # Diccionario para búsqueda rápida de paquetes procesados por id
    proc_dict = {p['id']: p for p in paquetes_proc}

    html_table = "<table style='width:100%; border-collapse: collapse;'>"
    if idioma=="es":
        headers = [
            "ID Original", "Prioridad Original", "Etiqueta Original", "Color Original",
            "→",
            "ID Procesado", "Prioridad Procesado", "Etiqueta Procesado", "Color Procesado"
        ]
    else:
        headers = [
            "Original ID", "Original Priority", "Original Label", "Original Color",
            "→",
            "Processed ID", "Processed Priority", "Processed Label", "Processed Color"
        ]

    html_table += "<thead><tr>"
    for col in headers:
        style = "background-color:#023047; color:white; text-align:center; border:1px solid #ddd; padding:8px;"
        html_table += f"<th style='{style}'>{col}</th>"
    html_table += "</tr></thead><tbody>"

    for o in paquetes_orig:
        p = proc_dict.get(o['id'], None)
        if p is None:
            continue  # o mostrar vacío si quieres
        etiqueta_o = o["etiqueta_es"] if idioma=="es" else o["etiqueta_en"]
        etiqueta_p = p["etiqueta_es"] if idioma=="es" else p["etiqueta_en"]

        html_table += (
            "<tr style='background-color:#f9f9f9; color:#000;'>"
            f"<td style='border:1px solid #ddd; padding:8px; text-align:center;'>Paquete {o['id']}</td>"
            f"<td style='border:1px solid #ddd; padding:8px; text-align:center;'>{o['prioridad']}</td>"
            f"<td style='border:1px solid #ddd; padding:8px; text-align:center;'>{etiqueta_o}</td>"
            f"<td style='border:1px solid #ddd; padding:8px; text-align:center;'>"
            f"<div style='width:20px; height:20px; background-color:{o['color']}; margin:auto; border-radius:6px;' title='{etiqueta_o}'></div>"
            f"</td>"
            f"<td style='border:none; text-align:center; font-weight:bold;'>→</td>"
            f"<td style='border:1px solid #ddd; padding:8px; text-align:center;'>Paquete {p['id']}</td>"
            f"<td style='border:1px solid #ddd; padding:8px; text-align:center;'>{p['prioridad']}</td>"
            f"<td style='border:1px solid #ddd; padding:8px; text-align:center;'>{etiqueta_p}</td>"
            f"<td style='border:1px solid #ddd; padding:8px; text-align:center;'>"
            f"<div style='width:20px; height:20px; background-color:{p['color']}; margin:auto; border-radius:6px;' title='{etiqueta_p}'></div>"
            f"</td>"
            "</tr>"
        )

    html_table += "</tbody></table>"
    st.markdown(html_table, unsafe_allow_html=True)

# Configuración página
st.set_page_config(page_title="Simulador de Algoritmos de Encolamiento", layout="wide")

# Selector de idioma
idioma = st.sidebar.selectbox("Idioma / Language", ["Español", "English"])
es = (idioma == "Español")

# Textos para interfaz según idioma
title_text = "📊 Simulador de Algoritmos de Encolamiento" if es else "📊 Queueing Algorithms Simulator"
instructions_text = (
    "- Elige la cantidad de paquetes que quieres generar.\n"
    "- Presiona **Generar paquetes** para crear una lista aleatoria con prioridades.\n"
    "- Selecciona el algoritmo de encolamiento.\n"
    "- Presiona **Procesar paquetes** para ver cómo se envían y reciben.\n"
    "- Los colores indican la prioridad de cada paquete (rojo = alta, amarillo = media, verde = baja, celeste = sin prioridad)."
) if es else (
    "- Choose how many packets you want to generate.\n"
    "- Press **Generate packets** to create a random list with priorities.\n"
    "- Select the queueing algorithm.\n"
    "- Press **Process packets** to see how they are sent and received.\n"
    "- Colors indicate packet priority (red = high, yellow = medium, green = low, light blue = no priority)."
)

st.title(title_text)

# Nombre destacado y enlace al inicio
st.markdown(
    """
    <p style='font-size:22px; font-weight:bold; text-align:center; color:#1d4ed8;'>
        Desarrollado por 
        <a href='https://www.linkedin.com/in/edwin-montenegro-aguilar' target='_blank' style='color:#1d4ed8; text-decoration:none;'>
            Edwin Montenegro Aguilar
        </a>
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

with st.expander("ℹ️ " + ("Instrucciones de Uso" if es else "Instructions"), expanded=True):
    st.markdown(instructions_text)

# --- Sidebar ---
with st.sidebar:
    st.header("Configuración" if es else "Settings")

    num_paquetes = st.number_input("Número de paquetes a generar" if es else "Number of packets to generate", min_value=1, max_value=1000, value=10, step=1)
    generar = st.button("Generar paquetes" if es else "Generate packets")

    st.markdown("---")
    algoritmo = st.selectbox("Selecciona algoritmo de encolamiento" if es else "Select queueing algorithm", ["FIFO", "PQ", "WFQ", "CB-WFQ"])
    procesar = st.button("Procesar paquetes" if es else "Process packets")

# --- Estado y lógica ---
if generar:
    st.session_state["paquetes"] = generar_paquetes(num_paquetes)
    st.success(f"Se generaron {num_paquetes} paquetes." if es else f"{num_paquetes} packets generated.")

if "paquetes" not in st.session_state:
    st.info("Primero genera paquetes en el panel lateral para empezar." if es else "First generate packets in the sidebar to start.")
    paquetes = []
else:
    paquetes = st.session_state["paquetes"]

# --- Layout principal ---
col1, col2 = st.columns([1, 1])

with col1:
    mostrar_paquetes_tabla(paquetes, titulo="Paquetes Generados" if es else "Generated Packets", icono="📦", idioma="es" if es else "en")

with col2:
    if not paquetes:
        st.warning("No hay paquetes generados para procesar." if es else "No packets generated to process.")
    else:
        if procesar:
            if algoritmo == "FIFO":
                cola = FIFOQueue()
            elif algoritmo == "PQ":
                cola = PQQueue()
            elif algoritmo == "WFQ":
                cola = WFQQueue()
            elif algoritmo == "CB-WFQ":
                cola = CBWFQQueue()
            else:
                cola = FIFOQueue()

            for p in paquetes:
                cola.enqueue(p)

            paquetes_procesados = cola.process()

            mostrar_paquetes_tabla(paquetes_procesados, titulo="📤 Paquetes Enviados" if es else "Sent Packets", icono="✅", idioma="es" if es else "en")

            st.markdown("---")
            st.subheader("⚙️ Procesamiento realizado" if es else "⚙️ Processing done")
            st.success(f"{'Total paquetes procesados' if es else 'Total packets processed'}: {len(paquetes_procesados)}")

            st.markdown("---")
            mostrar_paquetes_tabla(paquetes_procesados, titulo="📥 Paquetes Recibidos" if es else "Received Packets", icono="📥", idioma="es" if es else "en")

            st.markdown("---")
            mostrar_comparacion_tabla(paquetes, paquetes_procesados, idioma="es" if es else "en")

        else:
            st.info("Selecciona el algoritmo y haz clic en **Procesar paquetes** para ver resultados." if es else "Select algorithm and click **Process packets** to see results.")


