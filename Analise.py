import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

df = pd.read_csv('data/dados_crypto.csv')

plt.figure(figsize=(12,6))
plt.plot(df['Open_Time'], df['Close'], label='Preço de Fechamento', color='blue')
plt.xlabel('Data')
plt.ylabel('Preço de Fechamento')
plt.title('Evoluçaõ do Preço de Fechamento')
plt.legend()
plt.grid()
plt.show()

df_candles = df.copy()
df_candles["Open_Time"] = pd.to_datetime(df_candles["Open_Time"])
df_candles.set_index('Open_Time',inplace= True)

mpf.plot(df_candles, type = 'candle', style = 'charles', volume = False, title = 'Grafico BTC/USDT', ylabel='Preço(USDT)')