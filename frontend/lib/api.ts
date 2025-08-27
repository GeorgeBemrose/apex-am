// API service layer for communicating with FastAPI backend
import { User, Business, Accountant, BusinessFinancialMetrics, BusinessMetrics, LoginCredentials, AuthResponse, ApiError } from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
const API_TIMEOUT = parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || '10000');

// Utility functions
const getAuthHeaders = (): HeadersInit => {
  const token = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
  };
};

const handleResponse = async (response: Response) => {
  if (!response.ok) {
    const errorData: ApiError = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }
  return response.json();
};

const apiRequest = async <T>(
  endpoint: string, 
  options: RequestInit = {}
): Promise<T> => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      signal: controller.signal,
      headers: getAuthHeaders(),
    });
    
    clearTimeout(timeoutId);
    return await handleResponse(response);
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Network error');
  }
};

// Authentication API
export const authAPI = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    return apiRequest<AuthResponse>('/auth/login-json', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  },

  getCurrentUser: async (): Promise<User> => {
    return apiRequest<User>('/users/me');
  },
};

// Users API
export const usersAPI = {
  getAll: async (): Promise<User[]> => {
    return apiRequest<User[]>('/users/');
  },

  getById: async (id: string): Promise<User> => {
    return apiRequest<User>(`/users/${id}`);
  },

  update: async (id: string, userData: Partial<User>): Promise<User> => {
    return apiRequest<User>(`/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  },

  assignRole: async (userId: string, roleData: { new_role: string; super_accountant_id?: string }): Promise<User> => {
    return apiRequest<User>(`/users/${userId}/assign-role`, {
      method: 'POST',
      body: JSON.stringify(roleData),
    });
  },
};

// Accountants API
export const accountantsAPI = {
  getAll: async (): Promise<Accountant[]> => {
    return apiRequest<Accountant[]>('/accountants/');
  },

  getById: async (id: string): Promise<Accountant> => {
    return apiRequest<Accountant>(`/accountants/${id}`);
  },

  create: async (accountantData: Partial<Accountant>): Promise<Accountant> => {
    return apiRequest<Accountant>('/accountants/', {
      method: 'POST',
      body: JSON.stringify(accountantData),
    });
  },

  update: async (id: string, accountantData: Partial<Accountant>): Promise<Accountant> => {
    return apiRequest<Accountant>(`/accountants/${id}`, {
      method: 'PUT',
      body: JSON.stringify(accountantData),
    });
  },

  delete: async (id: string): Promise<void> => {
    return apiRequest<void>(`/accountants/${id}`, {
      method: 'DELETE',
    });
  },

  assignSuperAccountant: async (accountantId: string, superAccountantId: string): Promise<Accountant> => {
    return apiRequest<Accountant>(`/accountants/${accountantId}/assign-super`, {
      method: 'POST',
      body: JSON.stringify({ super_accountant_id: superAccountantId }),
    });
  },

  removeSuperAccountant: async (accountantId: string): Promise<Accountant> => {
    return apiRequest<Accountant>(`/accountants/${accountantId}/remove-super`, {
      method: 'POST',
    });
  },
};

// Businesses API
export const businessesAPI = {
  getAll: async (): Promise<Business[]> => {
    return apiRequest<Business[]>('/businesses/');
  },

  getById: async (id: string): Promise<Business> => {
    return apiRequest<Business>(`/businesses/${id}`);
  },

  create: async (businessData: Partial<Business>): Promise<Business> => {
    return apiRequest<Business>('/businesses/', {
      method: 'POST',
      body: JSON.stringify(businessData),
    });
  },

  update: async (id: string, businessData: Partial<Business>): Promise<Business> => {
    return apiRequest<Business>(`/businesses/${id}`, {
      method: 'PUT',
      body: JSON.stringify(businessData),
    });
  },

  delete: async (id: string): Promise<void> => {
    return apiRequest<void>(`/businesses/${id}`, {
      method: 'DELETE',
    });
  },

  getUserBusinesses: async (userId: string): Promise<Business[]> => {
    return apiRequest<Business[]>(`/users/${userId}/businesses`);
  },
};

// Export all APIs
export const api = {
  auth: authAPI,
  users: usersAPI,
  accountants: accountantsAPI,
  businesses: businessesAPI,
};
