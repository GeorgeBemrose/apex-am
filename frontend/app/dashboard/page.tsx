"use client";
// / Importing the LoginForm component
import { useEffect } from "react";
import { useRouter } from "next/navigation"
import { useAuth } from "../../context/AuthContext";

export default function Home() {
    const { user, login, logout } = useAuth();
    const router = useRouter()

    useEffect(() => {
        if (!user) {
            router.push("/login")
        }
    }, [user, router])

    const userRole = user ? user.role : null;

    return (
        <>
            {user ? (
                <p className="text-black">
                    Hello {user.name}, you have role: {user.role}
                </p>
            ) : (
                <p className="text-black"> Please log in</p>
            )}
            {userRole && (
                <p className="text-black">
                    {(() => {
                        switch (userRole) {
                            case 'root_admin':
                                return 'You have ROOT_ADMIN access.';
                            case 'super_accountant':
                                return 'You have SUPER_ACCOUNTANT access.';
                            case 'accountant':
                                return 'You have ACCOUNTANT access.';
                            default:
                                return 'Role not recognized.';
                        }
                    })()}
                </p>
            )}
        </>
    );
}
