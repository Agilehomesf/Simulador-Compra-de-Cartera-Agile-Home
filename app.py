import os
import logging
from flask import Flask, render_template, request, jsonify, session
import math

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")

# Bank data with real Colombian interest rates
BANKS = {
    'banco_bogota': {
        'name': 'Banco de Bogotá',
        'rates': {'min': 10.95, 'max': 12.68},
        'campaign_rate': 9.95,
        'campaign_description': 'Campaña nómina hasta 30 julio',
        'icon': 'bi-building'
    },
    'bbva': {
        'name': 'BBVA',
        'rates': {'min': 12.95, 'max': 15.79},
        'icon': 'bi-bank'
    },
    'itau': {
        'name': 'Itau',
        'rates': {'min': 11.71, 'max': 12.40},
        'icon': 'bi-credit-card'
    },
    'banco_occidente': {
        'name': 'Banco de Occidente',
        'rates': {'min': 10.85, 'max': 16.16},
        'icon': 'bi-piggy-bank'
    },
    'caja_social': {
        'name': 'Caja Social',
        'rates': {'min': 10.00, 'max': 16.60},
        'icon': 'bi-house'
    }
}

def calculate_monthly_payment(principal, annual_rate, months):
    """Calculate monthly payment using amortization formula"""
    if annual_rate == 0:
        return principal / months
    
    monthly_rate = annual_rate / 100 / 12
    payment = principal * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    return payment

def calculate_portfolio_purchase(data):
    """Calculate mortgage portfolio purchase scenarios"""
    results = []
    
    # Extract form data
    property_value = float(data['property_value'])
    portfolio_balance = float(data['portfolio_balance'])
    initial_term = int(data['initial_term'])
    remaining_term = int(data['remaining_term'])
    current_payment_total = float(data['current_payment'])  # This already includes insurance
    current_rate = float(data['current_rate'])
    insurance_value = float(data['insurance_value'])
    new_term = int(data['new_term'])
    selected_banks = data.getlist('selected_banks')
    
    # Calculate theoretical current payment based on current rate for fair comparison
    current_payment_base = current_payment_total - insurance_value
    theoretical_current_payment = calculate_monthly_payment(portfolio_balance, current_rate, remaining_term)
    theoretical_current_total = theoretical_current_payment + insurance_value
    
    for bank_key in selected_banks:
        if bank_key not in BANKS:
            continue
            
        bank = BANKS[bank_key]
        
        # Calculate payments with different rates
        best_rate = bank['rates']['min']
        worst_rate = bank['rates']['max']
        
        # Skip bank if minimum rate is higher than current rate (not allowed by law)
        if best_rate >= current_rate:
            logging.debug(f"{bank['name']}: Skipped - minimum rate {best_rate}% >= current rate {current_rate}%")
            continue
            
        # If worst rate is higher than current rate, cap it at current rate
        if worst_rate >= current_rate:
            worst_rate = current_rate - 0.01  # Just below current rate
            logging.debug(f"{bank['name']}: Capped maximum rate to {worst_rate}% (below current {current_rate}%)")
        
        new_payment_best = calculate_monthly_payment(portfolio_balance, best_rate, new_term)
        new_payment_worst = calculate_monthly_payment(portfolio_balance, worst_rate, new_term)
        
        # Calculate total monthly payments (including insurance)
        new_total_payment_best = new_payment_best + insurance_value
        new_total_payment_worst = new_payment_worst + insurance_value
        
        # Calculate monthly difference (current actual payment vs new payment)
        monthly_difference_best = current_payment_total - new_total_payment_best
        monthly_difference_worst = current_payment_total - new_total_payment_worst
        
        # Calculate total savings: what client would pay in remaining term vs new term
        current_total_to_pay = theoretical_current_total * remaining_term
        new_total_to_pay_best = new_total_payment_best * new_term
        new_total_to_pay_worst = new_total_payment_worst * new_term
        
        total_savings_best = current_total_to_pay - new_total_to_pay_best
        total_savings_worst = current_total_to_pay - new_total_to_pay_worst
        
        # Debug logging for calculation verification
        logging.debug(f"{bank['name']}: Portfolio=${portfolio_balance:,.0f}, Rate={best_rate}%, Term={new_term}")
        logging.debug(f"{bank['name']}: Actual payment=${current_payment_total:,.0f}, New payment=${new_total_payment_best:,.0f}, Monthly difference=${monthly_difference_best:,.0f}")
        logging.debug(f"{bank['name']}: Current total=${current_total_to_pay:,.0f}, New total=${new_total_to_pay_best:,.0f}, Total savings=${total_savings_best:,.0f}")
        
        result = {
            'bank': bank['name'],
            'bank_key': bank_key,
            'icon': bank['icon'],
            'best_rate': best_rate,
            'worst_rate': worst_rate,
            'new_payment_best': new_payment_best,
            'new_payment_worst': new_payment_worst,
            'monthly_savings_best': monthly_difference_best,
            'monthly_savings_worst': monthly_difference_worst,
            'total_savings_best': total_savings_best,
            'total_savings_worst': total_savings_worst
        }
        
        # Add campaign rate if available and valid
        if 'campaign_rate' in bank and bank['campaign_rate'] < current_rate:
            campaign_payment = calculate_monthly_payment(portfolio_balance, bank['campaign_rate'], new_term)
            campaign_total_payment = campaign_payment + insurance_value
            campaign_monthly_difference = current_payment_total - campaign_total_payment
            campaign_total_to_pay = campaign_total_payment * new_term
            campaign_total_savings = current_total_to_pay - campaign_total_to_pay
            
            result['campaign_rate'] = bank['campaign_rate']
            result['campaign_payment'] = campaign_payment
            result['campaign_total_payment'] = campaign_total_payment
            result['campaign_monthly_savings'] = campaign_monthly_difference
            result['campaign_total_savings'] = campaign_total_savings
            result['campaign_description'] = bank.get('campaign_description', '')
            
            # Debug campaign calculation
            logging.debug(f"{bank['name']} Campaign: Rate={bank['campaign_rate']}%, Payment=${campaign_total_payment:,.0f}, Monthly Difference=${campaign_monthly_difference:,.0f}")
        
        results.append(result)
    
    # Sort by best savings
    results.sort(key=lambda x: x['monthly_savings_best'], reverse=True)
    
    return {
        'results': results,
        'property_value': property_value,
        'portfolio_balance': portfolio_balance,
        'current_payment': current_payment_base,
        'current_total_payment': current_payment_total,
        'current_rate': current_rate,
        'insurance_value': insurance_value,
        'new_term': new_term,
        'remaining_term': remaining_term
    }

