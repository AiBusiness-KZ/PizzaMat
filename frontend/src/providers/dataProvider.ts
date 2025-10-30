import { DataProvider } from "@refinedev/core";
import axios from "axios";

// Use relative path for API calls (works with proxy in dev and production)
const API_URL = "";

// Helper to convert File objects to FormData
const toFormData = (obj: any): FormData => {
  const formData = new FormData();
  Object.keys(obj).forEach((key) => {
    const value = obj[key];
    if (value !== undefined && value !== null) {
      if (value instanceof File) {
        formData.append(key, value);
      } else if (typeof value === 'boolean') {
        formData.append(key, value.toString());
      } else {
        formData.append(key, value);
      }
    }
  });
  return formData;
};

export const dataProvider: DataProvider = {
  getList: async ({ resource, pagination, filters, sorters, meta }) => {
    const url = `${API_URL}/api/admin/${resource}`;
    
    const { data } = await axios.get(url);
    
    // Backend now returns data directly: [...]
    const items = Array.isArray(data) ? data : [];
    
    return {
      data: items,
      total: items.length,
    };
  },

  getOne: async ({ resource, id, meta }) => {
    const url = `${API_URL}/api/admin/${resource}/${id}`;
    
    const { data } = await axios.get(url);
    
    // Backend returns data directly
    return {
      data: data,
    };
  },

  create: async ({ resource, variables, meta }) => {
    const url = `${API_URL}/api/admin/${resource}`;
    
    // Backend expects FormData
    const formData = toFormData(variables);
    
    const { data } = await axios.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    // Backend returns data directly: { id: ..., name: ... }
    return {
      data: data,
    };
  },

  update: async ({ resource, id, variables, meta }) => {
    const url = `${API_URL}/api/admin/${resource}/${id}`;
    
    // Backend expects FormData
    const formData = toFormData(variables);
    
    const { data } = await axios.put(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    // Backend returns { success: true, message: "..." } for updates
    // Return the id since that's what Refine expects
    return {
      data: { id, ...data },
    };
  },

  deleteOne: async ({ resource, id, meta }) => {
    const url = `${API_URL}/api/admin/${resource}/${id}`;
    
    const { data } = await axios.delete(url);
    
    // Backend returns { success: true, message: "..." } for deletes
    return {
      data: { id },
    };
  },

  getApiUrl: () => API_URL,
};
