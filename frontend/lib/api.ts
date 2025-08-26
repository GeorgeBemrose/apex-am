// API service layer for communicating with FastAPI backend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
const API_TIMEOUT = parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || '10000');

// Types
export interface User {
  id: number;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface Business {
  id: number;
  name: string;
  description?: string;
  owner_id: number;
  accountant_id?: number;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  owner: User;
  accountant?: Accountant;
  financial_metrics?: BusinessFinancialMetrics;
  metrics?: BusinessMetrics;
}

export interface Accountant {
  id: number;
  user_id: number;
  super_accountant_id?: number;
  is_super_accountant: boolean;
  first_name?: string;
  last_name?: string;
  created_at: string;
  updated_at?: string;
  user: User;
}

export interface BusinessFinancialMetrics {
  id: number;
  business_id: number;
  revenue: number;
  gross_profit: number;
  net_profit: number;
  total_costs: number;
  percentage_change_revenue: number;
  percentage_change_gross_profit: number;
  percentage_change_net_profit: number;
  percentage_change_total_costs: number;
  created_at: string;
  updated_at?: string;
}

export interface BusinessMetrics {
  id: number;
  business_id: number;
  documents_due: number;
  outstanding_invoices: number;
  pending_approvals: number;
  accounting_year_end: string;
  created_at: string;
  updated_at?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface ApiError {
  detail: string;
}

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

  getById: async (id: number): Promise<User> => {
    return apiRequest<User>(`/users/${id}`);
  },

  update: async (id: number, userData: Partial<User>): Promise<User> => {
    return apiRequest<User>(`/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  },

  assignRole: async (userId: number, roleData: { new_role: string; super_accountant_id?: number }): Promise<User> => {
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

  getById: async (id: number): Promise<Accountant> => {
    return apiRequest<Accountant>(`/accountants/${id}`);
  },

  create: async (accountantData: Partial<Accountant>): Promise<Accountant> => {
    return apiRequest<Accountant>('/accountants/', {
      method: 'POST',
      body: JSON.stringify(accountantData),
    });
  },

  update: async (id: number, accountantData: Partial<Accountant>): Promise<Accountant> => {
    return apiRequest<Accountant>(`/accountants/${id}`, {
      method: 'PUT',
      body: JSON.stringify(accountantData),
    });
  },

  delete: async (id: number): Promise<void> => {
    return apiRequest<void>(`/accountants/${id}`, {
      method: 'DELETE',
    });
  },

  assignSuperAccountant: async (accountantId: number, superAccountantId: number): Promise<Accountant> => {
    return apiRequest<Accountant>(`/accountants/${accountantId}/assign-super`, {
      method: 'POST',
      body: JSON.stringify({ super_accountant_id: superAccountantId }),
    });
  },

  removeSuperAccountant: async (accountantId: number): Promise<Accountant> => {
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

  getById: async (id: number): Promise<Business> => {
    return apiRequest<Business>(`/businesses/${id}`);
  },

  create: async (businessData: Partial<Business>): Promise<Business> => {
    return apiRequest<Business>('/businesses/', {
      method: 'POST',
      body: JSON.stringify(businessData),
    });
  },

  update: async (id: number, businessData: Partial<Business>): Promise<Business> => {
    return apiRequest<Business>(`/businesses/${id}`, {
      method: 'PUT',
      body: JSON.stringify(businessData),
    });
  },

  delete: async (id: number): Promise<void> => {
    return apiRequest<void>(`/businesses/${id}`, {
      method: 'DELETE',
    });
  },

  getUserBusinesses: async (userId: number): Promise<Business[]> => {
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
