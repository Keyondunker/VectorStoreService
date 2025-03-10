from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import psycopg2
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to PostgreSQL
conn = psycopg2.connect("dbname=vector_store user=postgres password=yourpassword")
cur = conn.cursor()

# 🔍 Get File Details
@app.get("/details")
def get_details(body: List[str]):
    """Retrieve file details for given CIDs (Content Identifiers)."""
    details = []
    for cid in body:
        try:
            with open(f"./data/{cid}.txt", "r") as file:
                details.append(file.read())
        except FileNotFoundError:
            return JSONResponse(content={"error": f"File for CID {cid} not found"}, status_code=404)
    
    return details

# 🔍 Get Resources
@app.get("/resources")
def get_resources(id: Optional[int] = None, pc: Optional[str] = None):
    """Retrieve resource details based on ID or PC (Address)."""
    if id and pc:
        query = "SELECT * FROM resources WHERE id = %s AND pc = %s"
        cur.execute(query, (id, pc))
        resource = cur.fetchone()
        return {"resource": resource}
    else:
        cur.execute("SELECT * FROM resources")
        resources = cur.fetchall()
        return {"resources": resources}

# 📂 Create Collection
@app.post("/collection")
def create_collection(body: Dict[str, Any]):
    """Create a new collection (table) dynamically in PostgreSQL."""
    id = body["id"]
    pc = body["pc"]
    name = body["name"]
    fields = body["fields"]

    field_definitions = []
    for field in fields:
        field_type = {
            "String": "TEXT",
            "Integer32": "INTEGER",
            "Integer64": "BIGINT",
            "Float": "FLOAT",
            "Vector": f"VECTOR({field.get('dimension', 128)})",
            "Boolean": "BOOLEAN"
        }[field["type"]]

        if field.get("isPrimary"):
            field_definitions.append(f"{field['name']} {field_type} PRIMARY KEY")
        else:
            field_definitions.append(f"{field['name']} {field_type}")

    query = f"CREATE TABLE IF NOT EXISTS {name} ({', '.join(field_definitions)})"
    cur.execute(query)
    conn.commit()

    return {"message": f"Collection '{name}' created successfully"}

# ❌ Delete Collection
@app.delete("/collection")
def delete_collection(body: Dict[str, Any]):
    """Delete an existing collection."""
    query = f"DROP TABLE IF EXISTS {body['name']}"
    cur.execute(query)
    conn.commit()
    
    return {"message": f"Collection '{body['name']}' deleted successfully"}

# 🔍 Search in Collection
@app.post("/search")
def search(body: Dict[str, Any]):
    """Search for similar vectors in the collection."""
    id = body["id"]
    pc = body["pc"]
    collection = body["collection"]
    vector_field = body["vectorField"]
    embeddings = body["embeddings"]
    limit = body.get("options", {}).get("limit", 10)
    metric_type = body.get("options", {}).get("metricType", "cosine")

    metric_operator = {
        "l2": "<->",
        "ip": "<#>",
        "cosine": "<=>"
    }[metric_type]

    query = f"""
    SELECT *, 1 - ({vector_field} {metric_operator} %s) AS similarity
    FROM {collection}
    ORDER BY similarity DESC
    LIMIT {limit}
    """
    cur.execute(query, (embeddings,))
    results = cur.fetchall()

    return {"results": results}

# 📥 Insert Data into Collection
@app.post("/data")
def insert_data(body: Dict[str, Any]):
    """Insert data into an existing collection."""
    collection = body["collection"]
    data = body["data"]

    for item in data:
        text = item["description"]
        embedding = model.encode(text).tolist()
        item["embedding"] = embedding  # Add the embedding to the item data

        fields = ", ".join(item.keys())
        values = tuple(item.values())
        placeholders = ", ".join(["%s"] * len(item))
        query = f"INSERT INTO {collection} ({fields}) VALUES ({placeholders})"
        cur.execute(query, values)
    
    conn.commit()
    return {"message": "Data inserted successfully"}

# ❌ Delete Data from Collection
@app.delete("/data")
def delete_data(body: Dict[str, Any]):
    """Delete data from a collection based on conditions."""
    collection = body["collection"]
    conditions = body["conditions"]

    condition_str = " AND ".join([f"{k} = %s" for k in conditions.keys()])
    query = f"DELETE FROM {collection} WHERE {condition_str}"
    cur.execute(query, tuple(conditions.values()))
    conn.commit()

    return {"message": "Data deleted successfully"}

