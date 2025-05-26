import pandas as pd
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

# ---- Config ----
NEO4J_URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# ---- Read CSVs ----
ministries_df = pd.read_csv("ministries.csv")
departments_df = pd.read_csv("departments.csv")

# ---- Connect to Neo4j ----
driver = GraphDatabase.driver(NEO4J_URI, auth=(USERNAME, PASSWORD))

def load_data(tx, ministries, departments):
    for _, row in ministries.iterrows():
        tx.run("""
            MERGE (m:Ministry {id: $id})
            SET m.name = $name, m.google_map_script = $script
        """, id=row['id'], name=row['name'], script=row['google_map_script'])

    for _, row in departments.iterrows():
        tx.run("""
            MERGE (d:Department {id: $id})
            SET d.name = $name, d.google_map_script = $script
            WITH d
            MATCH (m:Ministry {id: $ministry_id})
            MERGE (m)-[:HAS_DEPARTMENT]->(d)
        """, id=row['id'], name=row['name'], script=row['google_map_script'], ministry_id=row['ministry_id'])

with driver.session() as session:
    session.execute_write(load_data, ministries_df, departments_df)

driver.close()
print("✅ Data successfully imported to Neo4j.")
