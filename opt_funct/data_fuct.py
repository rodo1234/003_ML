import ta
class functions:
    def clean_ds(df) -> object:
        for i in range(1, 4):
            df[f'X_t-{i}'] = df['Close'].shift(i)

        # Shift Close Column up by 5 rows
        df['Pt_5'] = df['Close'].shift(-5)

        # Agregamos RSI
        rsi_data = ta.momentum.RSIIndicator(close=df['Close'], window=28)
        df['RSI'] = rsi_data.rsi()

        # La Y
        df['Y_BUY'] = df['Close'] * (1 + 0.02) < df['Pt_5']
        df['Y_SELL'] = df['Close'] * (1 - 0.02) > df['Pt_5']

        df['Y_BUY'] = df['Y_BUY'].astype(int)
        df['Y_SELL'] = df['Y_SELL'].astype(int)

        return df