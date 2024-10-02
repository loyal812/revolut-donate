from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('GMAIL_AUTH_LOGIN')
app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_AUTH_APP_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

MERCHANT_TOKEN = os.getenv('MERCHENT_BUSINESS_SANDBOX_TOKEN')
REVOLUT_API = os.getenv('MERCHENT_BUSINESS_SANDBOX_URL')
ORGANIZATION_NAME = 'organizationName'


def send_email(to, name, amount):
    text = f"""
    {name}, thank you for your generous donation of £{amount} to {ORGANIZATION_NAME}!
    We truly appreciate your commitment.
    
    With your help, we can make a bigger impact.
    
    Sincerely,
    {ORGANIZATION_NAME}
    """
    msg = Message(f'{ORGANIZATION_NAME}: Thank you, {name}', 
                  sender=os.getenv('GMAIL_AUTH_LOGIN'),
                  recipients=[to])
    msg.body = text
    mail.send(msg)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create-order', methods=['POST'])
def create_order():
    data = request.json
    payment_data = {
        'amount': data['amount'],
        'currency': data['currency'],
        'full_name': f"{data['fname']} {data['lname']}" if len(data['fname']) >= 2 and len(data['lname']) >= 2 else None,
        'email': data['email'] if len(data['email']) and "@" in data['email'] else None
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {MERCHANT_TOKEN}'
    }
    
    response = requests.post(f'{REVOLUT_API}/1.0/orders', json=payment_data, headers=headers)
    return jsonify({**response.json(), **payment_data})


@app.route('/cancel-order', methods=['POST'])
def cancel_order():
    data = request.json
    order_id = data['orderId']
    response = requests.post(f'{REVOLUT_API}/1.0/orders/{order_id}/cancel', 
                             headers={'Authorization': f'Bearer {MERCHANT_TOKEN}'})
    return jsonify(response.json())


@app.route('/confirm-order', methods=['POST'])
def confirm_order():
    data = request.json
    order_id = data['orderId']
    
    order_response = retrieve_order(order_id)
    customer_id = order_response.get('customer_id')
    
    if not customer_id:
        return jsonify({'status': 400, 'message': 'No customer_id'})
    
    customer_response = retrieve_customer(customer_id)
    
    if order_response['state'] == 'PENDING' and customer_response['id'] == customer_id:
        confirm_url = f'{REVOLUT_API}/1.0/orders/{order_id}/confirm'
        payment_method_id = order_response['payments'][0]['payment_method']['id']
        response = requests.post(confirm_url, json={'payment_method_id': payment_method_id},
                                 headers={'Authorization': f'Bearer {MERCHANT_TOKEN}'})
        
        send_email(customer_response['email'], customer_response['full_name'], order_response['order_amount']['value'] / 100)
    
    return jsonify({'status': 200})


def retrieve_order(order_id):
    headers = {'Authorization': f'Bearer {MERCHANT_TOKEN}'}
    response = requests.get(f'{REVOLUT_API}/1.0/orders/{order_id}', headers=headers)
    return response.json()


def retrieve_customer(customer_id):
    headers = {'Authorization': f'Bearer {MERCHANT_TOKEN}'}
    response = requests.get(f'{REVOLUT_API}/1.0/customers/{customer_id}', headers=headers)
    return response.json()


if __name__ == '__main__':
    app.run(debug=False, port=5000)
