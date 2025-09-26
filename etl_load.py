# etl_load.py
import pandas as pd
from neo4j import GraphDatabase

# -----------------------
# Neo4j Connection Config
# -----------------------
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "sharan,27"   # make sure this matches your Neo4j setup

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

# -----------------------
# Helper Functions
# -----------------------
def create_nodes(tx, label, props):
    """
    Create or update a node in Neo4j.
    """
    props_str = ", ".join([f"{k}: ${k}" for k in props.keys()])
    query = f"""
    MERGE (n:{label} {{id: $id}})
    SET n += {{{props_str}}}
    """
    tx.run(query, **props)

def load_csv(file, label, mapping):
    """
    Load nodes from CSV into Neo4j.
    - file: path to CSV
    - label: Neo4j node label (e.g., Career, Skill)
    - mapping: dict {neo4j_prop: csv_column}
    """
    df = pd.read_csv(file)
    with driver.session() as session:
        for _, row in df.iterrows():
            props = {}
            for k, v in mapping.items():
                if v in row:
                    props[k] = row[v]
            # ensure id is always present
            if "id" not in props and "id" in df.columns:
                props["id"] = row["id"]
            session.write_transaction(create_nodes, label, props)

# -----------------------
# Main Load Script
# -----------------------
if __name__ == "__main__":
    # Careers CSV
    load_csv("data/careers.csv", "Career", {
        "id": "id",
        "career": "career",
        "description": "description",
        "required_skills": "required_skills"
    })

    # Skills CSV
    load_csv("data/skills.csv", "Skill", {
        "id": "id",
        "name": "name",
        "description": "description"
    })

    # Personality CSV
    load_csv("data/personality.csv", "Personality", {
        "id": "id",
        "name": "name",
        "dimension": "dimension",
        "description": "description"
    })

    # Institutions CSV
    load_csv("data/institutions.csv", "Institution", {
        "id": "id",
        "name": "name",
        "location": "location",
        "courses": "courses"
    })

    print("✅ ETL Load Complete: All CSVs imported into Neo4j.")