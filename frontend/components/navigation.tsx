"use client"

import Link from "next/link"
import { useAuth } from "../context/AuthContext";
import { usePathname } from "next/navigation";

export function Navigation() {
  const { user, logout } = useAuth()
  const pathname = usePathname();

  if (pathname === "/login") {
    return null; // Don't render navigation on the login page
  }

  return (
    <nav className="flex items-center justify-between px-6 py-4 bg-white border-b border-gray-100">
      <div className="flex items-center space-x-2">
        <div className="w-8 h-8 bg-black rounded-sm flex items-center justify-center">
          <span className="text-white font-bold text-sm">A</span>
        </div>
        <span className="text-xl font-semibold text-gray-900">Apex AM</span>
      </div>

      <div className="hidden md:flex items-center space-x-8">
        <Link href="#about" className="text-gray-600 hover:text-gray-900 transition-colors">
          About us
        </Link>
        <Link href="#blog" className="text-gray-600 hover:text-gray-900 transition-colors">
          Blog
        </Link>
        <Link href="#contact" className="text-gray-600 hover:text-gray-900 transition-colors">
          Contact
        </Link>
      </div>

      <div className="flex items-center space-x-4">
        {user ? (
          <div className="flex items-center space-x-4">
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
