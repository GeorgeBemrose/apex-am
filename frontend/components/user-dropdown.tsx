"use client"

import { useState, useRef, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Roles } from '../lib/roles';

interface DemoUser {
  email: string;
  password: string;
  role: string;
  displayName: string;
  color: string;
}

const demoUsers: DemoUser[] = [
  {
    email: 'admin@example.com',
    password: 'password',
    role: Roles.ROOT_ADMIN,
    displayName: 'Root Admin',
    color: 'from-red-500 to-red-600'
  },
  {
    email: 'super@example.com',
    password: 'password',
    role: Roles.SUPER_ACCOUNTANT,
    displayName: 'Super Accountant',
    color: 'from-purple-500 to-purple-600'
  },
  {
    email: 'p.jones@example.com',
    password: 'password',
    role: Roles.ACCOUNTANT,
    displayName: 'P. Jones (Accountant)',
    color: 'from-blue-500 to-blue-600'
  }
];

export function UserDropdown() {
  const { user, login, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [isSwitching, setIsSwitching] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleUserSwitch = async (demoUser: DemoUser) => {
    if (isSwitching) return;
    
    setIsSwitching(true);
    try {
      // Logout current user if any
      if (user) {
        logout();
      }
      
      // Login as new demo user
      const success = await login(demoUser.email, demoUser.password);
      if (success) {
        setIsOpen(false);
      }
    } catch (error) {
      console.error('Failed to switch user:', error);
    } finally {
      setIsSwitching(false);
    }
  };

  const getCurrentUserInfo = () => {
    if (!user) return null;
    return demoUsers.find(demo => demo.email === user.email);
  };

  const currentUser = getCurrentUserInfo();

  return (
    <div className="relative" ref={dropdownRef}>
      {/* User Avatar Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 p-2 rounded-full hover:bg-gray-100 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-orange-500"
        disabled={isSwitching}
      >
        <div className={`w-8 h-8 rounded-full bg-gradient-to-r ${currentUser?.color || 'from-gray-400 to-gray-500'} flex items-center justify-center text-white font-semibold text-sm`}>
          {currentUser ? currentUser.displayName.charAt(0) : 'U'}
        </div>
        <div className="hidden sm:block text-left">
          <div className="text-sm font-medium text-gray-700">
            {currentUser ? currentUser.displayName : 'Guest'}
          </div>
          <div className="text-xs text-gray-500">
            {currentUser ? currentUser.role.replace('_', ' ').toLowerCase() : 'Not logged in'}
          </div>
        </div>
        <svg
          className={`w-4 h-4 text-gray-400 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
          {/* Current User Info */}
          {currentUser && (
            <div className="px-4 py-3 border-b border-gray-100">
              <div className="flex items-center space-x-3">
                <div className={`w-10 h-10 rounded-full bg-gradient-to-r ${currentUser.color} flex items-center justify-center text-white font-semibold`}>
                  {currentUser.displayName.charAt(0)}
                </div>
                <div>
                  <div className="font-medium text-gray-900">{currentUser.displayName}</div>
                  <div className="text-sm text-gray-500">{currentUser.email}</div>
                  <div className="text-xs text-gray-400 capitalize">
                    {currentUser.role.replace('_', ' ')}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Demo User Options */}
          <div className="px-2 py-1">
            <div className="text-xs font-medium text-gray-500 px-3 py-1 mb-2">
              Quick Switch Demo Users
            </div>
            {demoUsers.map((demoUser) => (
              <button
                key={demoUser.email}
                onClick={() => handleUserSwitch(demoUser)}
                disabled={isSwitching || (currentUser?.email === demoUser.email)}
                className={`w-full flex items-center space-x-3 px-3 py-2 rounded-md text-left transition-all duration-200 ${
                  currentUser?.email === demoUser.email
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <div className={`w-6 h-6 rounded-full bg-gradient-to-r ${demoUser.color} flex items-center justify-center text-white text-xs font-semibold`}>
                  {demoUser.displayName.charAt(0)}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-sm truncate">{demoUser.displayName}</div>
                  <div className="text-xs text-gray-500 truncate">{demoUser.email}</div>
                </div>
                {currentUser?.email === demoUser.email && (
                  <svg className="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                )}
              </button>
            ))}
          </div>

          {/* Logout Option */}
          {currentUser && (
            <div className="border-t border-gray-100 pt-2">
              <button
                onClick={() => {
                  logout();
                  setIsOpen(false);
                }}
                className="w-full flex items-center space-x-3 px-3 py-2 text-left text-red-600 hover:bg-red-50 rounded-md transition-all duration-200"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span className="font-medium">Logout</span>
              </button>
            </div>
          )}

          {/* Loading State */}
          {isSwitching && (
            <div className="px-4 py-3 text-center">
              <div className="inline-flex items-center space-x-2 text-sm text-gray-500">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-orange-500"></div>
                <span>Switching user...</span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
