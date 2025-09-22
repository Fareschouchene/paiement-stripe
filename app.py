from flask import Flask, render_template, redirect, request, jsonify
import stripe
import os

app = Flask(__name__)

# ------------------------------------------------
# Configuration Stripe
# ⚠️ Ta clé secrète doit être mise dans Render > Environment Variables
# Nom : STRIPE_SECRET_KEY
# Valeur : sk_live_*****************************
# ------------------------------------------------
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# --------------------------
# Page de paiement pour les élèves
# --------------------------
@app.route("/eleves")
def eleves():
    return render_template("pay.html")

# Endpoint pour créer un PaymentIntent (utilisé par pay.html)
@app.route("/create-payment", methods=["POST"])
def create_payment():
    try:
        data = request.get_json()
        intent = stripe.PaymentIntent.create(
            amount=data["amount"],   # Montant en centimes
            currency="chf"
        )
        return jsonify({"client_secret": intent.client_secret})
    except Exception as e:
        return jsonify(error=str(e)), 403

# --------------------------
# Onboarding pour les profs
# --------------------------
@app.route("/profs")
def profs():
    # Crée un compte Connect Express
    account = stripe.Account.create(type="express")

    # Crée un lien d’onboarding
    account_link = stripe.AccountLink.create(
        account=account.id,
        refresh_url="https://ton-service.onrender.com/profs",  # si l’utilisateur annule
        return_url="https://ton-service.onrender.com/success", # si c’est terminé
        type="account_onboarding",
    )

    return redirect(account_link.url)

# --------------------------
# Page de succès
# --------------------------
@app.route("/success")
def success():
    return "<h1>✅ Compte créé avec succès !</h1>"

# --------------------------
# Page d’accueil
# --------------------------
@app.route("/")
def home():
    return "<h2>✅ Service en ligne - Paiement Stripe actif !</h2>"

if __name__ == "__main__":
    app.run(debug=True)
