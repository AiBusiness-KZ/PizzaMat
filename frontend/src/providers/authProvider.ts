import { AuthProvider } from "@refinedev/core";
import axios from "axios";

// Use relative path for API calls (works with proxy in dev and production)
const API_URL = "";

export const authProvider: AuthProvider = {
  login: async ({ username, password }) => {
    try {
      const response = await axios.post(`${API_URL}/api/auth/login`, {
        username,
        password,
      });

      if (response.data.access_token) {
        localStorage.setItem("token", response.data.access_token);
        localStorage.setItem("is_admin", response.data.is_admin);
        return {
          success: true,
          redirectTo: "/admin",
        };
      }

      return {
        success: false,
        error: {
          name: "LoginError",
          message: "Invalid username or password",
        },
      };
    } catch (error: any) {
      return {
        success: false,
        error: {
          name: "LoginError",
          message: error?.response?.data?.detail || "Login failed",
        },
      };
    }
  },

  logout: async () => {
    localStorage.removeItem("token");
    localStorage.removeItem("is_admin");
    return {
      success: true,
      redirectTo: "/login",
    };
  },

  check: async () => {
    const token = localStorage.getItem("token");
    if (token) {
      return {
        authenticated: true,
      };
    }

    return {
      authenticated: false,
      logout: true,
      redirectTo: "/login",
    };
  },

  getPermissions: async () => {
    const isAdmin = localStorage.getItem("is_admin");
    return isAdmin === "true" ? ["admin"] : [];
  },

  getIdentity: async () => {
    const token = localStorage.getItem("token");
    if (token) {
      return {
        id: "admin",
        name: "Admin",
        avatar: "https://i.pravatar.cc/300",
      };
    }
    return null;
  },

  onError: async (error) => {
    if (error?.status === 401 || error?.status === 403) {
      return {
        logout: true,
        redirectTo: "/login",
        error,
      };
    }

    return { error };
  },
};
