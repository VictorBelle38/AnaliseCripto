import streamlit as st
import pandas as pd
import numpy as np
import requests
import mplfinance as mpf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import plotly.graph_objects as go

# Funções
def get_fear_and_greed_index():
    try:
        url = "https://api.alternative.me/fng/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return int(data['data'][0]['value'])
    except:
        return 50  
    return 50

def get_fear_greed_status(value):
    if value >= 0 and value <= 25:
        return "Extreme Fear"
    elif value > 25 and value <= 45:
        return "Fear"
    elif value > 45 and value <= 55:
        return "Neutral"
    elif value > 55 and value <= 75:
        return "Greed"
    elif value > 75 and value <= 100:
        return "Extreme Greed"
    else:
        return "Invalid Value"

# Configuração da Página
st.set_page_config(page_title="Dashboard de Criptomoedas", layout="wide")

# Barra Lateral
st.sidebar.title("💹 Dashboard de Criptomoedas")
token = st.sidebar.selectbox(
    "Escolha o Token!",
    ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "DOTUSDT", "LINKUSDT", "LTCUSDT", "BCHUSDT", "XMRUSDT", "XLMUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "DOTUSDT", "LINKUSDT", "LTCUSDT", "BCHUSDT", "XMRUSDT", "XLMUSDT"]
)

# Adicionar o Fear & Greed Index
fear_greed_value = get_fear_and_greed_index()
status = get_fear_greed_status(fear_greed_value)

st.sidebar.markdown("---")  # Separator
st.sidebar.markdown("### Fear & Greed Index")

# Gauge para o Fear & Greed Index
sidebar_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=fear_greed_value,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': status, 'font': {'size': 14}},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "lightblue"},
        'steps': [
            {'range': [0, 25], 'color': "red"},
            {'range': [25, 45], 'color': "orange"},
            {'range': [45, 55], 'color': "yellow"},
            {'range': [55, 75], 'color': "lightgreen"},
            {'range': [75, 100], 'color': "green"}
        ],
        'threshold': {
            'line': {'color': "white", 'width': 4},
            'thickness': 0.75,
            'value': fear_greed_value
        }
    }
))

sidebar_gauge.update_layout(
    height=200,  # Tamanho da Gauge
    margin=dict(l=10, r=10, t=30, b=10),  # Margens
)

st.sidebar.plotly_chart(sidebar_gauge, use_container_width=True)

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
        
        # Converter data types
        df['Open_Time'] = pd.to_datetime(df['Open_Time'], unit='ms')
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df[numeric_columns] = df[numeric_columns].astype(float)
        
        return df[['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Number_Of_Trades']]
    return None

# Pegar dados
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

    # Layout do Dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title(f"📊 {token} Analise")
        
        # Convertendo dados para mplfinance
        df_mpf = df.set_index('Open_Time')

        # Criando um estilo personalizado para o gráfico
        mc = mpf.make_marketcolors(up='#26a69a',        # Verde para compra
                                  down='#ef5350',        # Vermelho para venda
                                  edge='inherit',
                                  wick={'up': '#26a69a', 'down': '#ef5350'},  # Wicks
                                  volume={'up': '#26a69a', 'down': '#ef5350'}, # Volume
                                  inherit=True)
        
        s = mpf.make_mpf_style(marketcolors=mc,
                              gridstyle='--',
                              gridcolor='#0e1117',
                              facecolor='#0e1117',
                              figcolor='#0e1117',
                              y_on_right=True,
                              rc={'axes.labelcolor': '#0e1117',
                                  'axes.edgecolor': '#0e1117',
                                  'xtick.color': 'white',
                                  'ytick.color': 'white',
                                  'text.color': 'white'})

        # Gráfico com estilo personalizado
        fig, ax = mpf.plot(
            df_mpf,
            type='candle',
            style=s,
            title=f'{token} Gráfico 1HR',
            ylabel='Preço (USDT)',
            ylabel_lower='Volume',
            volume=False,
            returnfig=True
        )

        # Definir o background da figura para preto
        fig.patch.set_facecolor('black')
        
        st.pyplot(fig)
    
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

    # 
    st.subheader("📊 Estatísticas de Preço")
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        st.metric("Maior Preço nas ultimas 100h", f"{df['High'].max():.2f}")
    with col6:
        st.metric("Menor Preço nas ultimas 100h", f"{df['Low'].min():.2f}")
    with col7:
        st.metric("Preço Médio nas ultimas 100h", f"{df['Close'].mean():.2f}")



else:
    st.error("Falha ao buscar dados da API da Binance")
