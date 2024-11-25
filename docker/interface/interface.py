import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import requests
import psycopg2
from sqlalchemy import create_engine
from pymongo import MongoClient

# Connection to Postgres Database
DATABASE_URL = 'postgresql://revestPG:Revest_Admin2024@postgres:5432/postgres'
engine = create_engine(DATABASE_URL)
db_conn = psycopg2.connect(
        host="postgres",
        port=5432,
        database="postgres",
        user="revestPG",
        password="Revest_Admin2024"
    )

# Connection to MongoDB
# Connect to MongoDB (change the connection string if you're using a different setup)
client = MongoClient("mongodb://mongodb:27017/")

# Select the database and collection
db = client["api_logs"]
logs_collection = db["logs"]


# Django REST Framework API for Recommendations
API_URL = "http://django:8000/api/recommend/"


# Page 1: Show sales related data and plots
def first_page():
    st.title("Sales Data Overview")

    # Get the number of total orders made (grouping by order_id)
    orders = pd.read_sql(
            """SELECT order_id, ROUND(cast(AVG(sales) as numeric), 2)\nFROM orders\nGROUP BY order_id;""", engine
        )
    st.write(f"Number# of orders: {len(orders)}")

    # Plot x as sales category and y as sales
    st.subheader("Order distribution by value:")
    st.code("""SELECT order_id, ROUND(cast(AVG(sales) as numeric), 2)\nFROM orders\nGROUP BY order_id;""", language='sql')
    mn = round(orders['round'].min(), 2)
    Q1 = round(orders['round'].quantile(0.25), 2)
    # Q2 = round(orders['round'].quantile(0.50), 2)
    Q3 = round(orders['round'].quantile(0.75), 2)
    # mx = round(orders['round'].quantile(1), 2)
    IQR = Q3 - Q1
    # Create a new column to categorize data into ranges
    def categorize_quartile(value):
        if value <= Q1 - 1.5 * IQR or value >= Q3 + 1.5 * IQR:
            return f'Outlier'
        else:
            return 'Within Range'

    # Apply the function to categorize each value
    df_quartiles = orders['round'].apply(categorize_quartile)


    # Plotting the data grouped by quartiles
    quartile_counts = df_quartiles.value_counts().reset_index().sort_values(by='round')
    quartile_counts.columns = ['Quartile', 'Count']

    # Create a bar plot using Plotly
    fig = px.bar(quartile_counts, x='Quartile', y='Count', color='Quartile', 
                labels={'Quartile': 'Quartile', 'Count': 'Count of Values'},
                title="Distribution of Data for Outliers")

    
    st.plotly_chart(fig)

    # Plot sales grouped by month
    monthly_sales = pd.read_sql(
            """SELECT EXTRACT(month from order_date), ROUND(CAST(AVG(sales) as numeric), 2)
            FROM orders
            GROUP BY EXTRACT(month from order_date);""", engine
        ).sort_values(by='extract')
    
    st.subheader("Sales Grouped by Month")
    st.code("""SELECT EXTRACT(month from order_date), ROUND(CAST(AVG(sales) as numeric), 2)\nFROM orders\nGROUP BY EXTRACT(month from order_date);""", language='sql')

    fig = px.bar(monthly_sales, x='extract', y='round', labels={'extract': 'Month', 'round': 'Total Sales'},
                 title="Monthly Sales")
    st.plotly_chart(fig)

# Second Page: User input, API call, and JSON display
def second_page():
    st.title("Recommendations")

    # User input field for product ID
    product_id = st.text_input("Enter Product ID:")

    if st.button("Submit") and product_id:
        # Make API call
        response = requests.post(API_URL, json={"id": product_id})
        
        if response.status_code == 200:
            # Show the JSON response
            product_data = response.json()
            for i, product in enumerate(product_data):
                # Extract required fields
                st.subheader(f"Product {i+1} Information")
                st.write(f"**Product ID:** {product.get('product_id')}")
                st.write(f"**Category:** {product.get('category')}")
                st.write(f"**Sub-category:** {product.get('sub_category')}")
                st.write(f"**Product Name:** {product.get('product_name')}")
        else:
            st.error(f"Error fetching product data. Status Code: {response.status_code}")
    else:
        st.warning("Please enter a Product ID to get details.")
        
def logs_page():
    st.title("Recent API Logs")
    st.write("This interface shows the 10 most recent API logs in counter-chronological order.")
    logs = logs_collection.find().sort("timestamp", -1).limit(10)
    for log in logs:
        st.subheader(f"Request ID#: {log.get('request_id')}")
        st.write(f"**Timestamp:** {log.get('timestamp')}")
        st.write(f"**Input Product ID:** {log.get('input').get('id')}")
        st.write(f"**Recommendations:** {[x.get('product_name') for x in log.get('output').values()]}")
    

# Streamlit multi-page setup
def main():
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", ["Sales Overview", "Product Recommendations", "Logs"])

    if page == "Sales Overview":
        first_page()
    elif page == "Product Recommendations":
        second_page()
    elif page == "Logs":
        logs_page()

if __name__ == "__main__":
    main()
