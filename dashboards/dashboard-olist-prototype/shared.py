from pathlib import Path 
import duckdb

db_path = Path(__file__).parent.parent.parent.parent

# Connect to Olist database
conn = duckdb.connect( db_path / 'olist-data-pipeline/olist_medallion_architecture.db', read_only = True)

# (temp) Materialize data to Pandas DataFrame
orders_df = conn.query("SELECT * FROM gold_orders").to_df()

# Close database connection
conn.close()