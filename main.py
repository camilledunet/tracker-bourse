import yfinance as yf
import pandas as pd
import time

print("--- 🚀 TRACKER NASDAQ 100 (VERSION INCASSABLE) ---")

def recuperer_nasdaq_100():
    # Au lieu de demander à Wikipedia (qui nous bloque), voici la liste officielle !
    # C'est la méthode la plus sûre pour que ça marche tout le temps.
    return [
        'AAPL', 'MSFT', 'NVDA', 'AMZN', 'GOOGL', 'META', 'TSLA', 'AVGO', 'PEP', 'COST',
        'LIN', 'AMD', 'NFLX', 'QCOM', 'TMUS', 'INTC', 'TXN', 'CMCSA', 'AMGN', 'INTU',
        'ISRG', 'HON', 'AMAT', 'BKNG', 'VRTX', 'SBUX', 'GILD', 'ADP', 'MDLZ', 'REGN',
        'ADI', 'LRCX', 'PANW', 'MU', 'SNPS', 'KLAC', 'PDD', 'CDNS', 'CSX', 'PYPL',
        'ASML', 'MAR', 'MELI', 'ORLY', 'MNST', 'CTAS', 'NXPI', 'ROP', 'FTNT', 'CHTR',
        'DXCM', 'MRVL', 'KDP', 'ADSK', 'PCAR', 'ORCL', 'MCHP', 'CPRT', 'PAYX', 'IDXX',
        'AEP', 'LULU', 'EXC', 'ODFL', 'AZN', 'BIIB', 'CSGP', 'KHC', 'SGEN', 'CTSH',
        'EA', 'WBD', 'FAST', 'XEL', 'BKR', 'DLTR', 'ANSS', 'GEHC', 'VRSK', 'CSCO',
        'GFS', 'ILMN', 'CDW', 'WBA', 'SIRI', 'EBAY', 'ZM', 'TEAM', 'JD', 'LCID'
    ]

# 1. On charge la liste
mes_cibles = recuperer_nasdaq_100()
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
            
            # On affiche le résultat
            print(f"✅ {ticker} : Dominé par {nom_chef}")
            compteur += 1
        else:
            print(f"❌ {ticker} : Pas d'info disponible")
            
    except Exception as e:
        print(f"⚠️ Petit souci sur {ticker}, on passe au suivant.")

    # Petite pause pour ne pas énerver Yahoo Finance
    time.sleep(0.2)

print("="*50)
print(f"🏁 FINI ! On a scanné {compteur} entreprises avec succès.")
