from flask import Flask, request, jsonify
import yfinance as yf
import os

# On crée le guichet
app = Flask(__name__)

print("--- 🤖 LE GUICHET EST OUVERT ---")

# C'est l'adresse où l'appli mobile va frapper
# Par exemple : https://ton-app.onrender.com/analyser?ticker=AAPL
@app.route('/analyser', methods=['GET'])
def analyser_entreprise():
    # 1. Le guichet écoute la demande : Quel ticker ?
    ticker = request.args.get('ticker')

    if not ticker:
        return jsonify({"erreur": "Il faut me donner un ticker ! (ex: ?ticker=AAPL)"}), 400

    ticker = ticker.upper() # On met en majuscule
    print(f"📞 Appel reçu pour : {ticker}")

    try:
        # 2. Le cerveau cherche l'info
        stock = yf.Ticker(ticker)
        holders = stock.institutional_holders

        if holders is not None and not holders.empty:
            # On prend le chef
            top_holder = holders.iloc[0]
            nom_chef = top_holder['Holder']
            parts = int(top_holder['Shares'])

            # 3. Le guichet prépare la réponse (en format JSON, le langage des applis)
            reponse = {
                "entreprise": ticker,
                "patron_nom": nom_chef,
                "patron_actions": f"{parts:,}",
                "message": f"Le boss de {ticker} est {nom_chef}."
            }
            return jsonify(reponse)
        else:
            return jsonify({"erreur": f"Pas d'infos sur les patrons pour {ticker}."}), 404

    except Exception as e:
        print(f"⚠️ Erreur : {e}")
        return jsonify({"erreur": "Oups, le cerveau a buggé."}), 500

# La commande pour lancer le serveur sur Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
