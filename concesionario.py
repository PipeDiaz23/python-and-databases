import mysql.connector
import os
import streamlit as st

def insert_data_bulk(df, table_name='clientesypedidos'):
    connection = None
    cursor = None

    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            st.success("Connected to the database successfully.")
            cursor = connection.cursor()

            # Consulta de inserción para los datos de clientes y órdenes
            insert_query = f"""
            INSERT INTO {table_name} (ClientID, ClientName, ContactNumber, Email, ProductID, OrderID, OrderDate, Quantity, CustomerName, DeliveryAddress)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Convertir el DataFrame a una lista de tuplas
            data_to_insert = df[['ClientID', 'ClientName', 'ContactNumber', 'Email', 'ProductID', 'OrderID', 'OrderDate', 'Quantity', 'CustomerName', 'DeliveryAddress']].to_records(index=False).tolist()

            # Ejecutar la inserción en bulk
            cursor.executemany(insert_query, data_to_insert)
            
            # Confirmar la transacción
            connection.commit()

            st.success(f"{cursor.rowcount} rows inserted successfully.")

    except mysql.connector.Error as e:
        st.error(f"Error: {e}")
        if connection:
            connection.rollback()

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
