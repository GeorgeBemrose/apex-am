import { User } from './user';
import { Accountant } from './accountant';
import { BusinessFinancialMetrics, BusinessMetrics } from './index';

export interface Business {
  id: string;
  name: string;
  description?: string;
  owner_id: string;
  accountant_id?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  owner: User;
  accountant?: Accountant;
  accountants?: Accountant[];
  financial_metrics?: BusinessFinancialMetrics[];
  metrics?: BusinessMetrics[];
}