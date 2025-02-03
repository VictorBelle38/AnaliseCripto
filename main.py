import requests as re
import pandas as pd 


url = "https://api.binance.com/api/v3/klines"


params = {
    "symbol": "BTCUSDT",
    "interval": "1h",
    "limit": 24  #
}


response = re.get(url, params=params)

#Verificação da requisição
if response.status_code == 200:
    data = response.json()
    #Criação do DataFrame com os nomes das colunas
    df = pd.DataFrame(data,columns =[
    'Open_Time', 'Open', 'High', 'Low', 'Close','Volume', 'Close_Time',
    'Base_Asset_Volume', 'Number_Of_Trades','Taker_Buy_Volume','Taker_Buy_Asset',
    'ignore'
    ])
    
    df['Open_Time'] = pd.to_datetime(df['Open_Time'],unit='ms')
    #Utilizando os dados mais importantes da API
    df = df[['Open_Time','Open','High','Low','Close','Volume','Number_Of_Trades']]
    #Convertendo os valor para uma data legivel
    df['Open_Time'] = pd.to_datetime(df['Open_Time'],unit='ms')
    #Convertendo os valores para Float
    df["Open"] = df["Open"].astype(float)
    df["High"] = df["High"].astype(float)
    df["Low"] = df["Low"].astype(float)
    df["Close"] = df["Close"].astype(float)
    df["Volume"] = df["Volume"].astype(float)
    df.to_csv("data/dados_crypto.csv", index = False)

    print('Dados salvos')

else:
    print('Erro ao realizar a requisição', response.status_code)


