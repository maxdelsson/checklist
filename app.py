import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lista de Chequeo - Multimedia San Felipe", layout="centered")

st.title("📋 Lista de Chequeo en Vivo")
st.markdown("### **Área:** Multimedia San Felipe | **Coordinador:** Esposos Graterol")
st.write("---")

# Inicializar los datos en la sesión para que persistan los cambios mientras está abierto
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "NRO": [1, 2, 3, 4],
        "DETALLE DE LA ACTIVIDAD": [
            "AYUNO SABADO",
            "SERVIDORES SONIDO AYUNO",
            "SERVIDORES STAFF AYUNO",
            "SERVIDORES SEGURIDAD AYUNO"
        ],
        "STATUS": ["EN PROCESO", "LISTO", "NO SE EJECUTO", "EN PROCESO"],
        "OBSERVACION": ["", "", "Faltó personal", ""]
    })

# Formulario interactivo para cambiar estatus fácilmente
st.subheader("⚙️ Actualizar Actividades")

for idx, row in st.session_state.df.iterrows():
    col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        st.markdown(f"**{row['NRO']}. {row['DETALLE DE LA ACTIVIDAD']}**")
    
    with col2:
        nuevo_status = st.selectbox(
            f"Status {idx}", 
            ["LISTO", "EN PROCESO", "NO SE EJECUTO"], 
            index=["LISTO", "EN PROCESO", "NO SE EJECUTO"].index(row['STATUS']),
            key=f"status_{idx}",
            label_visibility="collapsed"
        )
        st.session_state.df.at[idx, 'STATUS'] = nuevo_status
        
    with col3:
        nueva_obs = st.text_input(
            f"Obs {idx}", 
            value=row['OBSERVACION'], 
            key=f"obs_{idx}",
            placeholder="Observación...",
            label_visibility="collapsed"
        )
        st.session_state.df.at[idx, 'OBSERVACION'] = nueva_obs

st.write("---")
st.subheader("👁️ Vista General (Lo que ve la Pastora)")

# Función de diseño para pintar filas enteras según el estatus
def resaltar_fila(row):
    if row['STATUS'] == 'LISTO':
        return ['color: green; text-decoration: line-through; font-weight: bold;'] * len(row)
    elif row['STATUS'] == 'EN PROCESO':
        return ['color: #d4ac0d; font-weight: bold;'] * len(row)
    elif row['STATUS'] == 'NO SE EJECUTO':
        return ['color: red; font-weight: bold;'] * len(row)
    return [''] * len(row)

# Mostrar la tabla estilizada
tabla_estilizada = st.session_state.df.style.apply(resaltar_fila, axis=1)
st.dataframe(tabla_estilizada, use_container_width=True)