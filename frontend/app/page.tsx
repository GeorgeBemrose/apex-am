"use client";

import Link from "next/link"

export default function Home() {
  return (
    <div className="min-h-screen bg-white">

      {/* Hero Section */}
      <section className="px-6 py-20 max-w-6xl mx-auto">
        <div className="text-center space-y-8">
          <h1 className="text-5xl md:text-7xl font-bold text-gray-900 leading-tight">Apex AM: Modern Accounting Management</h1>

          <p className="text-2xl md:text-3xl leading-relaxed max-w-4xl mx-auto">
            <span className="bg-gradient-to-r from-orange-500 via-purple-500 to-blue-500 bg-clip-text text-transparent">
              Streamlined accounting management for modern firms and finance teams.
            </span>
          </p>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-6 py-16 max-w-6xl mx-auto">
        <div className="grid md:grid-cols-3 gap-12">
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900">Efficient Client Management</h3>
            <p className="text-gray-600 leading-relaxed">
              Manage your accounting clients with ease through our intuitive dashboard and workflow tools.
            </p>
          </div>

          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900">Smart Business Insights</h3>
            <p className="text-gray-600 leading-relaxed">Get real-time financial insights and analytics to drive better business decisions.</p>
          </div>

          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900">Automated Workflows</h3>
            <p className="text-gray-600 leading-relaxed">
              Streamline your accounting processes with automated workflows and compliance management.
            </p>
          </div>
        </div>
      </section>

    
      {/* Introducing Apex AM Section */}
      <section className="px-6 py-20 max-w-6xl mx-auto">
        <div className="grid md:grid-cols-2 gap-16 items-center">
          <div className="space-y-6">
            <h2 className="text-4xl font-bold text-gray-900">
              Welcome to{" "}
              <span className="bg-gradient-to-r from-orange-500 to-purple-500 bg-clip-text text-transparent">Apex AM</span>
            </h2>
            <h3 className="text-2xl font-semibold text-gray-900">Your Accounting Management Solution</h3>
          </div>

          <div className="space-y-4">
            <p className="text-gray-600 leading-relaxed">
              Apex AM is a comprehensive platform designed to streamline and modernize your accounting firm&apos;s operations.{" "}
              <span className="text-orange-500">Beyond basic management</span>, Apex AM provides{" "}
              <span className="text-purple-500">advanced analytics</span>, delivering real-time insights,
              increasing efficiency, and improving client satisfaction across your firm&apos;s services.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-6 py-20 text-center">
        <Link
          href="/login"
          className="bg-gradient-to-r from-orange-500 to-purple-500 text-white px-8 py-4 rounded-full text-lg font-medium hover:from-orange-600 hover:to-purple-600 transition-all duration-300 inline-block shadow-lg hover:shadow-xl"
        >
          Get Started with Apex AM
        </Link>
      </section>
    </div>
  )
}
