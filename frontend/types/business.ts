export interface Business {
    name: string;
    financialMetrics: {
        revenue: number;
        grossProfit: number;
        netProfit: number;
        totalCosts: number;
        percentageChangeRevenue: number;
        percentageChangeGrossProfit: number;
        percentageChangeNetProfit: number;
        percentageChangeTotalCosts: number;
    };
    metrics: {
        documentsDue: number;
        outstandingInvoices: number;
        pendingApprovals: number;
        accountingYearEnd: string;
    };
}