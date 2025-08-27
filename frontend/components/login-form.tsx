"use client"

import React from "react"

import { useState } from "react"
import { Button, TextField, Card, CardContent, Alert, InputAdornment, IconButton } from "@mui/material"
import { useAuth } from "../context/AuthContext"
import { EyeIcon, EyeSlashIcon, ExclamationCircleIcon } from "@heroicons/react/24/outline"

const LoginForm = () => {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [showPassword, setShowPassword] = useState(false)
    const { login, loading, error } = useAuth()



    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        e.stopPropagation()
        
        await login(email, password)
    }

    return (
        <>
        <div className="space-y-4">
            <div>
                <input
                    id="email"
                    placeholder="Email Address*"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                            e.preventDefault();
                            handleSubmit(e as any);
                        }
                    }}
                    className={`w-full h-16 px-6 text-lg text-black bg-gray-50 border-2 ${error ? "border-red-500" : "border-gray-300"
                        } rounded-full placeholder-gray-500 focus:outline-none focus:bg-white ${error ? "focus:border-red-500" : "focus:border-gray-400"
                        } hover:border-gray-400 transition-colors`}
                />
            </div>

            <div className="relative">
                <input
                    type={showPassword ? "text" : "password"}
                    placeholder="Password*"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                            e.preventDefault();
                            handleSubmit(e as any);
                        }
                    }}
                    className={`w-full h-16 px-6 pr-14 text-lg text-black bg-gray-50 border-2 ${error ? "border-red-500" : "border-gray-300"
                        } rounded-full placeholder-gray-500 focus:outline-none focus:bg-white ${error ? "focus:border-red-500" : "focus:border-gray-400"
                        } hover:border-gray-400 transition-colors`} />
                <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 transition-colors"
                >
                    {showPassword ? <EyeSlashIcon className="h-5 w-5" /> : <EyeSlashIcon className="h-5 w-5" />}
                </button>
            </div>
            
            {error && (
                <div className="flex items-center gap-2 text-red-500 mt-2">
                    <ExclamationCircleIcon className="h-5 w-5" />
                    <span>{error}</span>
                </div>
            )}
            
            <div className="text-left">
                <a
                    href="#"
                    onClick={(e) => {
                        e.preventDefault();
                        alert("You should have remembered it!");
                    }}
                    className="text-blue-600 hover:text-blue-800 font-medium transition-colors"
                >
                    Forgot password?
                </a>
            </div>

            <button
                type="button"
                disabled={loading}
                onClick={handleSubmit}
                className={`w-full h-16 text-lg font-medium text-white rounded-full transition-colors ${
                    loading 
                        ? 'bg-gray-400 cursor-not-allowed' 
                        : 'bg-slate-800 hover:bg-slate-900'
                }`}
            >
                {loading ? 'Logging in...' : 'Login'}
            </button>
            
            <div className="text-center text-sm text-black">
                Don&apos;t have an account?{" "}
                <a href="#" className="underline underline-offset-4">
                    Sign up
                </a>
            </div>

        </div>
        <div className="text-blue-600 *:[a]:hover:text-primary text-center text-xs text-balance *:[a]:underline *:[a]:underline-offset-4">
        By clicking continue, you agree to our <a href="#">Terms of Service</a>{" "}
        and <a href="#">Privacy Policy</a>.
      </div>
      </>
    )
}
export default LoginForm;
