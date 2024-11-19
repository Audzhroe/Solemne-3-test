import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Análisis Inteligente de Accidentes", layout="wide", page_icon="🚗")
st.title("🚗 **Análisis Inteligente de Accidentes**")
st.markdown("Explora datos y genera gráficos con validaciones dinámicas para asegurar que las selecciones sean coherentes.")

# Cargar datos
with st.sidebar:
    uploaded_file = st.file_uploader("📂 Sube tu archivo CSV:", type=["csv"])
    st.markdown("### 🎨 Tema de gráficos:")
    theme = st.radio("Selecciona un tema:", ["Plotly", "Seaborn", "Simple"])

if uploaded_file:
    # Leer archivo
    data = pd.read_csv(uploaded_file)
    st.success(f"Archivo cargado exitosamente: **{uploaded_file.name}**")
    
    # Opciones de gráficos
    st.header("📊 Gráficos Inteligentes")
    chart_type = st.selectbox("Selecciona el tipo de gráfico:", 
                              ["Barras", "Histograma", "Líneas", "Dispersión", "Torta"])
    
    columns = data.columns.tolist()
    column_types = {col: str(data[col].dtype) for col in columns}  # Mapear columnas y sus tipos
    
    # Selección dinámica del eje X
    x_axis = st.selectbox("Selecciona el eje X:", columns, help="Eje base del gráfico")
    
    # Filtrar columnas válidas para el eje Y según el gráfico y eje X seleccionado
    if chart_type in ["Líneas", "Dispersión"]:
        # Para gráficos continuos, solo números
        valid_y_columns = [col for col in columns if column_types[col] in ["int64", "float64"]]
    elif chart_type == "Torta":
        # Para gráficos de torta, solo categorías
        valid_y_columns = [col for col in columns if column_types[col] == "object"]
    else:
        # Para otros gráficos, cualquier columna excepto la seleccionada para X
        valid_y_columns = [col for col in columns if col != x_axis]
    
    if chart_type != "Torta":
        y_axis = st.selectbox("Selecciona el eje Y:", valid_y_columns, help="Eje dependiente del gráfico")
    
    # Validación: advertir si no hay columnas válidas para el eje Y
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
            
            if theme == "Seaborn":
                fig.update_layout(template="seaborn")
            elif theme == "Simple":
                fig.update_layout(template="simple_white")
            st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Por favor, sube un archivo CSV para comenzar.")

# Footer
st.markdown("---")
st.markdown("📢 **Nota:** Las selecciones dinámicas aseguran que los datos sean compatibles con el tipo de gráfico.")
