import streamlit as st
import datetime
import numpy as np
import pandas as pd
from modules.financial_functions import portfolio_volatility, portfolio_returns, VaR
from modules.backend import tickers_by_issuer

# ===============
# BACKEND
# ===============

def complemento_confianza(confianza_str: str) -> float:
    '''
    Recibe un nivel de confianza como string (como por ejemplo '95')
    y retorna 1 - nivel:de_confianza como float (por ejemplo 0.05)
    '''
    # elimnar el símbolo '%' si está presente
    limpio = confianza_str.strip().replace('%', '')

    valor = float(limpio) / 100 # convertir '95' -> 0.85
    return 1 - valor

def risk(start:str, end:str, confidence:float) -> pd.DataFrame:
    '''

    '''
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
    df_final = df_final.sort_values(
        by=f'Value At Risk: {1-confidence}%',
        ascending=False)
    
    return df_final

st.title('Programación en finanzas - evaluación 2')

st.sidebar.title('Parámetros de entrada')

##PANEL LATERAL
#Rango fechas
st.sidebar.date_input("Fecha inicio", '2023-01-01', key='start')
st.sidebar.date_input("Fecha fin", '2025-09-01', key='end')

#Nivel de confianza
confidence = st.sidebar.selectbox('Nivel confianza', ['95%','99%'])
confidence =  complemento_confianza(confianza_str = confidence)
st.session_state.confidence = np.round(confidence, 2)

st.write(st.session_state)

df = risk(
    start = st.session_state.start,
    end = st.session_state.end,
    confidence = st.session_state.confidence,
)

st.dataframe(df)





