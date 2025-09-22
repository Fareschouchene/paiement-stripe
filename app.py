import os
from flask import Flask, request, redirect, jsonify
import stripe

app = Flask(__name__)

# ⚠️ Mets ta clé secrète dans Render (Settings > Environment)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

YOUR_DOMAIN = "https://paiement-eleves.onrender.com"  # ton URL Render

@app.route("/")
def home():
    return """
    <h2>Élève : payer une facture</h2>
    <a href='/checkout?amount=100'><button>Payer 100 CHF</button></a>
    <a href='/checkout?amount=200'><button>Payer 200 CHF</button></a>
    <a href='/checkout?amount=300'><button>Payer 300 CHF</button></a>
    <p>👉 Tu peux aussi modifier l’URL comme ça : /checkout?amount=150</p>
    """

@app.route("/checkout")
def checkout():
    try:
        amount = int(request.args.get("amount", 100)) * 100  # en centimes

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "chf",
                    "product_data": {"name": "Paiement cours particulier"},
                    "unit_amount": amount,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{YOUR_DOMAIN}/success",
            cancel_url=f"{YOUR_DOMAIN}/cancel",
        )
        return redirect(session.url, code=303)

    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route("/success")
def success():
    return "✅ Paiement élève réussi ! Merci."

@app.route("/cancel")
def cancel():
    return "❌ Paiement annulé par l’élève."

if __name__ == "__main__":
    app.run(port=5000, debug=True)


