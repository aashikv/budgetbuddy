# BudgetBuddy

A modern personal finance tracker built with Python and Flask.

## Features
- **Dashboard**: View total income, expenses, and remaining balance
- **Transactions**: Add income and expense records with categories and notes
- **Budget Tracking**: Set monthly limits and track spending
- **Charts**: Visual spending breakdown and monthly trends
- **PDF Reports**: Download financial reports
- **Data Persistence**: All data is stored locally in `data.json`

## Setup Instructions

1. **Install Dependencies**:
   Ensure you have Python installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the App**:
   Open your browser and go to: `http://127.0.0.1:5000`

## Project Structure
- `app.py`: Main Flask application
- `data_manager.py`: Handles data storage and retrieval
- `static/style.css`: Custom styling
- `templates/`: HTML templates
- `data.json`: Stores your transaction data (created automatically)

## Technologies Used
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Charts**: Chart.js
- **Icons**: Font Awesome
