from flask import Flask, render_template, request
import stripe
import os

stripe_keys = {
  'secret_key': os.environ['STRIPE_SECRET_KEY'],
  'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}
stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET'])
def home():
    """Home page that describes the site and explains how it works"""
    return render_template('home.html')

@app.route('/contribute', methods=['GET'])
def purchase():
    """Purchasing page"""
    return render_template('checkout.html',key=stripe_keys['publishable_key'])

@app.route('/checkout', methods=['POST'])
def checkout():

    amount = 500

    customer = stripe.Customer.create(
        email='sample@customer.com',
        source=request.form['stripeToken']
    )

    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Investing in a renewable future'
    )

    return render_template('confirm.html', amount=amount)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000, debug=True)
