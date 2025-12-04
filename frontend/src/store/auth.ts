import { create } from 'zustand';
import { authApi } from '@/lib/api';

interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
}

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  _hasHydrated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, full_name: string) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isLoading: true,
  isAuthenticated: false,
  _hasHydrated: false,

  login: async (email: string, password: string) => {
    const data = await authApi.login(email, password);
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
    }
    
    const user = await authApi.getCurrentUser();
    set({ user, isAuthenticated: true, isLoading: false });
  },

  register: async (email: string, password: string, full_name: string) => {
    await authApi.register(email, password, full_name);
    // Auto-login after registration
    const data = await authApi.login(email, password);
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
    }
    
    const user = await authApi.getCurrentUser();
    set({ user, isAuthenticated: true, isLoading: false });
  },

  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
    set({ user: null, isAuthenticated: false });
  },

  checkAuth: async () => {
    const state = get();
    
    // If already authenticated with user data, skip check
    if (state.isAuthenticated && state.user) {
      return;
    }

    // If already checking (loading), skip
    if (state.isLoading && state._hasHydrated) {
      return;
    }

    set({ _hasHydrated: true, isLoading: true });

    if (typeof window === 'undefined') {
      set({ isLoading: false, isAuthenticated: false });
      return;
    }

    const token = localStorage.getItem('access_token');
    if (!token) {
      set({ isLoading: false, isAuthenticated: false });
      return;
    }

    try {
      const user = await authApi.getCurrentUser();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch (error) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      set({ user: null, isAuthenticated: false, isLoading: false });
    }
  },
}));
