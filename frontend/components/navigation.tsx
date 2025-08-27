"use client"

import Link from "next/link"
import { useAuth } from "../context/AuthContext";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { accountantsAPI } from "../lib/api";
import { Roles } from "../lib/roles";

export function Navigation() {
  const { user, logout } = useAuth()
  const pathname = usePathname();
  const [firstName, setFirstName] = useState<string>("");

  useEffect(() => {
    const fetchUserInfo = async () => {
      if (user && user.role !== Roles.ROOT_ADMIN) {
        try {
          // Get the accountant record to get the first name
          const accountants = await accountantsAPI.getAll();
          const userAccountant = accountants.find(acc => acc.user_id === user.id);
          if (userAccountant?.first_name) {
            setFirstName(userAccountant.first_name);
          }
        } catch (error) {
          console.error('Failed to fetch user info:', error);
        }
      }
    };

    fetchUserInfo();
  }, [user]);

  if (pathname === "/login") {
    return null;
  }

  const getWelcomeMessage = () => {
    if (!user) return "";
    if (user.role === Roles.ROOT_ADMIN) return `Welcome, Admin`;
    if (firstName) return `Welcome, ${firstName}`;
    return `Welcome, ${user.username}`;
  };

  return (
    <nav className="flex items-center justify-between px-6 py-4 bg-white border-b border-gray-100">
      <div className="flex items-center space-x-2">
        <div className="w-8 h-8 bg-black rounded-sm flex items-center justify-center">
          <span className="text-white font-bold text-sm">A</span>
        </div>
        <span className="text-xl font-semibold text-gray-900">Apex AM</span>
      </div>

      <div className="hidden md:flex items-center space-x-8">
        {user && pathname !== "/" ? 
        null 
        :
          (<>
            <Link href="#about" className="text-gray-600 hover:text-gray-900 transition-colors">
              About us
            </Link>
            <Link href="#blog" className="text-gray-600 hover:text-gray-900 transition-colors">
              Blog
            </Link>
            <Link href="#contact" className="text-gray-600 hover:text-gray-900 transition-colors">
              Contact
            </Link>
          </>)
        }
      </div>

      <div className="flex items-center space-x-4">
        {user ? (
          <div className="flex items-center space-x-4">
            <span className="text-gray-600">{getWelcomeMessage()}</span>
            <Link href="/dashboard" className="text-gray-600 hover:text-gray-900 transition-colors">
              Dashboard
            </Link>
            <button onClick={logout} className="text-gray-600 hover:text-gray-900 transition-colors">
              Logout
            </button>
          </div>
        ) : (
          <>
            <Link href="/login" className="text-gray-600 hover:text-gray-900 transition-colors">
              Login
            </Link>
            <Link
              href="/login"
              className="bg-black text-white px-4 py-2 rounded-full hover:bg-gray-800 transition-colors"
            >
              Get started
            </Link>
          </>
        )}
      </div>
    </nav>
  )
}
