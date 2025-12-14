from flask import Flask, request
import yfinance as yf
import pandas as pd
import io
import base64
import matplotlib
matplotlib.use('Agg') # Important pour que ça marche sur un serveur sans écran
import matplotlib.pyplot as plt

app = Flask(__name__)

def nettoyer_pourcentage(valeur):
    # Transforme "20.5%" en 0.205
    try:
        if isinstance(valeur, str):
            return float(valeur.replace('%', '')) / 100
        return float(valeur)
    except:
        return 0.0

def creer_image_graphique(fig):
    # Transforme le dessin en code texte (Base64) pour le web
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

@app.route('/analyser', methods=['GET'])
def analyser_entreprise():
    ticker = request.args.get('ticker')
    if not ticker:
        return "<h1>Erreur : Pas de ticker</h1>"
    
    ticker = ticker.upper()
    print(f"🎨 Création des graphiques pour : {ticker}")
    
    try:
        stock = yf.Ticker(ticker)
        
        # --- GRAPH 1 : TOP 20 INSTITUTIONNELS ---
        inst_holders = stock.institutional_holders
        graph1_html = "<p>Pas de données institutionnelles.</p>"
        
        if inst_holders is not None and not inst_holders.empty:
            # On prend les 20 premiers
            top_20 = inst_holders.head(20)
            
            # Création du Camembert
            fig1, ax1 = plt.subplots(figsize=(6, 6))
            ax1.pie(top_20['Shares'], labels=top_20['Holder'], autopct='%1.1f%%', startangle=90)
            ax1.set_title(f"Top 20 des Propriétaires de {ticker}")
            
            # Encodage
            img1_data = creer_image_graphique(fig1)
            graph1_html = f'<img src="data:image/png;base64,{img1_data}" style="width:100%; max-width:500px;">'
            plt.close(fig1)

        # --- GRAPH 2 : RÉPARTITION GLOBALE (INSIDERS vs PUBLIC) ---
        major = stock.major_holders
        graph2_html = "<p>Pas de données de structure.</p>"
        
        if major is not None:
            # Nettoyage des données (yfinance renvoie un format bizarre parfois)
            try:
                # On essaie de trouver les lignes importantes
                # 0 = Insiders, 1 = Institutions. (Ceci peut varier, on fait une estimation simple)
                df = major.copy()
                # On renomme pour être sûr
                if df.shape[1] == 2:
                    df.columns = ['Percent', 'Type']
                
                # On extrait les valeurs
                insiders = 0.0
                institutions = 0.0
                
                for index, row in df.iterrows():
                    desc = str(row[1]).lower()
                    val = nettoyer_pourcentage(row[0])
                    if "insider" in desc:
                        insiders = val
                    elif "institution" in desc:
                        institutions = val

                public = 1.0 - (insiders + institutions)
                if public < 0: public = 0 # Sécurité

                # Données pour le graph
                labels = ['Initiés (Insiders)', 'Institutions', 'Public / Flottant']
                sizes = [insiders, institutions, public]
                colors = ['#ff9999','#66b3ff','#99ff99']

                fig2, ax2 = plt.subplots(figsize=(6, 6))
                ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                ax2.set_title(f"Structure de l'actionnariat {ticker}")
                
                img2_data = creer_image_graphique(fig2)
                graph2_html = f'<img src="data:image/png;base64,{img2_data}" style="width:100%; max-width:500px;">'
                plt.close(fig2)

            except Exception as e:
                print(f"Erreur calcul major holders: {e}")

        # --- ASSEMBLAGE DE LA PAGE WEB ---
        html_final = f"""
        <html>
        <body style="font-family:sans-serif; text-align:center; background-color:#f0f0f0;">
            <h1 style="color:#333;">Rapport pour {ticker}</h1>
            <div style="background:white; padding:10px; margin:10px; border-radius:10px;">
                {graph2_html}
            </div>
            <div style="background:white; padding:10px; margin:10px; border-radius:10px;">
                {graph1_html}
            </div>
            <p>Analyse générée par ton Robot Python 🤖</p>
        </body>
        </html>
        """
        return html_final

    except Exception as e:
        return f"<h1>Oups erreur : {e}</h1>"

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
