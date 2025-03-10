import { useState } from "react";
import { useVectorStore } from "../store";
import "../styles/Search.css";

export default function Search() {
  // State variables for each parameter
  const [id, setId] = useState<number>(1);
  const [pc, setPc] = useState<string>("");
  const [collection, setCollection] = useState<string>("");
  const [vectorField, setVectorField] = useState<string>("");
  const [embeddings, setEmbeddings] = useState<string>("");
  const [metricType, setMetricType] = useState<"l2" | "ip" | "cosine" | "jaccard" | "hamming">("cosine");
  const [limit, setLimit] = useState<number>(10);
  const [data, setData] = useState<{ [field: string]: any }[]>([]);
  const [conditions, setConditions] = useState<string>("");
  const [cids, setCids] = useState<string>("");

  // Zustand store functions
  const { search, insert, delete: deleteProduct, createCollection, deleteCollection, getDetails, getResources } = useVectorStore();

  // Function handlers
  const handleSearch = () => {
    search(id, pc, collection, vectorField, embeddings.split(",").map(Number), { limit, metricType });
  };

  const handleInsert = () => {
    try {
      const parsedData = JSON.parse(data as unknown as string); // Convert input string to JSON
      insert(id, pc, collection, parsedData);
    } catch (error) {
      alert("Invalid JSON format for data.");
    }
  };

  const handleDelete = () => {
    try {
      const parsedConditions = JSON.parse(conditions);
      deleteProduct(id, pc, collection, parsedConditions);
    } catch (error) {
      alert("Invalid JSON format for conditions.");
    }
  };

  const handleCreateCollection = () => {
    createCollection(id, pc, collection, [
      { name: "id", type: "Integer32", properties: { isPrimary: true, autoIncrement: true } },
      { name: "name", type: "String" },
      { name: "description", type: "String" },
      { name: "image_url", type: "String" },
      { name: "embedding", type: "Vector", properties: { dimension: 384 } }
    ]);
  };

  const handleDeleteCollection = () => {
    deleteCollection(id, pc, collection);
  };

  const handleGetDetails = () => {
    getDetails(cids.split(","));
  };

  const handleGetResources = () => {
    getResources(id, pc);
  };

  return (
    <div className="container">
      <h2>Vector Store Platform</h2>

      {/* 🔍 Search Section */}
      <div className="section">
        <h3>🔍 Search Products</h3>
        <input type="number" placeholder="ID" value={id} onChange={(e) => setId(Number(e.target.value))} className="input-field" />
        <input type="text" placeholder="PC Address" value={pc} onChange={(e) => setPc(e.target.value)} className="input-field" />
        <input type="text" placeholder="Collection Name" value={collection} onChange={(e) => setCollection(e.target.value)} className="input-field" />
        <input type="text" placeholder="Vector Field" value={vectorField} onChange={(e) => setVectorField(e.target.value)} className="input-field" />
        <input type="text" placeholder="Embeddings (comma-separated)" value={embeddings} onChange={(e) => setEmbeddings(e.target.value)} className="input-field" />
        <select value={metricType} onChange={(e) => setMetricType(e.target.value as "l2" | "ip" | "cosine" | "jaccard" | "hamming")} className="input-field">
          <option value="l2">L2 Distance</option>
          <option value="ip">Inner Product</option>
          <option value="cosine">Cosine Similarity</option>
          <option value="jaccard">Jaccard Similarity</option>
          <option value="hamming">Hamming Distance</option>
        </select>
        <input type="number" placeholder="Limit" value={limit} onChange={(e) => setLimit(Number(e.target.value))} className="input-field" />
        <button onClick={handleSearch} className="search-button">Search</button>
      </div>

      {/* 📥 Insert Data */}
      <div className="section">
        <h3>📥 Insert Data</h3>
        <textarea placeholder="Data (JSON format)" value={JSON.stringify(data)} onChange={(e) => setData(JSON.parse(e.target.value))} className="input-field" />
        <button onClick={handleInsert} className="insert-button">Insert</button>
      </div>

      {/* 🗑️ Delete Data */}
      <div className="section">
        <h3>🗑️ Delete Data</h3>
        <textarea placeholder="Conditions (JSON format)" value={conditions} onChange={(e) => setConditions(e.target.value)} className="input-field" />
        <button onClick={handleDelete} className="delete-button">Delete</button>
      </div>

      {/* 📁 Collection Management */}
      <div className="section">
        <h3>📁 Create a Collection</h3>
        <input type="text" placeholder="Collection Name" value={collection} onChange={(e) => setCollection(e.target.value)} className="input-field" />
        <button onClick={handleCreateCollection} className="insert-button">Create Collection</button>
      </div>

      <div className="section">
        <h3>🗑️ Delete Collection</h3>
        <input type="text" placeholder="Collection Name" value={collection} onChange={(e) => setCollection(e.target.value)} className="input-field" />
        <button onClick={handleDeleteCollection} className="delete-button">Delete Collection</button>
      </div>

      {/* 📄 Retrieve Details */}
      <div className="section">
        <h3>📄 Retrieve File Details</h3>
        <input type="text" placeholder="CIDs (comma-separated)" value={cids} onChange={(e) => setCids(e.target.value)} className="input-field" />
        <button onClick={handleGetDetails} className="search-button">Retrieve Details</button>
      </div>

      {/* 🏗️ Get Resources */}
      <div className="section">
        <h3>🛠 Retrieve Resources</h3>
        <input type="number" placeholder="Resource ID (Optional)" value={id} onChange={(e) => setId(Number(e.target.value))} className="input-field" />
        <input type="text" placeholder="PC Address (Optional)" value={pc} onChange={(e) => setPc(e.target.value)} className="input-field" />
        <button onClick={handleGetResources} className="search-button">Get Resources</button>
      </div>
    </div>
  );
}
