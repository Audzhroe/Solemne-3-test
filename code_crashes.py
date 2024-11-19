import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Análisis Inteligente de Accidentes",
    layout="wide",
    page_icon="🚗"
)

# Encabezado principal con imagen
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #FF4B4B;
        font-size: 50px;
        font-weight: bold;
    }
    .description {
        text-align: center;
        color: #4F4F4F;
        font-size: 20px;
    }
    .sidebar-text {
        color: #FF4B4B;
        font-weight: bold;
    }
    </style>
    <h1 class="main-title">🚗 Análisis Inteligente de Accidentes 🚗</h1>
    <p class="description">Explora datos de accidentes y crea gráficos interactivos.</p>
""", unsafe_allow_html=True)

st.image("https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif", width=700, caption="Madruga carajo")

# Cargar datos desde la barra lateral
with st.sidebar:
    st.markdown('<p class="sidebar-text">📂 Sube tu archivo CSV:</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Sube tu archivo de accidentes aquí:", type=["csv"])
    
    st.markdown('<p class="sidebar-text">🎨 Tema de gráficos:</p>', unsafe_allow_html=True)
    theme = st.radio("Selecciona un tema:", ["Plotly", "Seaborn", "Simple"])
    
    st.markdown("---")
    

# Si hay un archivo subido
if uploaded_file:
    try:
        # Leer el archivo CSV
        data = pd.read_csv(uploaded_file)
        st.success(f"Archivo cargado exitosamente: **{uploaded_file.name}**")
        
        # Mostrar una tabla resumen
        st.markdown("### 👀 Vista previa de los datos:")
        st.dataframe(data.head())

        # Opciones de gráficos
        st.header("📊 Gráficos Inteligentes")
        chart_type = st.selectbox("Selecciona el tipo de gráfico:", 
                                  ["Barras", "Histograma", "Líneas", "Dispersión", "Torta"])

        columns = data.columns.tolist()
        column_types = data.dtypes.apply(lambda x: x.name).to_dict()

        # Selección del eje X
        x_axis = st.selectbox("Selecciona el eje X:", columns, help="Eje base del gráfico")
        
        # Validación dinámica de columnas para el eje Y
        if chart_type in ["Líneas", "Dispersión"]:
            # Gráficos continuos: Solo columnas numéricas
            valid_y_columns = [col for col, dtype in column_types.items() if dtype in ["int64", "float64"]]
        elif chart_type == "Torta":
            # Gráficos de torta: Solo columnas categóricas
            valid_y_columns = [col for col, dtype in column_types.items() if dtype == "object"]
        else:
            # Otros gráficos: Cualquier columna excepto el eje X
            valid_y_columns = [col for col in columns if col != x_axis]

        if chart_type != "Torta":
            y_axis = st.selectbox("Selecciona el eje Y:", valid_y_columns, help="Eje dependiente del gráfico")

        # Validar si hay columnas disponibles
        if chart_type != "Torta" and not valid_y_columns:
            st.error("No hay columnas válidas para el eje Y con la selección actual.")
        else:
            # Opciones avanzadas
            with st.expander("🔧 Opciones avanzadas"):
                color_col = st.selectbox("Columna para color (opcional):", ["Ninguno"] + columns)
                if color_col == "Ninguno":
                    color_col = None
                title = st.text_input("Título del gráfico:", value=f"Gráfico de {chart_type}")

            # Botón para generar el gráfico
            if st.button("Generar Gráfico"):
                if chart_type == "Barras":
                    fig = px.bar(data, x=x_axis, y=y_axis, color=color_col, title=title)
                elif chart_type == "Histograma":
                    fig = px.histogram(data, x=x_axis, color=color_col, title=title)
                elif chart_type == "Líneas":
                    fig = px.line(data, x=x_axis, y=y_axis, color=color_col, title=title)
                elif chart_type == "Dispersión":
                    fig = px.scatter(data, x=x_axis, y=y_axis, color=color_col, title=title)
                elif chart_type == "Torta":
                    fig = px.pie(data, names=x_axis, title=title)

                # Aplicar tema seleccionado
                if theme == "Seaborn":
                    fig.update_layout(template="seaborn")
                elif theme == "Simple":
                    fig.update_layout(template="simple_white")
                st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
else:
    st.warning("Por favor, sube un archivo CSV para comenzar.")
    st.image("https://giphy.com/gifs/cat-meme-wilfrosty-mr-fresh-wr7oA0rSjnWuiLJOY5", caption="Esperando datos...")

# Footer
st.markdown("---")
st.markdown("""
    <style>
    .footer {
        text-align: center;
        font-size: 14px;
        color: #888;
    }
    </style>
    <p class="footer">🚀 pongale bueno</p>
""", unsafe_allow_html=True)
