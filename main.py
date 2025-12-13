import yfinance as yf
import pandas as pd
import time

print("--- 🚀 TRACKER NASDAQ 100 (VERSION V2 - MISE À JOUR) ---")

def recuperer_nasdaq_100():
    # Liste mise à jour manuellement (Décembre 2025)
    # J'ai retiré les entreprises rachetées (SGEN, ANSS) et ajouté les nouvelles (TTD, DASH, etc.)
    return [
        'AAPL', 'MSFT', 'NVDA', 'AMZN', 'GOOGL', 'GOOG', 'META', 'TSLA', 'AVGO', 'COST',
        'PEP', 'CSCO', 'TMUS', 'CMCSA', 'INTC', 'AMD', 'TXN', 'QCOM', 'AMGN', 'HON',
        'INTU', 'BKNG', 'ISRG', 'VRTX', 'GILD', 'PANW', 'ADI', 'ADP', 'MDLZ', 'REGN',
        'KLAC', 'SNPS', 'LRCX', 'CDNS', 'CHTR', 'CSX', 'MAR', 'MU', 'ORLY', 'IDXX',
        'MNST', 'PCAR', 'PAYX', 'NXPI', 'ODFL', 'MELI', 'ASML', 'LULU', 'KDP', 'CTAS',
        'EXC', 'ADSK', 'EA', 'BIIB', 'XEL', 'ROST', 'FAST', 'AEP', 'CTSH', 'KHC',
        'WBD', 'MRVL', 'CPRT', 'SIRI', 'DLTR', 'ILMN', 'ALGN', 'TEAM', 'ZS', 'CRWD',
        'DDOG', 'TTD', 'DASH', 'GEHC', 'CEG', 'MCHP', 'ROP', 'ON', 'FANG', 'GFS',
        'CDW', 'CCEP', 'TTWO', 'BKR', 'VRSK', 'AZN', 'DXCM', 'FTNT', 'WDAY', 'LCID',
        'ARM', 'APP', 'ABNB', 'CEG', 'GEHC', 'MDB', 'PDD', 'SBUX', 'COIN', 'PLTR'
    ]

# 1. On charge la liste
mes_cibles = recuperer_nasdaq_100()
# On enlève les doublons au cas où (set) et on trie
mes_cibles = sorted(list(set(mes_cibles)))

print(f"🎯 Cibles chargées : {len(mes_cibles)} entreprises prêtes à être scannées.")
print("="*50)

# 2. La Boucle qui scanne tout
compteur = 0

for ticker in mes_cibles:
    try:
        # On va chercher l'info
        stock = yf.Ticker(ticker)
        holders = stock.institutional_holders
        
        if holders is not None and not holders.empty:
            # On prend le chef de la liste (le premier)
            top_holder = holders.iloc[0]
            nom_chef = top_holder['Holder']
            parts = top_holder['Shares']
            
            # On affiche le résultat
            print(f"✅ {ticker} : Dominé par {nom_chef} ({parts:,} actions)")
            compteur += 1
        else:
            print(f"❌ {ticker} : Pas d'info disponible (ou pas d'institutionnels)")
            
    except Exception as e:
        print(f"⚠️ Petit souci sur {ticker}, on passe au suivant.")

    # Petite pause
    time.sleep(0.2)

print("="*50)
print(f"🏁 FINI ! On a scanné {compteur} entreprises avec succès.")
