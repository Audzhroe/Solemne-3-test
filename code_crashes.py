import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Análisis Inteligente de Accidentes", layout="wide", page_icon="🚗")
st.title("🚗 **Análisis Inteligente de Accidentes**")
st.markdown("Explora datos y genera gráficos con validaciones dinámicas para asegurar que las selecciones sean coherentes.")

# Cargar datos desde la barra lateral
with st.sidebar:
    uploaded_file = st.file_uploader("📂 Sube tu archivo CSV:", type=["csv"])
    st.markdown("### 🎨 Tema de gráficos:")
    theme = st.radio("Selecciona un tema:", ["Plotly", "Seaborn", "Simple"])

# Si hay un archivo subido
if uploaded_file:
    try:
        # Leer el archivo CSV
        data = pd.read_csv(uploaded_file)
        st.success(f"Archivo cargado exitosamente: **{uploaded_file.name}**")
        
        # Obtener columnas y sus tipos
        columns = data.columns.tolist()
        column_types = data.dtypes.apply(lambda x: x.name).to_dict()

        # Opciones de gráficos
        st.header("📊 Gráficos Inteligentes")
        chart_type = st.selectbox("Selecciona el tipo de gráfico:", 
                                  ["Barras", "Histograma", "Líneas", "Dispersión", "Torta"])

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

# Footer
st.markdown("---")
st.markdown("📢 **Nota:** Las selecciones dinámicas aseguran que los datos sean compatibles con el tipo de gráfico.")
