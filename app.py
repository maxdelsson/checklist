import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Lista de Chequeo en Vivo", page_icon="📋", layout="centered"
)

st.markdown(
    """
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #2C3E50; margin-bottom: 0px; }
    .sub-header { font-size: 16px; color: #7F8C8D; margin-bottom: 20px; }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="main-title">📋 Lista de Chequeo en Vivo</p>',
    unsafe_allow_html=True,
)

# Sección de configuración general configurable
col_area, col_coord = st.columns(2)
with col_area:
    area_nombre = st.text_input("Área / Departamento", "Multimedia San Felipe")
with col_coord:
    coord_nombre = st.text_input("Coordinador(es)", "Esposos Graterol")

st.markdown(
    f'<p class="sub-header">Área: {area_nombre} | Coordinador: {coord_nombre}</p>',
    unsafe_allow_html=True,
)
st.markdown("---")

# Inicializar las actividades en la sesión para poder agregarlas/editarlas dinámicamente
if "df_actividades" not in st.session_state:
    st.session_state.df_actividades = pd.DataFrame(
        {
            "NRO": [1, 2],
            "DETALLE DE LA ACTIVIDAD": [
                "Revisión de equipos de sonido",
                "Prueba de cámaras y transmisión",
            ],
            "STATUS": ["EN PROCESO", "LISTO"],
            "OBSERVACION": ["", "Todo en orden"],
        }
    )

st.markdown("### ⚙️ Administrar y Actualizar Actividades")

# Formulario para agregar una nueva actividad
with st.expander("➕ Agregar nueva actividad a la lista"):
    with st.form("nueva_actividad_form"):
        nuevo_detalle = st.text_input("Detalle de la Actividad")
        nuevo_status = st.selectbox(
            "Status Inicial", ["EN PROCESO", "LISTO", "NO SE EJECUTO"]
        )
         nueva_obs = st.text_input("Observación (Opcional)")
        submit_agregar = st.form_submit_button("Agregar Actividad")

        if submit_agregar and nuevo_detalle:
            nuevo_nro = (
                len(st.session_state.df_actividades) + 1
            )
            nueva_fila = pd.DataFrame(
                {
                    "NRO": [nuevo_nro],
                    "DETALLE DE LA ACTIVIDAD": [nuevo_detalle],
                    "STATUS": [nuevo_status],
                    "OBSERVACION": [nueva_obs],
                }
            )
            st.session_state.df_actividades = pd.concat(
                [st.session_state.df_actividades, nueva_fila], ignore_index=True
            )
            st.success("¡Actividad agregada con éxito!")
            st.rerun()

st.markdown("#### Edición rápida de registros actuales:")

# Editor de datos interactivo para modificar status, observaciones o textos sobre la marcha
edited_df = st.data_editor(
    st.session_state.df_actividades,
    num_rows="dynamic",
    use_container_width=True,
    key="editor_actividades",
)

# Actualizar el estado de la sesión con lo editado
st.session_state.df_actividades = edited_df

st.markdown("---")
st.markdown("### 👁️ Vista General de Control")


# Función para colorear las celdas según el status
def color_status(val):
    if val == "LISTO":
        return "color: #27AE60; font-weight: bold;"
    elif val == "EN PROCESO":
        return "color: #D4AC0D; font-weight: bold;"
    elif val == "NO SE EJECUTO":
        return "color: #C0392B; font-weight: bold;"
    return ""


# Mostrar la tabla limpia y presentable
st.dataframe(
    st.session_state.df_actividades.style.applymap(
        color_status, subset=["STATUS"]
    ),
    use_container_width=True,
)
