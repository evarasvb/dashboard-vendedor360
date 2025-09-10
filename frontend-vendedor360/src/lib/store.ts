import { create } from "zustand";

interface User {
  email: string;
  name?: string;
}

interface Filters {
  q?: string;
  categoria?: string;
  fechaDesde?: string;
  fechaHasta?: string;
}

interface AppState {
  user: User | null;
  setUser: (u: User | null) => void;
  filters: Filters;
  setFilters: (f: Partial<Filters>) => void;
  sidebarOpen: boolean;
  setSidebarOpen: (v: boolean) => void;
}

export const useApp = create<AppState>((set) => ({
  user: null,
  setUser: (u) => set({ user: u }),
  filters: {},
  setFilters: (f) => set((s) => ({ filters: { ...s.filters, ...f } })),
  sidebarOpen: false,
  setSidebarOpen: (v) => set({ sidebarOpen: v }),
}));
