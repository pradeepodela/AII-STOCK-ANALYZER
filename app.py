from tradingview_ta import *
import streamlit as st
import pandas as pd

df = pd.read_csv('data.csv')

companies_listed = df['SYMBOL'].tolist()
symbol_list = [f'nse:{symbol}' for symbol in companies_listed]


st.title("Pradeep's bulk stock analyzer app")
st.markdown(
    '''
    <style>
    [data-testid='sidebar'][aria-expanded='true'] > div:firstchild{width:400px}
    [data-testid='sidebar'][aria-expanded='false'] > div:firstchild{width:400px , margin-left: -400px}
    </style>
    ''',
    unsafe_allow_html=True
)

st.markdown('---')
st.title("All Stock Analysis")
interval = st.selectbox('interval', ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M'])
interval_mapping = {
    '1m': Interval.INTERVAL_1_MINUTE,
    '5m': Interval.INTERVAL_5_MINUTES,
    '15m': Interval.INTERVAL_15_MINUTES,
    '30m': Interval.INTERVAL_30_MINUTES,
    '1h': Interval.INTERVAL_1_HOUR,
    '4h': Interval.INTERVAL_4_HOURS,
    '1d': Interval.INTERVAL_1_DAY,
    '1w': Interval.INTERVAL_1_WEEK,
    '1M': Interval.INTERVAL_1_MONTH
}
predection = st.selectbox('predection', ['STRONG_BUY', 'BUY', 'NEUTRAL', 'SELL', 'STRONG_SELL'])
interval = interval_mapping.get(interval, Interval.INTERVAL_1_DAY)

SUBMIT = st.button('GET DATA')


grandfather_symbols = []

if SUBMIT:
    grandfather_results = get_multiple_analysis(screener="india", interval=interval, symbols=symbol_list)
    for symbol, analysis_object in grandfather_results.items():
        try:
            if analysis_object.summary['RECOMMENDATION'] == predection:
                
                
                grandfather_symbols.append(symbol.replace('NSE:', ''))
        except Exception as e:
            pass

    

    st.markdown('---')
    st.title(predection)
    strong_buy_df = pd.DataFrame(grandfather_symbols, columns=[predection])
    st.dataframe(strong_buy_df)
    st.markdown('---')
