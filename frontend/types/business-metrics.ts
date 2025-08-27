export interface BusinessFinancialMetrics {
  id: string;
  business_id: string;
  revenue: number;
  gross_profit: number;
  net_profit: number;
  total_costs: number;
  percentage_change_revenue: number;
  percentage_change_gross_profit: number;
  percentage_change_net_profit: number;
  percentage_change_total_costs: number;
  created_at: string;
  updated_at?: string;
}

export interface BusinessMetrics {
  id: string;
  business_id: string;
  documents_due: number;
  outstanding_invoices: number;
  pending_approvals: number;
  accounting_year_end: string;
  created_at: string;
  updated_at?: string;
}