@app.route('/')
def index():
    """Main page with mortgage portfolio calculator"""
    return render_template('index.html', banks=BANKS)

@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle calculation request"""
    try:
        logging.debug(f"Form data received: {request.form}")
        
        # Validate required fields
        required_fields = ['property_value', 'portfolio_balance', 'initial_term', 
                         'remaining_term', 'current_payment', 'current_rate', 'insurance_value', 'new_term']
        
        for field in required_fields:
            if not request.form.get(field):
                return jsonify({'success': False, 'error': f'Campo requerido: {field}'})
        
        # Check if at least one bank is selected
        if not request.form.getlist('selected_banks'):
            return jsonify({'success': False, 'error': 'Debe seleccionar al menos un banco'})
        
        # Calculate results
        results = calculate_portfolio_purchase(request.form)
        results['success'] = True
        
        return jsonify(results)
        
    except Exception as e:
        logging.error(f"Error in calculation: {str(e)}")
        return jsonify({'success': False, 'error': f'Error en el cálculo: {str(e)}'})

@app.route('/whatsapp/<bank_key>')
def whatsapp_contact(bank_key):
    """Generate WhatsApp contact link"""
    bank = BANKS.get(bank_key)
    if not bank:
        return jsonify({'error': 'Banco no encontrado'})
    
    message = f"Hola! Estoy interesado en obtener información sobre compra de cartera hipotecaria en {bank['name']}. ¿Podrían ayudarme?"
    whatsapp_number = "573001234567"  # Replace with actual number
    encoded_message = message.replace(' ', '%20').replace('!', '%21').replace('?', '%3F')
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"
    
    return jsonify({'url': whatsapp_url})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)