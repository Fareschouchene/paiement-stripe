import os
from flask import Flask, request, redirect, jsonify
import stripe

app = Flask(__name__)

# ⚠️ Mets ta clé secrète LIVE ici
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

YOUR_DOMAIN = "https://paiement-stripe.onrender.com"

# Page d’accueil
@app.route("/")
def home():
    return """
    <h2>Professeur : créer ton compte Stripe</h2>
    <a href='/onboard-prof'><button>Créer mon compte Stripe</button></a>
    <br><br>
    <h2>Élève : payer une facture</h2>
    <a href='/checkout?amount=100'><button>Payer 100 CHF</button></a>
    <a href='/checkout?amount=200'><button>Payer 200 CHF</button></a>
    <a href='/checkout?amount=300'><button>Payer 300 CHF</button></a>
    <p>👉 Tu peux aussi modifier l’URL comme ça : /checkout?amount=150</p>
    """

# 1️⃣ Onboarding professeurs
@app.route("/onboard-prof")
def onboard_prof():
    account = stripe.Account.create(type="express")
    account_link = stripe.AccountLink.create(
        account=account.id,
        refresh_url=f"{YOUR_DOMAIN}/onboard-prof",
        return_url=f"{YOUR_DOMAIN}/success-prof",
        type="account_onboarding",
    )
    return redirect(account_link.url)

@app.route("/success-prof")
def success_prof():
    return "✅ Compte professeur créé avec succès !"

# 2️⃣ Paiement élève avec Checkout
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
            success_url=f"{YOUR_DOMAIN}/success-eleve",
            cancel_url=f"{YOUR_DOMAIN}/cancel-eleve",
        )
        return redirect(session.url, code=303)

    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route("/success-eleve")
def success_eleve():
    return "✅ Paiement élève réussi ! Merci."

@app.route("/cancel-eleve")
def cancel_eleve():
    return "❌ Paiement annulé par l’élève."

# Lancement local
if __name__ == "__main__":
    app.run(port=5000, debug=True)

