import os
import stripe
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Clé secrète Stripe depuis Render
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route("/")
def home():
    return """
    <h2>Professeur : créer ton compte Stripe</h2>
    <a href='/profs'><button>Créer mon compte Stripe</button></a>

    <h2>Élève : payer une facture</h2>
    <a href='/eleves'><button>Payer 100 CHF</button></a>
    """

# -----------------------------
# Page paiement élève
# -----------------------------
@app.route("/eleves", methods=["GET"])
def eleves():
    # Affiche la page HTML avec Stripe Elements
    return render_template("pay.html")

@app.route("/create-payment", methods=["POST"])
def create_payment():
    try:
        intent = stripe.PaymentIntent.create(
            amount=10000,   # 100 CHF en centimes
            currency="chf",
            payment_method_types=["card"]
        )
        return jsonify(client_secret=intent.client_secret)
    except Exception as e:
        return jsonify(error=str(e)), 400

# -----------------------------
# Page professeurs (onboarding)
# -----------------------------
@app.route("/profs", methods=["GET"])
def profs():
    return """
    <h1>Inscription Professeur</h1>
    <p><a href='/onboard-prof'><button>➡️ Créer mon compte Stripe</button></a></p>
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

    return f"<a href='{account_link.url}'><button>➡️ Compléter l’inscription Stripe</button></a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

