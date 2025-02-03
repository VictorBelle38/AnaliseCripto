import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#'Open_Time','Open','High','Low','Close','Volume','Number_Of_Trades'

df = pd.read_csv('data/dados_crypto.csv')
# Cálculo da Média Móvel Simples
df['SMA_10'] = df['Close'].rooling(window=10).mean() # 10 Periodos
df['SMA_20'] = df['Close'].rooling(window=20).mean() # 20 Periodos  
df['SMA_50'] = df['Close'].rooling(window=50).mean() # 50 Periodos

# Calculo da Média Móvel Exponencial 
df['EMA_10'] = df['Close'].ewm(span=10,adjust= False).mean() # 10 Periodos
df['EMA_20'] = df['Close'].ewm(span=20,adjust= False).mean() # 20 Periodos
df['EMA_50'] = df['Close'].ewm(span=50,adjust= False).mean() # 50 Periodos

# Cálculo do Índice de Força Relativa (RSI)
def calculo_rsi(data, windows=14):
    delta = data.diff()
    win = (delta.where(delta> 0,0)).rooling(window=window).mean()
    loss = (delta.where(delta< 0,0)).rooling(window=window).mean()
    rs = win/loss
    return 100 - (100 / (1 + rs))

df['RSI'] = calculo_rsi(df['Close'],14)

# Cálculo MACD

df['EMA_12'] = df['Close'].ewm(span=12,adjust=False).mean()
df['EMA_26'] = df['Close'].ewm(span=26,adjust=False).mean()
df['MACD'] = df['EMA_12'] - df['EMA_26']
df['Signal'] = df['MACD'].ewm(span=9,adjust=False).mean


print("\n📊 Estatísticas dos Indicadores:")
print(df[['SMA_10','SMA_20','SMA_50','EMA_10','EMA_20','EMA_50','RSI','MACD','Signal']].describe())



#Plotar os Indicadores