"use client";
import Image from "next/image";
import { useAuth } from "../context/AuthContext";
import LoginForm from "../components/login-form"; // Importing the LoginForm component

// export default function Home() {
//   const { user, login, logout } = useAuth();

//   return (
//     <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
//       <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">

//             {user ? (
//               <div>
//                 <p>Welcome, {user.name}!</p>
//                 <button
//                   className="bg-red-500 text-white px-4 py-2 rounded"
//                   onClick={logout}
//                 >
//                   Logout
//                 </button>
//               </div>
//             ) : (
//               <LoginForm/>
//             )}

//       </main>
//     </div>
//   );
// }

// "use client"

import Link from "next/link"
import { Navigation } from "../components/navigation"
import WaitlistForm from "@/components/wait-list-form";

export default function Home() {
  return (
    <div className="min-h-screen bg-white">

      {/* Hero Section */}
      <section className="px-6 py-20 max-w-6xl mx-auto">
        <div className="text-center space-y-8">
          <h1 className="text-5xl md:text-7xl font-bold text-gray-900 leading-tight">Accountant Management Systems Don't Have To Be Dull</h1>

          <p className="text-2xl md:text-3xl leading-relaxed max-w-4xl mx-auto">
            <span className="bg-gradient-to-r from-orange-500 via-purple-500 to-blue-500 bg-clip-text text-transparent">
              Domain Specific AI for Accounting Firms and Finance Teams.
            </span>
          </p>

          <div className="pt-8">
            {/* <Link
              href="/login"
              className="bg-black text-white px-8 py-4 rounded-full text-lg font-medium hover:bg-gray-800 transition-colors inline-block"
            >
              Try Artifact
            </Link> */}
            <WaitlistForm />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-6 py-16 max-w-6xl mx-auto">
        <div className="grid md:grid-cols-3 gap-12">
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900">Bookkeeping Reimagined</h3>
            <p className="text-gray-600 leading-relaxed">
              Get instant reconciliation & real-time categorisation with our global bookkeeping engine.
            </p>
          </div>

          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900">AI-Powered Insights & Forecasting</h3>
            <p className="text-gray-600 leading-relaxed">Plan better with data-driven CFO-level intelligence</p>
          </div>

          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900">Seamless Automation & Compliance</h3>
            <p className="text-gray-600 leading-relaxed">
              Automate invoices and tax filings with AI-driven accuracy—reducing errors and keeping you audit-ready.
            </p>
          </div>
        </div>
      </section>

    
      {/* Introducing Arti Section */}
      <section className="px-6 py-20 max-w-6xl mx-auto">
        <div className="grid md:grid-cols-2 gap-16 items-center">
          <div className="space-y-6">
            <h2 className="text-4xl font-bold text-gray-900">
              Introducing{" "}
              <span className="bg-gradient-to-r from-orange-500 to-purple-500 bg-clip-text text-transparent">Arti</span>
            </h2>
            <h3 className="text-2xl font-semibold text-gray-900">Your Personal Accountant</h3>
          </div>

          <div className="space-y-4">
            <p className="text-gray-600 leading-relaxed">
              Arti is your AI assistant designed to streamline and automate the entire accounting process.{" "}
              <span className="text-blue-600">Beyond automation</span>, Arti provides{" "}
              <span className="text-purple-600">predictive insights</span>, delivering real-time financial insights,
              increasing margins, revenue, and customer satisfaction across your firm's services.
            </p>
          </div>
        </div>
      </section>

      {/* Key Features Section */}
      <section className="px-6 py-20 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-16">Key features</h2>

        <div className="space-y-16">
          <div className="grid md:grid-cols-2 gap-16 items-start">
            <div className="space-y-6">
              <h3 className="text-2xl font-bold text-gray-900">
                Use{" "}
                <span className="bg-gradient-to-r from-orange-500 to-purple-500 bg-clip-text text-transparent">
                  Arti
                </span>{" "}
                locally
              </h3>
              <h4 className="text-xl font-semibold text-gray-900">No more outsourcing your key functions.</h4>
            </div>

            <div className="space-y-4">
              <p className="text-gray-600 leading-relaxed">
                Stop relying on offshore bookkeepers and third-party services.{" "}
                <span className="text-blue-600">Arti</span> automates bookkeeping and financial insights in-house,
                keeping your data secure, accurate, and fully under your control.
              </p>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {[
              {
                title: "Keep Your Data Secure",
                description: "All data is stored privately in your own environment, ensuring complete data security.",
              },
              {
                title: "Eliminate Delays & Errors",
                description: "Get real-time insights and eliminate human error with automated accuracy and efficiency.",
              },
              {
                title: "Reduce Costs Without Hiring",
                description:
                  "Scale your accounting operations without adding staff, reducing your operational costs significantly.",
              },
              {
                title: "Increase Revenue",
                description:
                  "Improve margins, revenue and client satisfaction across all accounting, advisory and audit engagements.",
              },
              {
                title: "HMRC Recognised",
                description: "We are HMRC Recognised and able to support Tax and returns.",
              },
              {
                title: "Stay Compliant & Informed",
                description:
                  "All invoices, tax filings, reconciliations, and financial reports are handled with AI-driven accuracy and compliance.",
              },
            ].map((feature, index) => (
              <div key={index} className="space-y-3">
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-purple-100 rounded-full flex items-center justify-center mt-1 flex-shrink-0">
                    <div className="w-2 h-2 bg-purple-600 rounded-full"></div>
                  </div>
                  <div>
                    <h5 className="font-semibold text-gray-900">{feature.title}</h5>
                    <p className="text-gray-600 text-sm leading-relaxed">{feature.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-6 py-20 text-center">
        <Link
          href="/login"
          className="bg-black text-white px-8 py-4 rounded-full text-lg font-medium hover:bg-gray-800 transition-colors inline-block"
        >
          Get started with Artifact
        </Link>
      </section>
    </div>
  )
}
