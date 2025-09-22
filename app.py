import os
import stripe
from flask import Flask, request, jsonify

app = Flask(__name__)

# Clé secrète Stripe (ajoutée dans les variables Render)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route("/")
def home():
    return "✅ Service en ligne - Paiement Stripe actif !"

# -----------------------------
# Lien pour les élèves (paiement)
# -----------------------------
@app.route("/eleves", methods=["GET"])
def eleves():
    return """
    <h1>Paiement Élève</h1>
    <p>Bienvenue sur la page de paiement pour les élèves.</p>
    <p><a href='/create-payment'>➡️ Payer ici</a></p>
    """

@app.route("/create-payment", methods=["POST"])
def create_payment():
    try:
        intent = stripe.PaymentIntent.create(
            amount=5000,          # 50 CHF en centimes
            currency="chf",
            payment_method_types=["card"]
        )
        return jsonify(client_secret=intent.client_secret)
    except Exception as e:
        return jsonify(error=str(e)), 400

# -----------------------------
# Lien pour les profs (onboarding)
# -----------------------------
@app.route("/profs", methods=["GET"])
def profs():
    return """
    <h1>Inscription Professeur</h1>
    <p>Bienvenue sur la page d’inscription des professeurs.</p>
    <p><a href='/onboard-prof'>➡️ Créer mon compte Stripe</a></p>
    """

@app.route("/onboard-prof", methods=["GET"])
def onboard_prof():
    account = stripe.Account.create(type="express")

    account_link = stripe.AccountLink.create(
        account=account.id,
        refresh_url="https://paiement-stripe.onrender.com/profs",
        return_url="https://paiement-stripe.onrender.com/profs",
        type="account_onboarding"
    )

    return f"<a href='{account_link.url}'>➡️ Compléter l’inscription Stripe</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

