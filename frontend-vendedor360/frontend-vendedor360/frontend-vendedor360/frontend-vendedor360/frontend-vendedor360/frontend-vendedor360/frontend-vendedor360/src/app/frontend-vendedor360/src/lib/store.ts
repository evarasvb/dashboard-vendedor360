import { create } from "zustand";

type User = { email: string; name?: string } | null;
type Filters = { q?: string; categoria?: string; fechaDesde?: string; fechaHasta?: string };

type AppState = {
  user: User;
  setUser: (u: User) => void;
  filters: Filters;
  setFilters: (f: Partial<Filters>) => void;
  sidebarOpen: boolean;
  setSidebarOpen: (v: boolean) => void;
};

export const useApp = create<AppState>((set) => ({
  user: null,
  setUser: (u) => set({ user: u }),
  filters: {},
  setFilters: (f) => set((s) => ({ filters: { ...s.filters, ...f } })),
  sidebarOpen: false,
  setSidebarOpen: (v) => set({ sidebarOpen: v }),
}));
