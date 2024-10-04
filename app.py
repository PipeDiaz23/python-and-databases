import streamlit as st
import pandas as pd
from concesionario import insert_data_bulk

def _extract_data_from_excel(excel_file):
    try:
        df = pd.read_excel(excel_file)
        return df
    except Exception as e:
        st.write(f"Error reading the Excel file: {e}")
        return pd.DataFrame()

st.title("Upload two Excel files to combine")

uploaded_file_1 = st.file_uploader("Upload first Excel file", type=["xls", "xlsx"], key="file1")
uploaded_file_2 = st.file_uploader("Upload second Excel file", type=["xls", "xlsx"], key="file2")

if uploaded_file_1 is not None and uploaded_file_2 is not None:
    st.write("Both files uploaded successfully.")
    
    df1 = _extract_data_from_excel(uploaded_file_1)
    st.write(df1)
    df2 = _extract_data_from_excel(uploaded_file_2)
    st.write(df2)
    
    # # Limpiar los nombres de las columnas
    # df1.columns = df1.columns.str.strip()
    # df2.columns = df2.columns.str.strip()
    
    if not df1.empty and not df2.empty:
        # Verificar si ProductID existe en ambos DataFrames
        if 'ProductID' in df1.columns and 'ProductID' in df2.columns:
            # Realizar el merge
            combined_df = pd.merge(df1, df2, on='ProductID', how='inner')
            st.write("Combined DataFrame:")
            st.write(combined_df)
            
            # Botón para insertar los datos en la base de datos
            if st.button("Upload to Database"):
                insert_data_bulk(combined_df)  # Llamada a la función para insertar los datos
                st.success("Data inserted into the database successfully!")
        else:
            st.write("Column 'ProductID' not found in one or both files.")
    else:
        st.write("One or both files are empty or invalid.")
