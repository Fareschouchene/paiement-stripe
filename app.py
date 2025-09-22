import os
from flask import Flask, request, redirect, jsonify
import stripe

app = Flask(__name__)

# ⚠️ Mets ta clé secrète dans Render (Settings > Environment > STRIPE_SECRET_KEY)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Ton domaine Render (à modifier après déploiement)
YOUR_DOMAIN = "https://paiement-stripe.onrender.com"

# 🟢 PAGE D’ACCUEIL
@app.route("/")
def home():
    return """
    <h2>Bienvenue 👋</h2>
    <p>
      🔹 <a href='/checkout?amount=5000'>Paiement élève (50 CHF)</a><br>
      🔹 <a href='/profs'>Espace professeurs</a>
    </p>
    """

# 🟢 ROUTE PAIEMENT ÉLÈVES (Checkout)
@app.route("/checkout")
def checkout():
    # Récupère le montant depuis l’URL, par défaut 5000 (50 CHF)
    try:
        amount = int(request.args.get("amount", 5000))
    except:
        return "❌ Montant invalide", 400

    # Crée une session Stripe Checkout
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "chf",
                "product_data": {"name": "Paiement facture élève"},
                "unit_amount": amount,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"{YOUR_DOMAIN}/success",
        cancel_url=f"{YOUR_DOMAIN}/cancel",
    )
    return redirect(session.url, code=303)

# 🟢 ROUTE PROFESSEURS (Onboarding Stripe Connect)
@app.route("/profs")
def profs():
    account = stripe.Account.create(type="express")
    link = stripe.AccountLink.create(
        account=account.id,
        refresh_url=f"{YOUR_DOMAIN}/profs",
        return_url=f"{YOUR_DOMAIN}/success-profs",
        type="account_onboarding",
    )
    return redirect(link.url, code=303)

# 🟢 ROUTES DE SUCCÈS / ANNULATION
@app.route("/success")
def success():
    return "✅ Paiement réussi, merci beaucoup !"

@app.route("/cancel")
def cancel():
    return "❌ Paiement annulé."

@app.route("/success-profs")
def success_profs():
    return "✅ Compte professeur créé avec succès !"

if __name__ == "__main__":
    app.run(port=5000, debug=True)


