import pandas as pd
import numpy as np
from modules.financial_functions import portfolio_volatility, portfolio_returns, VaR
from modules.backend import tickers_by_issuer


if __name__ =='__main__': 
    #Obtener tickers de ishares
    tickers = tickers_by_issuer(issuer= 'iShares')
    list_tickers = list(tickers['TICKER'])
    
    for ticker in list_tickers:
        print(f'Instrumento: {ticker}')
    
    #Portafolio de renta fija
    tickers_rf = tickers[tickers['CATEGORIA']=='ETF RF']
    list_tickers_rf = list(tickers_rf['TICKER'])

    #Portafolio de renta variable
    tickers_rv = tickers[tickers['CATEGORIA']=='ETF RV']
    list_tickers_rv = list(tickers_rv['TICKER'])

    # rango de fechas
    start = '2024-01-01'
    end = '2024-12-31'

    # nivel de confianza
    confidence = 0.05

    lst = []

    for portfolio in [list_tickers_rf, list_tickers_rv]:
        print(portfolio)
        
        # obtener retornos
        df = portfolio_returns(tickers=portfolio, start=start, end=end)
        print(df.head(5))

        vector_w = np.array([1/len(portfolio)] * len(portfolio))

        # calcular volatilidad
        sigma = portfolio_volatility( df=df, vector_w=vector_w)

        # calcular VaR (medida de riesgo de mercado)
        var = VaR(sigma=sigma, confidence=confidence)
        var = np.abs(var)
        var_mensual = var * np.sqrt(20)
        lst.append(var_mensual)
    
    df_final = pd.DataFrame(
        {
            'PORTAFOLIO': ['iShares Renta Fija', 'iShares Renta Variable'],
            f'Value At Risk: {1-confidence}%': lst
        }
    )
    print(df_final)
