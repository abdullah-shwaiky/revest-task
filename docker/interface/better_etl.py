import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import pyarrow as pa
DATABASE_URL = 'postgresql://revestPG:Revest_Admin2024@postgres:5432/postgres'
engine = create_engine(DATABASE_URL)
db_conn = psycopg2.connect(
        host="postgres",
        port=5432,
        database="postgres",
        user="revestPG",
        password="Revest_Admin2024"
    )
cursor = db_conn.cursor()


# Extract - Read From CSV:
data = pd.read_csv("sales.csv").infer_objects()

# Transform:
data.columns = [x.lower().replace(' ', '_').replace('-','_') for x in data.columns]
data = data.rename(columns={"row_id": "purchase_id"})

# Not Missing At Random Values Found
# Filling missing postal code data with correct value:
data.loc[data['city']=='Burlington', "postal_code"] = 5401

# Splitting DB to Logical Sectors: (Order Details, Customer Details, Product Details)

orders = data[['purchase_id', 'order_id', 'order_date','ship_date', 'ship_mode', 'sales', 'customer_id', 'product_id']]
customers = data[['customer_id', 'customer_name', 'segment', 'country','city','state','postal_code','region']]
products = data[['product_id', 'category', 'sub_category', 'product_name']]

print(orders.duplicated().sum())
# Dropping dupliactes in IDs:
orders = orders.drop_duplicates(['purchase_id'])
customers = customers.drop_duplicates(['customer_id'])
products = products.drop_duplicates(['product_id'])

# Load
# Load data to Database
orders.to_sql('orders', engine, if_exists='replace', index=False)
customers.to_sql('customers', engine, if_exists='replace', index=False)
products.to_sql('products', engine, if_exists='replace', index=False)


pk_command = """
    ALTER TABLE orders
    ADD PRIMARY KEY (purchase_id);
    
    ALTER TABLE orders
    ALTER COLUMN order_date TYPE DATE 
    using to_date(order_date, 'DD/MM/YYYY');
    
    ALTER TABLE orders
    ALTER COLUMN ship_date TYPE DATE 
    using to_date(ship_date, 'DD/MM/YYYY');
    
    ALTER TABLE customers
    ADD PRIMARY KEY (customer_id);
    
    ALTER TABLE products
    ADD PRIMARY KEY (product_id);
"""
cursor.execute(pk_command)
db_conn.commit()

for table_name in ["orders", "customers", "products"]:
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    table = pa.Table.from_pandas(df)
    table.to_pandas().to_parquet(f'{table_name}.parquet', engine='pyarrow')