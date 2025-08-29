"use client";

import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useRouter } from 'next/navigation';
import { businessesAPI, accountantsAPI } from '../../lib/api';
import { Business, Accountant } from '../../types';
import BusinessCard from '../../components/business-card';
import ManageSuperDashboard from '../../components/manage-super-dashboard';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { Roles } from '../../lib/roles';

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(9);
  const [activeTab, setActiveTab] = useState("businesses");
  const [accountants, setAccountants] = useState<Accountant[]>([]);

  const fetchBusinesses = useCallback(async () => {
    if (!user) return;
    
    try {
      setLoading(true);
      let businessesData: Business[];

      if (user.role === Roles.ROOT_ADMIN) {
        // Root admin can see all businesses
        businessesData = await businessesAPI.getAll();
      } else if (user.role === Roles.SUPER_ACCOUNTANT) {
        // Super accountant can see businesses they manage
        businessesData = await businessesAPI.getAll();
      } else {
        // Regular accountant can only see their own businesses
        businessesData = await businessesAPI.getUserBusinesses(user.id);
      }

      setBusinesses(businessesData);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch businesses:', err);
      setError('Failed to load businesses');
    } finally {
      setLoading(false);
    }
  }, [user]);

  const fetchAccountants = useCallback(async () => {
    if (!user) return;
    
    try {
      const accountantsData = await accountantsAPI.getAll();
      setAccountants(accountantsData);
    } catch (err) {
      console.error('Failed to fetch accountants:', err);
    }
  }, [user]);

  // Add useEffect after function definitions to avoid dependency issues
  useEffect(() => {
    if (!user) {
      router.push('/login');
      return;
    }

    fetchBusinesses();
    fetchAccountants();
  }, [user, router, fetchBusinesses, fetchAccountants]);

  // Filter businesses based on search term
  const filteredBusinesses = businesses.filter(business =>
    business.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Pagination logic
  const totalPages = Math.ceil(filteredBusinesses.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentBusinesses = filteredBusinesses.slice(startIndex, endIndex);

  // Reset to first page when search changes
  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm]);

  if (!user) {
    return null;
  }

  // Define tabs based on user role
  const getTabsByRole = () => {
    if (user.role === Roles.ROOT_ADMIN) {
      return [
        { value: "businesses", label: "Businesses", content: <BusinessDashboardContent businesses={currentBusinesses} searchTerm={searchTerm} setSearchTerm={setSearchTerm} currentPage={currentPage} setCurrentPage={setCurrentPage} totalPages={totalPages} totalBusinesses={filteredBusinesses.length} onRefresh={fetchBusinesses} /> },
        { value: "manageSuper", label: "Accountants", content: <ManageSuperDashboard /> },
      ];
    } else if (user.role === Roles.SUPER_ACCOUNTANT || user.role === Roles.ACCOUNTANT) {
      return [
        { value: "businesses", label: "Businesses", content: <BusinessDashboardContent businesses={currentBusinesses} searchTerm={searchTerm} setSearchTerm={setSearchTerm} currentPage={currentPage} setCurrentPage={setCurrentPage} totalPages={totalPages} totalBusinesses={filteredBusinesses.length} onRefresh={fetchBusinesses} /> }
      ];
    }
  };

  const userTabs = getTabsByRole() || [];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-8xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Dashboard
          </h1>
          
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            </div>
          </div>
        )}

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="bg-white rounded-lg shadow-sm p-6 animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-2/3"></div>
              </div>
            ))}
          </div>
        ) : businesses.length > 0 ? (
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-2 lg:w-auto lg:grid-cols-2 bg-gradient-to-r from-blue-50 to-purple-50 p-1 rounded-xl border border-blue-200 shadow-sm">
              {userTabs?.map((tab) => (
                <TabsTrigger 
                  key={tab.value} 
                  value={tab.value}
                  className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-500 data-[state=active]:to-purple-600 data-[state=active]:text-white data-[state=active]:shadow-md data-[state=active]:scale-105 text-gray-700 hover:text-blue-600 transition-all duration-300 font-semibold text-sm px-4 py-2 rounded-lg hover:bg-blue-100 hover:scale-102"
                >
                  {tab.label}
                </TabsTrigger>
              ))}
            </TabsList>
            {userTabs?.map((tab) => (
              <TabsContent key={tab.value} value={tab.value} className="mt-6">
                {tab.content}
              </TabsContent>
            ))}
          </Tabs>
        ) : (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No businesses found</h3>
            <p className="text-gray-500">
              {user.role === Roles.ACCOUNTANT 
                ? "You don't have any businesses assigned yet."
                : "No businesses have been created yet."
              }
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

// Business Dashboard Component
function BusinessDashboardContent({ 
  businesses, 
  searchTerm, 
  setSearchTerm, 
  currentPage, 
  setCurrentPage, 
  totalPages, 
  totalBusinesses,
  onRefresh
}: { 
  businesses: Business[];
  searchTerm: string;
  setSearchTerm: (term: string) => void;
  currentPage: number;
  setCurrentPage: (page: number) => void;
  totalPages: number;
  totalBusinesses: number;
  onRefresh: () => void;
}) {
  return (
    <div className="w-full space-y-6">
      {/* Search Bar */}
      <div className="w-full flex justify-center items-center space-x-4">
        <div className="flex-1 max-w-md">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              type="text"
              placeholder="Search businesses..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
        </div>
        <div className="text-sm text-gray-500 flex-shrink-0">
          {totalBusinesses} business{totalBusinesses !== 1 ? 'es' : ''} found
        </div>
      </div>

      {/* Business Cards Grid */}
      <div className="w-full">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {businesses.map((business) => (
            <BusinessCard 
              key={business.id} 
              business={business}
              onRefresh={onRefresh}
            />
          ))}
        </div>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="w-full flex items-center justify-between">
          <div className="text-sm text-gray-700">
            Showing page {currentPage} of {totalPages}
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
              disabled={currentPage === 1}
              className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <div className="flex items-center space-x-1">
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <button
                  key={page}
                  onClick={() => setCurrentPage(page)}
                  className={`px-3 py-2 text-sm font-medium rounded-md ${
                    currentPage === page
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-500 bg-white border border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  {page}
                </button>
              ))}
            </div>
            <button
              onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
              disabled={currentPage === totalPages}
              className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}