"use client";

import React from 'react';
import { useAuth } from '../../context/AuthContext';
import LoginForm from '../../components/login-form';
import { useRouter } from "next/navigation"
import { useEffect } from "react"
import Link from 'next/link'

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
            <div className="w-8 h-8 bg-gradient-to-r from-orange-500 to-purple-500 rounded-sm flex items-center justify-center">
              <span className="text-white font-bold text-sm">A</span>
            </div>
            <Link
              href="/"
              className="text-gray-900 hover:text-orange-500 font-medium transition-colors"
            >
              <span className="text-2xl font-semibold">Apex AM</span>
            </Link>
          </div>
          <h2 className="text-3xl font-bold text-gray-900">Sign in to your account</h2>
        </div>
        <LoginForm />
      </div>
    </div>
  )
}

