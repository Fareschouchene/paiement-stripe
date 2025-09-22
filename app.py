from flask import Flask, render_template_string, request, redirect, url_for
import stripe
import os

app = Flask(__name__)

# Clé secrète Stripe (met ta vraie clé live dans les variables Render)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# ---------------- ROUTE ACCUEIL ----------------
@app.route("/")
def home():
    return render_template_string("""
        <h2>Bienvenue</h2>
        <p><a href="/checkout?amount=5000"><button>Payer 50 CHF</button></a></p>
        <p><a href="/profs"><button>Espace professeurs</button></a></p>
        <p>👉 Tu peux changer le montant en modifiant l’URL comme ça :
        <code>/checkout?amount=10000</code> (100 CHF)</p>
    """)

# ---------------- ROUTE CHECKOUT ----------------
@app.route("/checkout")
def checkout():
    amount = request.args.get("amount", default=5000, type=int)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "chf",
                "product_data": {"name": "Cours particulier"},
                "unit_amount": amount,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=url_for("success", _external=True),
        cancel_url=url_for("cancel", _external=True),
    )
    return redirect(session.url, code=303)

# ---------------- ROUTE SUCCESS ----------------
@app.route("/success")
def success():
    return "<h3>✅ Paiement réussi, merci !</h3>"

# ---------------- ROUTE CANCEL ----------------
@app.route("/cancel")
def cancel():
    return "<h3>❌ Paiement annulé.</h3>"

# ---------------- ROUTE PROFS ----------------
@app.route("/profs")
def profs():
    return render_template_string("""
        <h2>Professeur : créer ton compte Stripe</h2>
        <a href="/create-account"><button>Créer mon compte Stripe</button></a>
    """)

@app.route("/create-account")
def create_account():
    account = stripe.Account.create(type="express")
    account_link = stripe.AccountLink.create(
        account=account.id,
        refresh_url=url_for("profs", _external=True),
        return_url=url_for("profs", _external=True),
        type="account_onboarding",
    )
    return redirect(account_link.url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


