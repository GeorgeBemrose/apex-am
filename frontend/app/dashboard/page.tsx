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
    return (
        <>
            {user ? (
                <p className="text-black">
                    Hello {user.name}
                </p>
            ) :
                (<p className="text-black"> Please log in</p>)
            }
        </>
    );
}
