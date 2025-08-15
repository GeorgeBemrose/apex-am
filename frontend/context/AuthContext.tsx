"use client";

import { createContext, useState, useEffect, useContext, ReactNode } from "react";
import { authenticateUser } from "../auth/mockAuth";

type AuthContextType = {
    user: any | null;
    login: (email: string, password: string) => Promise<boolean>;
    logout: () => void;
    loading: boolean;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<any | null>(null);
    const [userRole, setUserRole] = useState("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const savedUser = localStorage.getItem("user");
        const savedRole = localStorage.getItem("userRole");
    
        if (savedUser) {
          setUser(JSON.parse(savedUser));
        }
        if (savedRole) {
          setUserRole(savedRole);
        }
      }, []);

    const login = async (email: string, password: string): Promise<boolean> => {
        setLoading(true);
        try {
            const authenticatedUser = await authenticateUser(email, password);
            if (authenticatedUser) {
                setUser(authenticatedUser);
                setUserRole(authenticatedUser.role);
                localStorage.setItem("user", JSON.stringify(authenticatedUser));
                localStorage.setItem("userRole", authenticatedUser.role);
                return true;
            }
            return false;
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        localStorage.removeItem("user");
        localStorage.removeItem("userRole");
        setUser(null);
        setUserRole("");
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
};