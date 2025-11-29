from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from data_manager import DataManager
from fpdf import FPDF
import io

app = Flask(__name__)
app.secret_key = 'supersecretkey' # Change this in production
data_manager = DataManager()

@app.route('/')
def dashboard():
    summary = data_manager.get_summary()
    
    # Smart Suggestions
    budget_limit = summary['budget_limit']
    total_expense = summary['total_expense']
    usage_percent = (total_expense / budget_limit * 100) if budget_limit > 0 else 0
    
    suggestion = "Great job 👏 You're spending smart!"
    suggestion_class = "success"
    
    if usage_percent >= 90:
        suggestion = "🚨 Critical! You've almost exhausted your budget."
        suggestion_class = "danger"
    elif usage_percent >= 75:
        suggestion = "⚠️ You're close to your limit — consider reducing food and travel expenses."
        suggestion_class = "warning"
    elif usage_percent >= 50:
        suggestion = "You're doing okay, keep an eye on expenses."
        suggestion_class = "info"
        
    return render_template('dashboard.html', summary=summary, suggestion=suggestion, suggestion_class=suggestion_class)

@app.route('/set_budget', methods=['POST'])
def set_budget():
    limit = request.form.get('budget_limit')
    try:
        data_manager.set_budget_limit(limit)
        flash('Budget limit updated successfully!', 'success')
    except ValueError:
        flash('Invalid budget limit.', 'error')
    return redirect(url_for('dashboard'))

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        amount = request.form.get('amount')
        category = request.form.get('category')
        date = request.form.get('date')
        note = request.form.get('note')
        type = request.form.get('type')
        
        try:
            data_manager.save_transaction(amount, category, date, note, type)
            flash(f'{type.capitalize()} added successfully!', 'success')
        except ValueError:
            flash('Invalid amount entered.', 'error')
        return redirect(url_for('dashboard'))
    
    type = request.args.get('type', 'expense')
    return render_template('add_transaction.html', type=type)

@app.route('/download_report')
def download_report():
    summary = data_manager.get_summary()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="BudgetBuddy Monthly Report", ln=1, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Total Income: {summary['total_income']:.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Total Expense: {summary['total_expense']:.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Balance: {summary['balance']:.2f}", ln=1)
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Transactions", ln=1)
    pdf.set_font("Arial", size=10)
    
    # Table Header
    pdf.cell(30, 10, "Date", 1)
    pdf.cell(40, 10, "Category", 1)
    pdf.cell(20, 10, "Type", 1)
    pdf.cell(30, 10, "Amount", 1)
    pdf.cell(70, 10, "Note", 1)
    pdf.ln()
    
    # Helper to handle unicode in FPDF (Latin-1 only)
    def clean_text(text):
        return str(text).encode('latin-1', 'replace').decode('latin-1')

    for t in summary['transactions']:
        pdf.cell(30, 10, clean_text(t['date']), 1)
        pdf.cell(40, 10, clean_text(t['category']), 1)
        pdf.cell(20, 10, clean_text(t['type']), 1)
        pdf.cell(30, 10, clean_text(t['amount']), 1)
        pdf.cell(70, 10, clean_text(t['note']), 1)
        pdf.ln()
        
    # Output to string and then to buffer
    pdf_content = pdf.output(dest='S').encode('latin-1')
    buffer = io.BytesIO(pdf_content)
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name='budget_report.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
