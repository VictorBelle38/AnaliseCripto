import pandas as pd
import numpy as np

#Carregar os dados do arquivo salvo
df = pd.read_csv('data/dados_crypto.csv')

#Estatisticas Basicas dos preços

print('\n Estatisticas Básicas dos Preços: ')
print(df[['Open','High','Low','Close']].describe())

media_fechamento = df['Close'].mean()
mediana_fechamento = df['Close'].median()
desvio_padrao = df['Close'].std()

print(f'\n Média do Preço de Faturamento :{media_fechamento:.2f} USDT')
print(f'Mediana do Preço de Faturamento :{mediana_fechamento:.2f} USDT')
print(f'Desvio Padrão do Preço de Faturamento :{desvio_padrao:.2f} USDT')
#Variação percenteual dos candles
df['Pct_Return']= df['Close'].pct_change()* 100
media_variacao = df['Pct_Return'].mean()

print(f'A média da variação percentual entre os candles é de: {media_variacao:.2f}%')

maior_preco = df['High'].max()
menor_preco = df['Low'].min()

print(f'\n o Maior Preço Registrado: {maior_preco:.2f} USDT')
print(f'\n o Menor Preço Registrado: {menor_preco:.2f} USDT')

correlacao_open_close = df["Open"].corr(df["Close"])

print(f"\n Correlação entre preço de abertura e fechamento: {correlacao_open_close:.2f}")


