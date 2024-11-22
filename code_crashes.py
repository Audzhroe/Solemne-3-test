import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Análisis Inteligente de Accidentes de Autos",
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
    <h1 class="main-title">🚗 Análisis de Accidentes de Autos 🚗</h1>
    <p class="description">Explora los datos de accidentes de vehículos de manera interactiva y fácil.</p>
""", unsafe_allow_html=True)

# Barra lateral con instrucciones y carga de archivo
with st.sidebar:
    st.markdown('<p class="sidebar-text">📂 Sube tu archivo CSV:</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Sube un archivo CSV con datos de accidentes:", type=["csv"])

    st.markdown("---")
    st.markdown("<p><b>Instrucciones:</b></p>", unsafe_allow_html=True)
    st.markdown("""
        1. Carga un archivo CSV con información sobre accidentes de autos.
        2. Utiliza los filtros para seleccionar el rango de fechas, tipo de accidente, etc.
        3. Explora diferentes gráficos para obtener una visión detallada de los accidentes.
    """)
    
    st.markdown("---")
    st.markdown('<p class="sidebar-text">🎨 Elige un tema para los gráficos:</p>', unsafe_allow_html=True)
    theme = st.radio("Selecciona un tema:", ["Colores Simples", "Colores más tenues", "Colores sólidos"])

    st.markdown("---")

# Si se carga un archivo
if uploaded_file:
    try:
        # Leer el archivo CSV
        data = pd.read_csv(uploaded_file)
        st.success(f"Archivo cargado exitosamente: **{uploaded_file.name}**")

        # Verificación de columnas relevantes (fecha, tipo de accidente, ubicación, etc.)
        columns = data.columns.tolist()
        st.markdown(f"### Columnas disponibles en el archivo: {', '.join(columns)}")

        # Filtrar por columna de fecha si existe
        date_columns = [col for col in columns if "fecha" in col.lower()]
        if date_columns:
            date_column = st.selectbox("Selecciona la columna de fecha:", date_columns, index=0)
            data[date_column] = pd.to_datetime(data[date_column], errors='coerce')

            # Filtro de fechas
            fecha_min = data[date_column].min()
            fecha_max = data[date_column].max()

            st.sidebar.markdown('<p class="sidebar-text">📅 Filtro de fechas:</p>', unsafe_allow_html=True)
            fecha_inicio, fecha_fin = st.sidebar.date_input(
                "Selecciona el rango de fechas:",
                value=(fecha_min, fecha_max),
                min_value=fecha_min,
                max_value=fecha_max
            )
            data = data[(data[date_column] >= pd.to_datetime(fecha_inicio)) & (data[date_column] <= pd.to_datetime(fecha_fin))]
        else:
            st.warning("No se encontró una columna de fecha en los datos.")

        # Mostrar estadísticas básicas
        st.markdown("### Estadísticas Clave de Accidentes:")
        st.write(f"Número total de accidentes: {data.shape[0]}")
        if 'ubicacion' in columns:
            st.write(f"Accidentes por ubicación: {data['ubicacion'].value_counts().head(5)}")
        if 'tipo_accidente' in columns:
            st.write(f"Accidentes por tipo: {data['tipo_accidente'].value_counts().head(5)}")

        # Gráficos básicos (e.g., accidentes por día)
        st.header("📊 Análisis Visual")

        # Gráfico de accidentes por día
        if date_column:
            accidents_by_day = data.groupby(data[date_column].dt.date).size().reset_index(name='Número de Accidentes')
            fig = px.line(accidents_by_day, x=date_column, y='Número de Accidentes', title="Accidentes por Día")
            st.plotly_chart(fig)

        # Filtros avanzados
        st.sidebar.markdown('<p class="sidebar-text">🔧 Filtros avanzados:</p>', unsafe_allow_html=True)
        accident_types = data['tipo_accidente'].unique() if 'tipo_accidente' in columns else []
        selected_accident_types = st.sidebar.multiselect("Selecciona el tipo de accidente", accident_types)

        locations = data['ubicacion'].unique() if 'ubicacion' in columns else []
        selected_locations = st.sidebar.multiselect("Selecciona la ubicación", locations)

        # Filtrar los datos según los filtros seleccionados
        if selected_accident_types:
            data = data[data['tipo_accidente'].isin(selected_accident_types)]
        if selected_locations:
            data = data[data['ubicacion'].isin(selected_locations)]

        # Opciones de gráfico
        chart_type = st.selectbox("Selecciona el tipo de gráfico:", 
                                  ["Barras", "Histograma", "Líneas", "Dispersión", "Torta"])

        # Selección de ejes para los gráficos
        x_axis = st.selectbox("Selecciona el eje X:", data.columns.tolist(), help="Eje base del gráfico")
        y_axis = st.selectbox("Selecciona el eje Y:", data.columns.tolist(), help="Eje dependiente del gráfico")

        # Generación de gráficos
        if st.button("Generar Gráfico"):
            if chart_type == "Barras":
                fig = px.bar(data, x=x_axis, y=y_axis, title=f"Gráfico de Barras: {x_axis} vs {y_axis}")
            elif chart_type == "Histograma":
                fig = px.histogram(data, x=x_axis, title=f"Histograma de {x_axis}")
            elif chart_type == "Líneas":
                fig = px.line(data, x=x_axis, y=y_axis, title=f"Gráfico de Líneas: {x_axis} vs {y_axis}")
            elif chart_type == "Dispersión":
                fig = px.scatter(data, x=x_axis, y=y_axis, title=f"Gráfico de Dispersión: {x_axis} vs {y_axis}")
            elif chart_type == "Torta":
                fig = px.pie(data, names=x_axis, title=f"Gráfico de Torta: {x_axis}")

            # Aplicar tema seleccionado
            if theme == "Colores más tenues":
                fig.update_layout(template="seaborn")
            elif theme == "Colores sólidos":
                fig.update_layout(template="simple_white")
            
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
        st.image("https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif", width=700, caption="bA")
else:
    st.warning("Por favor, sube un archivo CSV para comenzar.")
    st.image("https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDQ5OXB5d3QyZHh6ZzhlcnpzcjlmeTV1dTZyYTZxdHFoOTQ1bzIxNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/wr7oA0rSjnWuiLJOY5/giphy-downsized.gif", width=250, caption="Esperando datos...")

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
    <p class="footer">🚀 Creado por estudiantes de la USS</p>
""", unsafe_allow_html=True)
