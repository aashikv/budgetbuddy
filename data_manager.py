import json
import os
from datetime import datetime

DATA_FILE = 'data.json'

class DataManager:
    def __init__(self):
        self._ensure_data_file()

    def _ensure_data_file(self):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w') as f:
                json.dump({'transactions': [], 'budget_limit': 20000.0}, f)
        else:
            # Ensure budget_limit exists in existing file
            with open(DATA_FILE, 'r+') as f:
                try:
                    data = json.load(f)
                    if 'budget_limit' not in data:
                        data['budget_limit'] = 20000.0
                        f.seek(0)
                        json.dump(data, f, indent=4)
                        f.truncate()
                except json.JSONDecodeError:
                    pass

    def load_data(self):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                if 'budget_limit' not in data:
                    data['budget_limit'] = 20000.0
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {'transactions': [], 'budget_limit': 20000.0}

    def set_budget_limit(self, limit):
        data = self.load_data()
        data['budget_limit'] = float(limit)
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def save_transaction(self, amount, category, date, note, type):
        data = self.load_data()
        transaction = {
            'amount': float(amount),
            'category': category,
            'date': date,
            'note': note,
            'type': type,
            'id': len(data['transactions']) + 1
        }
        data['transactions'].append(transaction)
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def get_summary(self):
        data = self.load_data()
        transactions = data['transactions']
        budget_limit = data.get('budget_limit', 20000.0)
        
        total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
        balance = total_income - total_expense
        
        # Category Breakdown for Pie Chart
        category_breakdown = {}
        for t in transactions:
            if t['type'] == 'expense':
                cat = t['category']
                category_breakdown[cat] = category_breakdown.get(cat, 0) + t['amount']
        
        # Monthly Trend for Line Chart (Last 6 months ideally, but all for now)
        monthly_trend = {}
        for t in transactions:
            # Assumes date format YYYY-MM-DD
            month_key = t['date'][:7] # YYYY-MM
            if month_key not in monthly_trend:
                monthly_trend[month_key] = {'income': 0, 'expense': 0}
            monthly_trend[month_key][t['type']] += t['amount']
            
        # Sort trend by date
        sorted_trend = dict(sorted(monthly_trend.items()))

        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'budget_limit': budget_limit,
            'transactions': sorted(transactions, key=lambda x: x['date'], reverse=True),
            'category_breakdown': category_breakdown,
            'monthly_trend': sorted_trend
        }
