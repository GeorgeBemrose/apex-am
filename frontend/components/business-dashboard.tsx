import React, { useState } from 'react';
import BusinessCard from './business-card';
import {
    Pagination,
    PaginationContent,
    PaginationEllipsis,
    PaginationItem,
    PaginationLink,
    PaginationNext,
    PaginationPrevious,
} from "@/components/ui/pagination";
import { Business } from '../types';


const ITEMS_PER_PAGE = 6;

interface AccountantDashboardProps {
    businesses: Business[];
}

const AccountantDashboard: React.FC<AccountantDashboardProps> = ({businesses}) => {
    const [currentPage, setCurrentPage] = useState(1);
    const [searchTerm, setSearchTerm] = useState(''); // BEGIN: Added searchTerm state
    const totalPages = Math.ceil(businesses.length / ITEMS_PER_PAGE);
    
    const handleNextPage = () => {
        if (currentPage < totalPages) {
            setCurrentPage(currentPage + 1);
        }
    };

    const handlePreviousPage = () => {
        if (currentPage > 1) {
            setCurrentPage(currentPage - 1);
        }
    };

    const filteredBusinesses = businesses.filter(business => 
        business.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const totalFilteredPages = Math.ceil(filteredBusinesses.length / ITEMS_PER_PAGE);
    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    const currentBusinesses = filteredBusinesses.slice(startIndex, startIndex + ITEMS_PER_PAGE);

    return (
        <div className='space-y-6'>
            <div className="grid place-items-center gap-y-8">
                <input 
                    type="text" 
                    placeholder="Search businesses..." 
                    value={searchTerm}
                    className="w-1/2 rounded-full border border-gray-200 bg-white px-5 py-3 pr-20 text-base shadow-md transition-shadow duration-200 hover:shadow-lg focus:border-gray-300 focus:outline-none"
                    onChange={(e) => {
                        setSearchTerm(e.target.value);
                        setCurrentPage(1);
                    }}
                />
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {currentBusinesses.map((business) => (
                        <BusinessCard key={business.id} business={business} />
                    ))}
                </div>
            </div>
            <Pagination>
                <PaginationContent>
                    <PaginationItem>
                        <PaginationPrevious href="#" onClick={handlePreviousPage} />
                    </PaginationItem>
                    {Array.from({ length: totalFilteredPages }, (_, i) => (
                        <PaginationItem key={i}>
                            <PaginationLink href="#" onClick={() => setCurrentPage(i + 1)}>
                                {i + 1}
                            </PaginationLink>
                        </PaginationItem>
                    ))}
                    <PaginationItem>
                        <PaginationEllipsis />
                    </PaginationItem>
                    <PaginationItem>
                        <PaginationNext href="#" onClick={handleNextPage} />
                    </PaginationItem>
                </PaginationContent>
            </Pagination>
        </div>
    );
};

export default AccountantDashboard;

