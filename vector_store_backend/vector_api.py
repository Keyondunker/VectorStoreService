from fastapi import FastAPI, HTTPException
import psycopg2
from typing import List, Dict, Any

app = FastAPI()

# Database connection
conn = psycopg2.connect("dbname=vector_store user=postgres password=yourpassword")
cur = conn.cursor()

@app.post("/search")
def search(collection: str, vector_field: str, embeddings: List[float], limit: int = 10):
    query = f"""
    SELECT *, 1 - (embedding <-> %s) AS similarity 
    FROM {collection} 
    ORDER BY similarity DESC 
    LIMIT {limit}
    """
    cur.execute(query, (embeddings,))
    results = cur.fetchall()
    return {"results": results}

@app.post("/insert")
def insert_data(collection: str, data: Dict[str, Any]):
    keys = ", ".join(data.keys())
    values = ", ".join(["%s"] * len(data))
    query = f"INSERT INTO {collection} ({keys}) VALUES ({values})"
    cur.execute(query, tuple(data.values()))
    conn.commit()
    return {"message": "Data inserted"}

@app.delete("/delete")
def delete_data(collection: str, conditions: Dict[str, Any]):
    condition_str = " AND ".join([f"{k} = %s" for k in conditions.keys()])
    query = f"DELETE FROM {collection} WHERE {condition_str}"
    cur.execute(query, tuple(conditions.values()))
    conn.commit()
    return {"message": "Data deleted"}
