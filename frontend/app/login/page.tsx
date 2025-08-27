"use client";

import React from 'react';
import { useAuth } from '../../context/AuthContext';
import LoginForm from '../../components/login-form';
import { useRouter } from "next/navigation"
import { useEffect } from "react"

export default function LoginPage() {
  const { user } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (user && user.id) {
      router.push("/dashboard");
    }
  }, [user, router])

  if (user) {
    return null
  }

  return (
    <div className="min-h-screen bg-white flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="flex items-center justify-center space-x-2 mb-6">
            <div className="w-8 h-8 bg-black rounded-sm flex items-center justify-center">
              <span className="text-white font-bold text-sm">A</span>
            </div>
            <a
              href="/"
              className="text-gray-900 hover:text-gray-700 font-medium transition-colors"
            >
              <span className="text-2xl font-semibold">Apex AM</span>
            </a>
          </div>
          <h2 className="text-3xl font-bold text-gray-900">Sign in to your account</h2>
        </div>
        <LoginForm />
      </div>
    </div>
  )
}

