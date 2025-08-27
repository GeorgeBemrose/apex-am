"use client";

import { createContext, useState, useEffect, useContext, ReactNode } from "react";
import { authAPI } from "../lib/api";
import { User, LoginCredentials } from "../types";

type AuthContextType = {
    user: User | null;
    login: (email: string, password: string) => Promise<boolean>;
    logout: () => void;
    loading: boolean;
    error: string | null;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Check for existing token and fetch user data on mount
    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            fetchCurrentUser();
        }
    }, []);



    const fetchCurrentUser = async () => {
        try {
            const userData = await authAPI.getCurrentUser();
            setUser(userData);
            setError(null);
        } catch (err) {
            console.error('Failed to fetch current user:', err);
            // Token might be invalid, clear it
            localStorage.removeItem('access_token');
            setUser(null);
        }
    };

    const login = async (email: string, password: string): Promise<boolean> => {
        setLoading(true);
        setError(null);
        
        try {
            const credentials: LoginCredentials = {
                email: email,
                password: password
            };
            
            const authResponse = await authAPI.login(credentials);
            
            // Store the token
            localStorage.setItem('access_token', authResponse.access_token);
            
            // Fetch user data
            await fetchCurrentUser();
            
            return true;
        } catch (err) {
            console.error('Login failed:', err);
            const errorMessage = err instanceof Error ? err.message : 'Login failed';
            setError(errorMessage);
            
            // Clear any stored token on failed login
            localStorage.removeItem('access_token');
            setUser(null); // Ensure user state is cleared on failed login
            
            return false;
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        setUser(null);
        setError(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading, error }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};