import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      if (typeof window !== 'undefined') {
        try {
          const refreshToken = localStorage.getItem('refresh_token');
          if (refreshToken) {
            const response = await axios.post(`${API_URL}/api/v1/auth/refresh`, {
              refresh_token: refreshToken,
            });

            const { access_token, refresh_token: newRefreshToken } = response.data;
            localStorage.setItem('access_token', access_token);
            localStorage.setItem('refresh_token', newRefreshToken);

            originalRequest.headers.Authorization = `Bearer ${access_token}`;
            return api(originalRequest);
          }
        } catch (refreshError) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          if (typeof window !== 'undefined') {
            window.location.href = '/login';
          }
          return Promise.reject(refreshError);
        }
      }
    }

    return Promise.reject(error);
  }
);

export const authApi = {
  login: async (email: string, password: string) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await axios.post(`${API_URL}/api/v1/auth/login`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  register: async (email: string, password: string, full_name: string) => {
    const response = await axios.post(`${API_URL}/api/v1/auth/register`, {
      email,
      password,
      full_name,
    });
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/api/v1/users/me');
    return response.data;
  },
};

export const organizationApi = {
  list: async () => {
    const response = await api.get('/api/v1/orgs/');
    return response.data;
  },

  create: async (name: string, slug: string, description?: string) => {
    const response = await api.post('/api/v1/orgs/', {
      name,
      slug,
      description,
    });
    return response.data;
  },

  get: async (orgId: number) => {
    const response = await api.get(`/api/v1/orgs/${orgId}`);
    return response.data;
  },

  update: async (orgId: number, data: { name?: string; description?: string }) => {
    const response = await api.patch(`/api/v1/orgs/${orgId}`, data);
    return response.data;
  },
};

export const aiApi = {
  getUsage: async (orgId: number) => {
    const response = await api.get('/api/v1/ai/usage', {
      headers: {
        'X-Current-Org': orgId.toString(),
      },
    });
    return response.data;
  },
};

export const billingApi = {
  getSubscription: async (orgId: number) => {
    const response = await api.get('/api/v1/billing/subscription', {
      headers: {
        'X-Current-Org': orgId.toString(),
      },
    });
    return response.data;
  },
};
