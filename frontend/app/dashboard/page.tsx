"use client";
// / Importing the LoginForm component
import { useEffect } from "react";
import { useRouter } from "next/navigation"
import { useAuth } from "../../context/AuthContext";
import RootAdminDashboard from "../../components/root-admin-dashboard";
import SuperAccountantDashboard from "../../components/super-accountant-dashboard";
import AccountantDashboard from "@/components/accountant-dashboard";

export default function Home() {
    const { user, login, logout } = useAuth();
    const router = useRouter()

    useEffect(() => {
        if (!user) {
            router.push("/login")
        }
    }, [user, router])

    const userRole = user ? user.role : null;
    const userName = user ? user.name : null;
    return (
        <>
            {userName && (
                <p className="text-black">
                    Hello {user.name}, you have role: {user.role}
                </p>)}

            {userRole && (
                (() => {
                    switch (userRole) {
                        case 'root_admin':
                            return (<RootAdminDashboard />);
                        case 'super_accountant':
                            return (<SuperAccountantDashboard/>);
                        case 'accountant':
                            return (<AccountantDashboard/>);
                        default:
                            return (<p className="text-black">Role not recognized.</p>);
                    }
                })()
            )}
        </>
    );
}
