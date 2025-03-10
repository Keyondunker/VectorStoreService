import { create } from "zustand";
import axios from "axios";

// Interface for Product Data
interface Product {
  id?: number;
  name: string;
  description: string;
  image_url: string;
  similarity?: number;
}

// Interface for Collection Fields
interface CollectionField {
  name: string;
  type: "String" | "Integer32" | "Integer64" | "Float" | "Vector" | "Boolean";
  properties?: {
    isPrimary?: boolean;
    default?: any;
    dimension?: number;
    autoIncrement?: boolean;
  };
}

// Interface for Zustand Store
interface VectorStore {
  results: Product[];
  collections: string[];
  search: (id: number, pc: string, collection: string, vectorField: string, embeddings: any[], options?: { limit?: number, metricType?: "l2" | "ip" | "cosine"| "jaccard" | "hamming"}) => void;
  insert: (id: number, pc: string, collection: string, data: Omit<Product, "id" | "similarity">[]) => void;
  delete: (id: number, pc: string, collection: string, conditions: Record<string, any>) => void;
  createCollection: (id: number, pc: string, name: string, fields: CollectionField[]) => void;
  deleteCollection: (id: number, pc: string, name: string) => void;
  getDetails: (cids: string[]) => void;
  getResources: (id?: number, pc?: string) => void;
}

// Create Zustand Store
export const useVectorStore = create<VectorStore>((set) => ({
  results: [],
  collections: [],

  // Search for products using vector embeddings
  search: async (id, pc, collection, vectorField, embeddings, options) => {
    try {
      const response = await axios.post("http://localhost:8000/search-vectors/", {
        id,
        pc,
        collection,
        vectorField,
        embeddings,
        options
      });
      set({ results: response.data.results });
    } catch (error) {
      console.error("Search error:", error);
    }
  },

  // Insert a new product into a collection
  insert: async (id, pc, collection, data) => {
    try {
      await axios.post("http://localhost:8000/insert-data/", {
        id,
        pc,
        collection,
        data,
      });
    } catch (error) {
      console.error("Insert error:", error);
    }
  },

  // Delete a product from a collection
  delete: async (id, pc, collection, conditions) => {
    try {
      await axios.post("http://localhost:8000/delete-data/", {
        id,
        pc,
        collection,
        conditions,
      });
    } catch (error) {
      console.error("Delete error:", error);
    }
  },

  // Create a new collection
  createCollection: async (id, pc, name, fields) => {
    try {
      await axios.post("http://localhost:8000/create-collection/", {
        id,
        pc,
        name,
        fields,
      });
      set((state) => ({ collections: [...state.collections, name] }));
    } catch (error) {
      console.error("Create Collection error:", error);
    }
  },

  // Delete an existing collection
  deleteCollection: async (id, pc, name) => {
    try {
      await axios.post("http://localhost:8000/delete-collection/", {
        id,
        pc,
        name,
      });
      set((state) => ({ collections: state.collections.filter((col) => col !== name) }));
    } catch (error) {
      console.error("Delete Collection error:", error);
    }
  },

  // Retrieve file details from given CIDs
  getDetails: async (cids) => {
    try {
      const response = await axios.post("http://localhost:8000/details/", { body: cids });
      console.log("Details retrieved:", response.data);
    } catch (error) {
      console.error("Details retrieval error:", error);
    }
  },

  // Retrieve available resources
  getResources: async (id, pc) => {
    try {
      const response = await axios.get("http://localhost:8000/resources/", { params: { id, pc } });
      console.log("Resources retrieved:", response.data);
    } catch (error) {
      console.error("Resource retrieval error:", error);
    }
  },
}));
