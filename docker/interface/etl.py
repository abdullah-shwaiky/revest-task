import pandas as pd
from sqlalchemy import create_engine
import psycopg2
DATABASE_URL = 'postgresql://postgres:postgres@localhost:5433/postgres'
engine = create_engine(DATABASE_URL)
db_conn = psycopg2.connect(
        host="postgres",
        port=5433,
        database="postgres",
        user="revestPG",
        password="RevestAdmin@2024"
    )
cursor = db_conn.cursor()


# Extract - Read From CSV:
data = pd.read_csv("sales.csv").infer_objects()

# Transform:
data = data.drop(['Row ID'], axis = 1)
# Dropping dupliactes in IDs:
data = data.drop_duplicates(['Order ID'])
data.columns = [x.lower().replace(' ', '_').replace('-','_') for x in data.columns]

# Not Missing At Random Values Found
# Filling missing postal code data with correct value:
data.loc[data['city']=='Burlington', "postal_code"] = 5401

# Load
# Load data to Database
data.to_sql('sales_data', engine, if_exists='replace', index=False)
pk_command = """
    ALTER TABLE sales_data
    ADD PRIMARY KEY (order_id);
    ALTER TABLE sales_data
    ALTER COLUMN order_date TYPE DATE 
    using to_date(order_date, 'DD/MM/YYYY');
    ALTER TABLE sales_data
    ALTER COLUMN ship_date TYPE DATE 
    using to_date(ship_date, 'DD/MM/YYYY');
"""
cursor.execute(pk_command)
db_conn.commit()