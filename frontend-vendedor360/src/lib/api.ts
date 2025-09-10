import axios from "axios";

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
  timeout: 20000,
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    console.error("API error:", err?.response?.data || err.message);
    return Promise.reject(err);
  }
);

export const ApiRoutes = {
  health: () => api.get("/health"),
  kpis: () => api.get("/kpis/overview"),
  inventario: (params?: Record<string, any>) => api.get("/inventory", { params }),
  cotizaciones: (params?: Record<string, any>) => api.get("/quotes", { params }),
  ordenes: (params?: Record<string, any>) => api.get("/orders", { params }),
  loginOtp: (email: string) => api.post("/auth/otp/request", { email }),
  verifyOtp: (email: string, code: string) => api.post("/auth/otp/verify", { email, code }),
};
