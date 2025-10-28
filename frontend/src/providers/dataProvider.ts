import { DataProvider } from "@refinedev/core";
import axios from "axios";

const API_URL = "http://localhost:8000";

// Helper to convert File objects to FormData
const toFormData = (obj: Record<string, any>): FormData => {
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
    
    // Backend returns: { success: true, data: [...] }
    const items = data.data || [];
    
    return {
      data: items,
      total: items.length, // Временно, пока backend не возвращает total
    };
  },

  getOne: async ({ resource, id, meta }) => {
    const url = `${API_URL}/api/admin/${resource}/${id}`;
    
    const { data } = await axios.get(url);
    
    return {
      data: data.data || data,
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
    
    return {
      data: data.data || { id: data.data?.id },
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
    
    return {
      data: data.data || { id },
    };
  },

  deleteOne: async ({ resource, id, meta }) => {
    const url = `${API_URL}/api/admin/${resource}/${id}`;
    
    const { data } = await axios.delete(url);
    
    return {
      data: data.data || { id },
    };
  },

  getApiUrl: () => API_URL,
};
