from neo4j import GraphDatabase
import csv
import os

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("****", "****")
)

def create_constraints():
    with driver.session() as session:
        session.run("""
            CREATE CONSTRAINT IF NOT EXISTS
            FOR (d:Disease) REQUIRE d.name IS UNIQUE
        """)
        session.run("""
            CREATE CONSTRAINT IF NOT EXISTS
            FOR (dr:Drug) REQUIRE dr.name IS UNIQUE
        """)

def load_data(csv_file: str):
    with driver.session() as session, open(csv_file, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            disease = row["Disease"]
            drug = row["Drug"]
            relation = row.get("Relation", "TREATS")

            query = f"""
            MERGE (d:Disease {{name:$disease}})
            MERGE (dr:Drug {{name:$drug}})
            MERGE (dr)-[:{relation}]->(d)
            """

            session.run(query, disease=disease, drug=drug)

if __name__ == "__main__":
    create_constraints()
    load_data("data/drugs_diseases.csv")
    print("Graph data loaded successfully!")