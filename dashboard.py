import streamlit as st
import pandas as pd
import numpy as np
import requests
import mplfinance as mpf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Configuração da Página
st.set_page_config(page_title="Dashboard de Criptomoedas", layout="wide")

# Barra Lateral
st.sidebar.title("💹 Dashboard de Criptomoedas")
token = st.sidebar.selectbox(
    "Escolha o Token!",
    ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]
)


# Função para buscar dados da Binance
def get_crypto_data(symbol, interval="1h", limit=100):
    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=[
            'Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_Time',
            'Base_Asset_Volume', 'Number_Of_Trades', 'Taker_Buy_Volume', 'Taker_Buy_Asset', 'ignore'
        ])
        
        # Convert data types
        df['Open_Time'] = pd.to_datetime(df['Open_Time'], unit='ms')
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df[numeric_columns] = df[numeric_columns].astype(float)
        
        return df[['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Number_Of_Trades']]
    return None

# Get data
df = get_crypto_data(token)

if df is not None:
    # Cálculo dos Indicadores
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()

    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    
    # Cálculo do RSI
    def calculate_rsi(data, window=14):
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()

        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    df['RSI'] = calculate_rsi(df['Close'])
    
    # MACD
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # Dashboard Layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title(f"📊 {token} Analysis")
        
        # Convertendo dados para mplfinance
        df_mpf = df.set_index('Open_Time')

        # Gerando o gráfico corretamente com mplfinance
        fig, ax = mpf.plot(
            df_mpf,
            type='candle',
            style='charles',
            title=f'{token} Gráfico de Preço',
            ylabel='Preço (USDT)',
            ylabel_lower='Volume',
            volume=True,
            returnfig=True  # Retorna a figura e os eixos corretamente

        )

        st.pyplot(fig)  # Renderiza o gráfico no Streamlit
    
    with col2:
        # Preço Atual e Variação de 24h
        current_price = df['Close'].iloc[-1]
        price_change = ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
        

        st.metric(
            "Preço Atual (USDT)",
            f"{current_price:.2f}",
            f"{price_change:.2f}%"
        )
        
        # Volume
        st.metric(
            "24h Volume",
            f"{df['Volume'].iloc[-1]:,.2f}"
        )
        
        # RSI
        st.metric(
            "RSI",
            f"{df['RSI'].iloc[-1]:.2f}"
        )

    # Indicadores Técnicos
    st.subheader("📈 Indicadores Técnicos")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Gráfico RSI
        fig_rsi = plt.figure(figsize=(12, 4))
        plt.plot(df['Open_Time'], df['RSI'], color='purple')
        plt.axhline(70, linestyle='dashed', color='red', alpha=0.5)
        plt.axhline(30, linestyle='dashed', color='green', alpha=0.5)
        plt.title("RSI")

        plt.grid(True)
        st.pyplot(fig_rsi)
    
    with col4:
        # Gráfico MACD
        fig_macd = plt.figure(figsize=(12, 4))
        plt.plot(df['Open_Time'], df['MACD'], label='MACD', color='blue')
        plt.plot(df['Open_Time'], df['Signal'], label='Signal', color='orange')
        plt.title("MACD")
        plt.legend()
        plt.grid(True)

        st.pyplot(fig_macd)

    # Statistics
    st.subheader("📊 Estatísticas de Preço")
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        st.metric("ATH", f"{df['High'].max():.2f}")
    with col6:
        st.metric("Menor Preço", f"{df['Low'].min():.2f}")
    with col7:
        st.metric("Preço Médio", f"{df['Close'].mean():.2f}")

else:
    st.error("Falha ao buscar dados da API da Binance")
