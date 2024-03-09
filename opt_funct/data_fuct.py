import ta
class functions:
    def clean_ds(df):
        df = df.copy()
        for i in range(1, 4):
            df[f'X_t-{i}'] = df['Close'].shift(i)

        # Shift Close Column up by 5 rows
        df['Pt_5'] = df['Close'].shift(-5)

        # Agregamos RSI
        rsi_data = ta.momentum.RSIIndicator(close=df['Close'], window=28)
        df['RSI'] = rsi_data.rsi()

        # La Y
        df['Y_BUY'] = df['Close'] < df['Pt_5']
        df['Y_SELL'] = df['Close'] > df['Pt_5']

        # df['Y_BUY'] = df['Y_BUY'].astype(int)
        # df['Y_SELL'] = df['Y_SELL'].astype(int)

        return df

class Operation:
    def __init__(self, operation_type, bought_at, timestamp, n_shares,
                 stop_loss, take_profit):
        self.operation_type = operation_type
        self.bought_at = bought_at
        self.timestamp = timestamp
        self.n_shares = n_shares
        self.sold_at = None
        self.stop_loss = stop_loss
        self.take_profit = take_profit