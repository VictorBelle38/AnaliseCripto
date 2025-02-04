# 🚀 Crypto Asset Analysis Dashboard | Real-Time Market Insights

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.22.0-FF4B4B)](https://streamlit.io/)
[![Binance API](https://img.shields.io/badge/API-Binance-F0B90B)](https://www.binance.com/en)

**Projeto em Evolução Contínua** | [Explore a Demo](https://victorbelle38-analisecripto.streamlit.app/) | [Relatório Técnico](/docs/TECHNICAL_REPORT.md)

## 🔥 Elevator Pitch
Dashboard interativo para análise técnica de criptoativos (BTC, ETH, SOL, BNB) utilizando dados em tempo real da Binance API. Desenvolvido para traders e entusiastas que precisam de:

✔️ Visualização profissional de candlesticks  
✔️ Indicadores técnicos calculados em tempo real  
✔️ Insights históricos fundamentais  
✔️ Base para estratégias quantitativas

*"Nasci da minha paixão por mercados financeiros digitais e hoje processa 100+ dados por requisição para democratizar acesso à análise profissional"*

## 🖥 Demonstração Visual
<table align="center">
  <tr>
    <td align="center">
      <img src="ImagensDashboard/GraficoCriptomoeda.png" width="400">
      <br>
      <em>Interface Principal com Séries Temporais</em>
    </td>
    <td align="center">
      <img src="ImagensDashboard/IndicadoresTecnicos.png" width="400">
      <br>
      <em>Análise Técnica com RSI e MACD</em>
    </td>
  </tr>
</table>

## 🎯 Problema & Solução
**Desafio:** 72% dos traders iniciantes de cripto não utilizam análise técnica por complexidade de ferramentas ([Fonte: CoinJournal](https://coinjournal.net/))  
**Minha Resposta:**  
- Pipeline automatizado de dados da Binance API
- Visualização intuitiva com Streamlit
- Cálculo em tempo real de métricas-chave

## ⚙️ Funcionalidades Técnicas
| Módulo | Tecnologias | Métricas |
|--------|-------------|----------|
| **Data Pipeline** | Python, Binance API, pandas | Coleta de 100 candles históricos |
| **Análise Técnica** | TA-Lib, NumPy | RSI, MACD, ATH, Médias Móveis |
| **Visualização** | Plotly, Streamlit | Gráficos interativos com zoom temporal |
| **Deploy** | Streamlit Cloud | Atualizações automáticas via CI/CD |

## 🛠️ Como Contribuir
```bash
# Clone o repositório
git clone https://github.com/VictorBelle38/AnaliseCripto.git

# Instalação (ambiente virtual recomendado)
pip install -r requirements.txt

# Execute localmente
streamlit run dashboard.py

