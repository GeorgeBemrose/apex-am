"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation"
import { useAuth } from "../../context/AuthContext";
import ManageSuperDashboard from "../../components/manage-super-dashboard";
import BusinessDashboard from "@/components/business-dashboard";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import businesses from '@/test/testData/businesses.json';
export default function Home() {
    const { user, login, logout } = useAuth();
    const router = useRouter()

    useEffect(() => {
        if (!user) {
            router.push("/login")
        }
    }, [user, router])

    type UserRole = "root_admin" | "super_accountant" | "accountant";

    const userRole: UserRole | null = user ? user.role as UserRole : null;
    const userName = user ? user.name : null;
    
    const tabsByRole = {
        root_admin: [
            { value: "businesses", label: "Businesses", content: <BusinessDashboard businesses={businesses}/> },
            { value: "manageSuper", label: "Manage Super Accountants", content: <ManageSuperDashboard /> },
        ],
        super_accountant: [
            { value: "businesses", label: "Businesses", content: <BusinessDashboard businesses={businesses}/> }
        ],
        accountant: [
            { value: "businesses", label: "Businesses", content: <BusinessDashboard businesses={businesses}/> },
        ],
    };

    const userTabs = userRole ? tabsByRole[userRole] : null;

    return (
        <div className="w-flex w-full flex-col gap-6 p-4">
            {userRole && userTabs ? (
                <Tabs defaultValue={userTabs[0].value}>
                    <TabsList>
                        {userTabs.map((tab) => (
                            <TabsTrigger key={tab.value} value={tab.value}>
                                {tab.label}
                            </TabsTrigger>
                        ))}
                    </TabsList>
                    {userTabs.map((tab) => (
                        <TabsContent key={tab.value} value={tab.value}>
                            {tab.content}
                        </TabsContent>
                    ))}
                </Tabs>
            ) : (
                <p className="text-black">404: Role not recognized.</p>
            )}
        </div>
    );
}