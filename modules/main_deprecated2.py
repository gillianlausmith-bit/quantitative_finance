# import pandas as pd
# import numpy as np
# from modules.backend import market_prices

# #portafolio
# tickers = ['IEF', 'SPOTL', 'TLT', 'VGLT']

# start = '2023-01-01'
# end = '2024-21-31'

# df_port = market_prices(start_date=start, end_date=end, tickers=tickers)
# df_port = df_port[['FECHA', 'TICKER', 'EMISOR', 'PRECIO_CIERRE']] #para las columnas que quiero
# print(df_port.head(5))

# #==== volatilidad portafolio

# #vector de ponderación "pesos" (weights)
# weights =[1/len(tickers)] * len(tickers)
# vector_weights = np.array(weights)
# vector_weights_t = np.array([weights])
# # print(weights)

# # pivot table
# df_pivot = pd.pivot_table(
#     data=df_port, 
#     index='FECHA', 
#     columns='TICKER', 
#     values='PRECIO_CIERRE', 
#     aggfunc= 'max'
#     )

# print('-'*100)
# print(df_pivot.head(5))

# #retornos
# print('-'*100)
# df_ret = df_pivot.pct_change().dropna() #calcula el retorno de la fila respecto a la fila anterior
# print(df_ret)

# #matriz var - cov
# m_cov = df_ret.cov()
# print('-'*100)
# print(m_cov)
# matriz_cov = np.array(m_cov.values)

# #varianza del protafolio
# print('-'*100)
# print(f'dimension del vector de weights: {vector_weights.shape}')
# print(f'Dimension de la matriz de covarianza. {matriz_cov.shape}')
# print(f'dimension del vector de weights traspuesto es: {vector_weights.T.shape}')

# print('-'*100)
# vector_cov = np.dot(matriz_cov, vector_weights)
# print(f'dimension del vector de covarianza es: {vector_cov.shape}')

# print('-'*100)
# varianza = np.dot(vector_weights_t, vector_cov)[0]
# print(f'la varianza del portafolio es: {varianza}')

# # volatilidad
# vol_port = np.sqrt(varianza)
# print(f'la volatilidad del portafolio es: {vol_port}')

# # volatilidad anualizada
# vol_port_1y = vol_port * np.sqrt(252)



# ###############################

# from modules.backend import DB_Investments

# db = DB_Investments()
# df = db.execute_query("SELECT * FROM DM_INSTRUMENTOS")
# print(df.head())
# db.disconnect()

import pandas as pd
import numpy as np
from modules.backend import market_prices

#portafolio
tickers = ['IEF', 'SPOTL', 'TLT', 'VGLT']

start = '2023-01-01'
end = '2024-12-31'   # CORRECCIÓN de fecha inválida

df_port = market_prices(start_date=start, end_date=end, tickers=tickers)
df_port = df_port[['FECHA', 'TICKER', 'EMISOR', 'PRECIO_CIERRE']]  # columnas que quiero
print(df_port.head(5))

# pivot table
df_pivot = pd.pivot_table(
    data=df_port, 
    index='FECHA', 
    columns='TICKER', 
    values='PRECIO_CIERRE', 
    aggfunc='max'
)

print('-'*100)
print(df_pivot.head(5))

#retornos
print('-'*100)
df_ret = df_pivot.pct_change().dropna()  # retorna por filas
print(df_ret)

# número REAL de activos con datos
n_activos = len(df_ret.columns)

# pesos iguales para las columnas reales de la matriz
weights = [1/n_activos] * n_activos
vector_weights = np.array(weights)
vector_weights_t = np.array([weights])

#matriz var - cov
m_cov = df_ret.cov()
print('-'*100)
print(m_cov)
matriz_cov = np.array(m_cov.values)

#varianza del portafolio
print('-'*100)
print(f'dimension del vector de weights: {vector_weights.shape}')
print(f'Dimension de la matriz de covarianza. {matriz_cov.shape}')
print(f'dimension del vector de weights traspuesto es: {vector_weights_t.shape}')

print('-'*100)
vector_cov = np.dot(matriz_cov, vector_weights)
print(f'dimension del vector de covarianza es: {vector_cov.shape}')

print('-'*100)
varianza = np.dot(vector_weights_t, vector_cov)[0]
print(f'la varianza del portafolio es: {varianza}')

# volatilidad
vol_port = np.sqrt(varianza)
print(f'la volatilidad del portafolio es: {vol_port}')

# volatilidad anualizada
vol_port_1y = vol_port * np.sqrt(252)
print(f'la volatilidad anualizada del portafolio es: {vol_port_1y}')

###############################

from modules.backend import DB_Investments

db = DB_Investments()
df = db.execute_query("SELECT * FROM DM_INSTRUMENTOS")
print(df.head())
db.disconnect()
