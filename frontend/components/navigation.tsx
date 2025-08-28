"use client"

import Link from "next/link"
import { useAuth } from "../context/AuthContext";
import { usePathname } from "next/navigation";
import { UserDropdown } from "./user-dropdown";

export function Navigation() {
  const { user } = useAuth()
  const pathname = usePathname();

  if (pathname === "/login") {
    return null;
  }



  return (
    <nav className="flex items-center justify-between px-8 py-5 bg-white/95 backdrop-blur-sm border-b border-gray-200/50 shadow-sm sticky top-0 z-50">
      {/* Logo Section */}
      <div className="flex items-center space-x-3 group">
        <div className="w-10 h-10 bg-gradient-to-br from-orange-500 via-purple-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300 transform group-hover:scale-105">
          <span className="text-white font-bold text-lg">A</span>
        </div>
        <span className="text-2xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
          Apex AM
        </span>
      </div>

      {/* Center Navigation - Demo Mode Indicator */}
      <div className="hidden md:flex items-center space-x-8">
        {user && (
          <div className="flex items-center space-x-2 px-3 py-1 bg-gradient-to-r from-orange-100 to-purple-100 border border-orange-200 rounded-full">
            <div className="w-2 h-2 bg-orange-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-medium text-orange-700">Demo Mode</span>
          </div>
        )}
      </div>

      {/* Right Side - User Actions */}
      <div className="flex items-center space-x-6">
        {user ? (
          <div className="flex items-center space-x-6">
            <Link 
              href="/dashboard" 
              className="text-gray-700 hover:text-orange-500 font-medium transition-all duration-200 hover:scale-105"
            >
              Dashboard
            </Link>
            <UserDropdown />
          </div>
        ) : (
          <>
            <Link 
              href="/login" 
              className="text-gray-700 hover:text-orange-500 font-medium transition-all duration-200 hover:scale-105"
            >
              Login
            </Link>
            <Link
              href="/login"
              className="bg-gradient-to-r from-orange-500 via-purple-500 to-blue-600 text-white px-6 py-3 rounded-full font-semibold hover:from-orange-600 hover:via-purple-600 hover:to-blue-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 hover:-translate-y-0.5"
            >
              Get Started
            </Link>
          </>
        )}
      </div>
    </nav>
  )
}
