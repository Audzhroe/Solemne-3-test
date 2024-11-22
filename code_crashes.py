import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Análisis Inteligente de Accidentes",
    layout="wide",
    page_icon="🚗"
)

# Encabezado principal
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
    <h1 class="main-title">🚗 Análisis de Accidentes 🚗</h1>
    <p class="description">Explora los datos, filtra por años y genera gráficos interactivos.</p>
""", unsafe_allow_html=True)

# Barra lateral para configuración
with st.sidebar:
    st.markdown('<p class="sidebar-text">📂 Sube tu archivo CSV:</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Sube tu archivo aquí", type=["csv"])

    st.markdown('<p class="sidebar-text">🎨 Tema de los gráficos:</p>', unsafe_allow_html=True)
    theme = st.radio("Selecciona un tema:", ["Colores Simples", "Colores más tenues", "Colores sólidos"])

    st.markdown("---")

# Verificar si se subió un archivo
if uploaded_file:
    try:
        # Leer el archivo CSV
        data = pd.read_csv(uploaded_file)
        st.success(f"Archivo cargado exitosamente: **{uploaded_file.name}**")

        # Verificar si hay una columna de años
        year_column = None
        for col in data.columns:
            if pd.api.types.is_numeric_dtype(data[col]) and "año" in col.lower():
                year_column = col
                break

        # Aplicar filtro por años si existe una columna válida
        if year_column:
            min_year, max_year = int(data[year_column].min()), int(data[year_column].max())
            with st.sidebar:
                selected_years = st.slider(
                    "Selecciona el rango de años:",
                    min_value=min_year,
                    max_value=max_year,
                    value=(min_year, max_year),
                    step=1
                )
            # Filtrar los datos
            data = data[(data[year_column] >= selected_years[0]) & (data[year_column] <= selected_years[1])]
            st.info(f"Datos filtrados para los años: {selected_years[0]} - {selected_years[1]}")

        # Mostrar una vista previa de los datos
        st.markdown("### 👀 Vista previa de los datos:")
        st.dataframe(data.head(16))

        # Seleccionar tipo de gráfico
        st.header("📊 Generación de Gráficos")
        chart_type = st.selectbox("Selecciona el tipo de gráfico:", 
                                  ["Barras", "Histograma", "Líneas", "Dispersión", "Torta"])

        # Obtener columnas disponibles
        columns = data.columns.tolist()

        # Selección de ejes
        x_axis = st.selectbox("Selecciona el eje X:", columns, help="Eje base del gráfico")
        if chart_type != "Torta":
            y_axis = st.selectbox("Selecciona el eje Y:", [col for col in columns if col != x_axis], help="Eje dependiente del gráfico")

        # Configuración de color y título
        with st.expander("🔧 Opciones avanzadas"):
            color_col = st.selectbox("Columna para color (opcional):", ["Ninguno"] + columns)
            if color_col == "Ninguno":
                color_col = None
            title = st.text_input("Título del gráfico:", value=f"Gráfico de {chart_type}")

        # Generar gráfico
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

            # Aplicar tema
            if theme == "Colores más tenues":
                fig.update_layout(template="seaborn")
            elif theme == "Colores sólidos":
                fig.update_layout(template="simple_white")
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
else:
    st.warning("Por favor, sube un archivo CSV para comenzar.")
    st.image(
        "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDQ5OXB5d3QyZHh6ZzhlcnpzcjlmeTV1dTZyYTZxdHFoOTQ1bzIxNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/wr7oA0rSjnWuiLJOY5/giphy-downsized.gif",
        width=250, caption="Esperando datos...")

# Pie de página
st.markdown("---")
st.markdown("""
    <style>
    .footer {
        text-align: center;
        font-size: 14px;
        color: #888;
    }
    </style>
    <p class="footer">🚀 Creado por estudiantes de la USS</p>
""", unsafe_allow_html=True)
