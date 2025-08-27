import { User } from './user';

export interface Accountant {
  id: string;
  user_id: string;
  super_accountant_id?: string;
  is_super_accountant: boolean;
  first_name?: string;
  last_name?: string;
  created_at: string;
  updated_at?: string;
  user: User;
}
