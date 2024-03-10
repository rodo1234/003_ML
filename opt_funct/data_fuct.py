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


class STRATEGY_XGBOOST_BUY:
    def __init__(self, df, cash, active_operations, com, n_shares, stop_loss_long, take_profit_long):
        self.df = df
        self.cash = cash
        self.active_operations = active_operations
        self.com = com
        self.n_shares = n_shares
        self.stop_loss_long = stop_loss_long
        self.take_profit_long = take_profit_long
        self.strategy_value = []

    def run_strategy(self):
        for i, row in self.df.iterrows():
            # Close Operations
            temp_operations = []
            for op in self.active_operations:
                if op.operation_type == 'Long':
                    if op.stop_loss > row.Close:  # Close losing operations
                        self.cash += row.Close * op.n_shares * (1 - self.com)
                    elif op.take_profit < row.Close:  # Close profits
                        self.cash += row.Close * op.n_shares * (1 - self.com)
                    else:
                        temp_operations.append(op)

            self.active_operations = temp_operations

            # Execute New Operations
            if self.cash >= row['Close'] * self.n_shares * (1 + self.com):
                if row['xg_boost_buy']:
                    self.active_operations.append(Operation(operation_type='Long',
                                                            bought_at=row['Close'],
                                                            timestamp=row.Timestamp,
                                                            n_shares=self.n_shares,
                                                            stop_loss=(row['Close'] * self.stop_loss_long),
                                                            take_profit=row['Close'] * (1 + self.take_profit_long)))
                    self.cash -= row['Close'] * self.n_shares * (1 + self.com)

                    # Calculate Strategy Value
            open_positions_value = sum(op.n_shares * row['Close'] for op in self.active_operations)
            self.strategy_value.append(self.cash + open_positions_value)

        return self.strategy_value[-1]


class STRATEGY_REGLOG_BUY:
    def __init__(self, df, cash, active_operations, com, n_shares, stop_loss_long, take_profit_long):
        self.df = df
        self.cash = cash
        self.active_operations = active_operations
        self.com = com
        self.n_shares = n_shares
        self.stop_loss_long = stop_loss_long
        self.take_profit_long = take_profit_long
        self.strategy_value = []

    def run_strategy(self):
        for i, row in self.df.iterrows():
            # Close Operations
            temp_operations = []
            for op in self.active_operations:
                if op.operation_type == 'Long':
                    if op.stop_loss > row.Close:  # Close losing operations
                        self.cash += row.Close * op.n_shares * (1 - self.com)
                    elif op.take_profit < row.Close:  # Close profits
                        self.cash += row.Close * op.n_shares * (1 - self.com)
                    else:
                        temp_operations.append(op)

            self.active_operations = temp_operations

            # Execute New Operations
            if self.cash >= row['Close'] * self.n_shares * (1 + self.com):
                if row['reg_log_buy']:
                    self.active_operations.append(Operation(operation_type='Long',
                                                            bought_at=row['Close'],
                                                            timestamp=row.Timestamp,
                                                            n_shares=self.n_shares,
                                                            stop_loss=(row['Close'] * self.stop_loss_long),
                                                            take_profit=row['Close'] * (1 + self.take_profit_long)))
                    self.cash -= row['Close'] * self.n_shares * (1 + self.com)

                    # Calculate Strategy Value
            open_positions_value = sum(op.n_shares * row['Close'] for op in self.active_operations)
            self.strategy_value.append(self.cash + open_positions_value)

        return self.strategy_value[-1]


class STRATEGY_SVC_BUY:
    def __init__(self, df, cash, active_operations, com, n_shares, stop_loss_long, take_profit_long):
        self.df = df
        self.cash = cash
        self.active_operations = active_operations
        self.com = com
        self.n_shares = n_shares
        self.stop_loss_long = stop_loss_long
        self.take_profit_long = take_profit_long
        self.strategy_value = []

    def run_strategy(self):
        for i, row in self.df.iterrows():
            # Close Operations
            temp_operations = []
            for op in self.active_operations:
                if op.operation_type == 'Long':
                    if op.stop_loss > row.Close:  # Close losing operations
                        self.cash += row.Close * op.n_shares * (1 - self.com)
                    elif op.take_profit < row.Close:  # Close profits
                        self.cash += row.Close * op.n_shares * (1 - self.com)
                    else:
                        temp_operations.append(op)

            self.active_operations = temp_operations

            # Execute New Operations
            if self.cash >= row['Close'] * self.n_shares * (1 + self.com):
                if row['SVC_buy']:
                    self.active_operations.append(Operation(operation_type='Long',
                                                            bought_at=row['Close'],
                                                            timestamp=row.Timestamp,
                                                            n_shares=self.n_shares,
                                                            stop_loss=(row['Close'] * self.stop_loss_long),
                                                            take_profit=row['Close'] * (1 + self.take_profit_long)))
                    self.cash -= row['Close'] * self.n_shares * (1 + self.com)

                    # Calculate Strategy Value
            open_positions_value = sum(op.n_shares * row['Close'] for op in self.active_operations)
            self.strategy_value.append(self.cash + open_positions_value)

        return self.strategy_value[-1]

class STRATEGY_XGBOOST_REGLOG_BUY:
    def __init__(self, df, cash, active_operations, com, n_shares, stop_loss_long, take_profit_long):
        self.df = df
        self.cash = cash
        self.active_operations = active_operations
        self.com = com
        self.n_shares = n_shares
        self.stop_loss_long = stop_loss_long
        self.take_profit_long = take_profit_long
        self.strategy_value = []

    def run_strategy(self):
        for i, row in self.df.iterrows():
            # Close Operations
            temp_operations = []
            for op in self.active_operations:
                if op.operation_type == 'Long':
                    if op.stop_loss > row.Close:  # Close losing operations
                        self.cash += row.Close * op.n_shares * (1 - self.com)
                    elif op.take_profit < row.Close:  # Close profits
                        self.cash += row.Close * op.n_shares * (1 - self.com)
                    else:
                        temp_operations.append(op)

            self.active_operations = temp_operations

            # Execute New Operations
            if self.cash >= row['Close'] * self.n_shares * (1 + self.com):
                if (row['xg_boost_buy'])&(row['reg_log_buy']):
                    self.active_operations.append(Operation(operation_type='Long',
                                                            bought_at=row['Close'],
                                                            timestamp=row.Timestamp,
                                                            n_shares=self.n_shares,
                                                            stop_loss=(row['Close'] * self.stop_loss_long),
                                                            take_profit=row['Close'] * (1 + self.take_profit_long)))
                    self.cash -= row['Close'] * self.n_shares * (1 + self.com)

                    # Calculate Strategy Value
            open_positions_value = sum(op.n_shares * row['Close'] for op in self.active_operations)
            self.strategy_value.append(self.cash + open_positions_value)

        return self.strategy_value[-1]

class STRATEGY_XGBOOST_SVC_BUY:
    def __init__(self, df, cash, active_operations, com, n_shares, stop_loss_long, take_profit_long):
        self.df = df
        self.cash = cash
        self.active_operations = active_operations
        self.com = com
        self.n_shares = n_shares
        self.stop_loss_long = stop_loss_long
        self.take_profit_long = take_profit_long
        self.strategy_value = []

    def run_strategy(self):
        for i, row in self.df.iterrows():
            # Close Operations
            temp_operations = []
            for op in self.active_operations:
                if op.operation_type == 'Long':
                    if op.stop_loss > row.Close:  # Close losing operations
                        self.cash += row.Close * op.n_shares * (1 - self.com)
                    elif op.take_profit < row.Close:  # Close profits
                        self.cash += row.Close * op.n_shares * (1 - self.com)
                    else:
                        temp_operations.append(op)

            self.active_operations = temp_operations

            # Execute New Operations
            if self.cash >= row['Close'] * self.n_shares * (1 + self.com):
                if (row['xg_boost_buy'])&(row['SVC_buy']):
                    self.active_operations.append(Operation(operation_type='Long',
                                                            bought_at=row['Close'],
                                                            timestamp=row.Timestamp,
                                                            n_shares=self.n_shares,
                                                            stop_loss=(row['Close'] * self.stop_loss_long),
                                                            take_profit=row['Close'] * (1 + self.take_profit_long)))
                    self.cash -= row['Close'] * self.n_shares * (1 + self.com)

                    # Calculate Strategy Value
            open_positions_value = sum(op.n_shares * row['Close'] for op in self.active_operations)
            self.strategy_value.append(self.cash + open_positions_value)

        return self.strategy_value[-1]

class STRATEGY_REGLOG_SVC_BUY:
    def __init__(self, df, cash, active_operations, com, n_shares, stop_loss_long, take_profit_long):
        self.df = df
        self.cash = cash
        self.active_operations = active_operations
        self.com = com
        self.n_shares = n_shares
        self.stop_loss_long = stop_loss_long
        self.take_profit_long = take_profit_long
        self.strategy_value = []

    def run_strategy(self):
        for i, row in self.df.iterrows():
            # Close Operations
            temp_operations = []
            for op in self.active_operations:
                if op.operation_type == 'Long':
                    if op.stop_loss > row.Close:  # Close losing operations
                        self.cash += row.Close * op.n_shares * (1 - self.com)
                    elif op.take_profit < row.Close:  # Close profits
                        self.cash += row.Close * op.n_shares * (1 - self.com)
                    else:
                        temp_operations.append(op)

            self.active_operations = temp_operations

            # Execute New Operations
            if self.cash >= row['Close'] * self.n_shares * (1 + self.com):
                if (row['reg_log_buy'])&(row['SVC_buy']):
                    self.active_operations.append(Operation(operation_type='Long',
                                                            bought_at=row['Close'],
                                                            timestamp=row.Timestamp,
                                                            n_shares=self.n_shares,
                                                            stop_loss=(row['Close'] * self.stop_loss_long),
                                                            take_profit=row['Close'] * (1 + self.take_profit_long)))
                    self.cash -= row['Close'] * self.n_shares * (1 + self.com)

                    # Calculate Strategy Value
            open_positions_value = sum(op.n_shares * row['Close'] for op in self.active_operations)
            self.strategy_value.append(self.cash + open_positions_value)

        return self.strategy_value[-1]


class STRATEGY_XGBOOST_REGLOG_SVC_BUY:
    def __init__(self, df, cash, active_operations, com, n_shares, stop_loss_long, take_profit_long):
        self.df = df
        self.cash = cash
        self.active_operations = active_operations
        self.com = com
        self.n_shares = n_shares
        self.stop_loss_long = stop_loss_long
        self.take_profit_long = take_profit_long
        self.strategy_value = []

    def run_strategy(self):
        for i, row in self.df.iterrows():
            # Close Operations
            temp_operations = []
            for op in self.active_operations:
                if op.operation_type == 'Long':
                    if op.stop_loss > row.Close:  # Close losing operations
                        self.cash += row.Close * op.n_shares * (1 - self.com)
                    elif op.take_profit < row.Close:  # Close profits
                        self.cash += row.Close * op.n_shares * (1 - self.com)
                    else:
                        temp_operations.append(op)

            self.active_operations = temp_operations

            # Execute New Operations
            if self.cash >= row['Close'] * self.n_shares * (1 + self.com):
                if (row['xg_boost_buy'])&(row['reg_log_buy'])&(row['SVC_buy']):
                    self.active_operations.append(Operation(operation_type='Long',
                                                            bought_at=row['Close'],
                                                            timestamp=row.Timestamp,
                                                            n_shares=self.n_shares,
                                                            stop_loss=(row['Close'] * self.stop_loss_long),
                                                            take_profit=row['Close'] * (1 + self.take_profit_long)))
                    self.cash -= row['Close'] * self.n_shares * (1 + self.com)

                    # Calculate Strategy Value
            open_positions_value = sum(op.n_shares * row['Close'] for op in self.active_operations)
            self.strategy_value.append(self.cash + open_positions_value)

        return self.strategy_value[-1]




########################## SELLL
class STRATEGY_XGBOOST_SELL:
    def __init__(self, df, cash, active_operations, com, n_shares, stop_loss_short,
                 take_profit_short):
        self.df = df
        self.cash = cash
        self.active_operations = active_operations
        self.com = com
        self.n_shares = n_shares
        self.stop_loss_short = stop_loss_short
        self.take_profit_short = take_profit_short
        self.strategy_value = []

    def run_strategy(self):
        for i, row in self.df.iterrows():
            # Close Operations
            temp_operations = []
            for op in self.active_operations:
                if op.operation_type == 'Short':
                    if op.stop_loss < row.Close:  # Close losing operations
                        self.cash -= row.Close * op.n_shares * (1 + self.com)
                    elif op.take_profit > row.Close:  # Close profits
                        self.cash -= row.Close * op.n_shares * (1 + self.com)
                    else:
                        temp_operations.append(op)
            self.active_operations = temp_operations

            # Execute New Operations
            if self.cash >= row['Close'] * self.n_shares * (1 + self.com):

                if row['xg_boost_sell']:
                    self.active_operations.append(Operation(operation_type='Short',
                                                            bought_at=row['Close'],
                                                            timestamp=row.Timestamp,
                                                            n_shares=self.n_shares,
                                                            stop_loss=row['Close'] * (1 + self.stop_loss_short),
                                                            take_profit=row['Close'] * self.take_profit_short))

                    self.cash += row['Close'] * self.n_shares * (1 - self.com)

                    # Calculate Strategy Value
            open_positions_value = sum(op.n_shares * row['Close'] for op in self.active_operations)
            self.strategy_value.append(self.cash + open_positions_value)

        return self.strategy_value[-1]


class STRATEGY_REGLOG_SELL:
    def __init__(self, df, cash, active_operations, com, n_shares, stop_loss_short,
                 take_profit_short):
        self.df = df
        self.cash = cash
        self.active_operations = active_operations
        self.com = com
        self.n_shares = n_shares
        self.stop_loss_short = stop_loss_short
        self.take_profit_short = take_profit_short
        self.strategy_value = []

    def run_strategy(self):
        for i, row in self.df.iterrows():
            # Close Operations
            temp_operations = []
            for op in self.active_operations:
                if op.operation_type == 'Short':
                    if op.stop_loss < row.Close:  # Close losing operations
                        self.cash -= row.Close * op.n_shares * (1 + self.com)
                    elif op.take_profit > row.Close:  # Close profits
                        self.cash -= row.Close * op.n_shares * (1 + self.com)
                    else:
                        temp_operations.append(op)
            self.active_operations = temp_operations

            # Execute New Operations
            if self.cash >= row['Close'] * self.n_shares * (1 + self.com):

                if row['reg_log_sell']:
                    self.active_operations.append(Operation(operation_type='Short',
                                                            bought_at=row['Close'],
                                                            timestamp=row.Timestamp,
                                                            n_shares=self.n_shares,
                                                            stop_loss=row['Close'] * (1 + self.stop_loss_short),
                                                            take_profit=row['Close'] * self.take_profit_short))

                    self.cash += row['Close'] * self.n_shares * (1 - self.com)

                    # Calculate Strategy Value
            open_positions_value = sum(op.n_shares * row['Close'] for op in self.active_operations)
            self.strategy_value.append(self.cash + open_positions_value)

        return self.strategy_value[-1]


class STRATEGY_SVC_SELL:
    def __init__(self, df, cash, active_operations, com, n_shares, stop_loss_short,
                 take_profit_short):
        self.df = df
        self.cash = cash
        self.active_operations = active_operations
        self.com = com
        self.n_shares = n_shares
        self.stop_loss_short = stop_loss_short
        self.take_profit_short = take_profit_short
        self.strategy_value = []

    def run_strategy(self):
        for i, row in self.df.iterrows():
            # Close Operations
            temp_operations = []
            for op in self.active_operations:
                if op.operation_type == 'Short':
                    if op.stop_loss < row.Close:  # Close losing operations
                        self.cash -= row.Close * op.n_shares * (1 + self.com)
                    elif op.take_profit > row.Close:  # Close profits
                        self.cash -= row.Close * op.n_shares * (1 + self.com)
                    else:
                        temp_operations.append(op)
            self.active_operations = temp_operations

            # Execute New Operations
            if self.cash >= row['Close'] * self.n_shares * (1 + self.com):

                if row['SVC_sell']:
                    self.active_operations.append(Operation(operation_type='Short',
                                                            bought_at=row['Close'],
                                                            timestamp=row.Timestamp,
                                                            n_shares=self.n_shares,
                                                            stop_loss=row['Close'] * (1 + self.stop_loss_short),
                                                            take_profit=row['Close'] * self.take_profit_short))

                    self.cash += row['Close'] * self.n_shares * (1 - self.com)

                    # Calculate Strategy Value
            open_positions_value = sum(op.n_shares * row['Close'] for op in self.active_operations)
            self.strategy_value.append(self.cash + open_positions_value)

        return self.strategy_value[-1]



class STRATEGY_XGBOOST_REGLOG_SELL:
    def __init__(self, df, cash, active_operations, com, n_shares, stop_loss_short,
                 take_profit_short):
        self.df = df
        self.cash = cash
        self.active_operations = active_operations
        self.com = com
        self.n_shares = n_shares
        self.stop_loss_short = stop_loss_short
        self.take_profit_short = take_profit_short
        self.strategy_value = []

    def run_strategy(self):
        for i, row in self.df.iterrows():
            # Close Operations
            temp_operations = []
            for op in self.active_operations:
                if op.operation_type == 'Short':
                    if op.stop_loss < row.Close:  # Close losing operations
                        self.cash -= row.Close * op.n_shares * (1 + self.com)
                    elif op.take_profit > row.Close:  # Close profits
                        self.cash -= row.Close * op.n_shares * (1 + self.com)
                    else:
                        temp_operations.append(op)
            self.active_operations = temp_operations

            # Execute New Operations
            if self.cash >= row['Close'] * self.n_shares * (1 + self.com):

                if (row['xg_boost_sell'])&(row['reg_log_sell']):
                    self.active_operations.append(Operation(operation_type='Short',
                                                            bought_at=row['Close'],
                                                            timestamp=row.Timestamp,
                                                            n_shares=self.n_shares,
                                                            stop_loss=row['Close'] * (1 + self.stop_loss_short),
                                                            take_profit=row['Close'] * self.take_profit_short))

                    self.cash += row['Close'] * self.n_shares * (1 - self.com)

                    # Calculate Strategy Value
            open_positions_value = sum(op.n_shares * row['Close'] for op in self.active_operations)
            self.strategy_value.append(self.cash + open_positions_value)

        return self.strategy_value[-1]


class STRATEGY_XGBOOST_SVC_SELL:
    def __init__(self, df, cash, active_operations, com, n_shares, stop_loss_short,
                 take_profit_short):
        self.df = df
        self.cash = cash
        self.active_operations = active_operations
        self.com = com
        self.n_shares = n_shares
        self.stop_loss_short = stop_loss_short
        self.take_profit_short = take_profit_short
        self.strategy_value = []

    def run_strategy(self):
        for i, row in self.df.iterrows():
            # Close Operations
            temp_operations = []
            for op in self.active_operations:
                if op.operation_type == 'Short':
                    if op.stop_loss < row.Close:  # Close losing operations
                        self.cash -= row.Close * op.n_shares * (1 + self.com)
                    elif op.take_profit > row.Close:  # Close profits
                        self.cash -= row.Close * op.n_shares * (1 + self.com)
                    else:
                        temp_operations.append(op)
            self.active_operations = temp_operations

            # Execute New Operations
            if self.cash >= row['Close'] * self.n_shares * (1 + self.com):

                if (row['xg_boost_sell'])&(row['SVC_sell']):
                    self.active_operations.append(Operation(operation_type='Short',
                                                            bought_at=row['Close'],
                                                            timestamp=row.Timestamp,
                                                            n_shares=self.n_shares,
                                                            stop_loss=row['Close'] * (1 + self.stop_loss_short),
                                                            take_profit=row['Close'] * self.take_profit_short))

                    self.cash += row['Close'] * self.n_shares * (1 - self.com)

                    # Calculate Strategy Value
            open_positions_value = sum(op.n_shares * row['Close'] for op in self.active_operations)
            self.strategy_value.append(self.cash + open_positions_value)

        return self.strategy_value[-1]


class STRATEGY_REGLOG_SVC_SELL:
    def __init__(self, df, cash, active_operations, com, n_shares, stop_loss_short,
                 take_profit_short):
        self.df = df
        self.cash = cash
        self.active_operations = active_operations
        self.com = com
        self.n_shares = n_shares
        self.stop_loss_short = stop_loss_short
        self.take_profit_short = take_profit_short
        self.strategy_value = []

    def run_strategy(self):
        for i, row in self.df.iterrows():
            # Close Operations
            temp_operations = []
            for op in self.active_operations:
                if op.operation_type == 'Short':
                    if op.stop_loss < row.Close:  # Close losing operations
                        self.cash -= row.Close * op.n_shares * (1 + self.com)
                    elif op.take_profit > row.Close:  # Close profits
                        self.cash -= row.Close * op.n_shares * (1 + self.com)
                    else:
                        temp_operations.append(op)
            self.active_operations = temp_operations

            # Execute New Operations
            if self.cash >= row['Close'] * self.n_shares * (1 + self.com):

                if (row['reg_log_sell'])&(row['SVC_sell']):
                    self.active_operations.append(Operation(operation_type='Short',
                                                            bought_at=row['Close'],
                                                            timestamp=row.Timestamp,
                                                            n_shares=self.n_shares,
                                                            stop_loss=row['Close'] * (1 + self.stop_loss_short),
                                                            take_profit=row['Close'] * self.take_profit_short))

                    self.cash += row['Close'] * self.n_shares * (1 - self.com)

                    # Calculate Strategy Value
            open_positions_value = sum(op.n_shares * row['Close'] for op in self.active_operations)
            self.strategy_value.append(self.cash + open_positions_value)

        return self.strategy_value[-1]


class STRATEGY_XGBOOST_REGLOG_SVC_SELL:
    def __init__(self, df, cash, active_operations, com, n_shares, stop_loss_short,
                 take_profit_short):
        self.df = df
        self.cash = cash
        self.active_operations = active_operations
        self.com = com
        self.n_shares = n_shares
        self.stop_loss_short = stop_loss_short
        self.take_profit_short = take_profit_short
        self.strategy_value = []

    def run_strategy(self):
        for i, row in self.df.iterrows():
            # Close Operations
            temp_operations = []
            for op in self.active_operations:
                if op.operation_type == 'Short':
                    if op.stop_loss < row.Close:  # Close losing operations
                        self.cash -= row.Close * op.n_shares * (1 + self.com)
                    elif op.take_profit > row.Close:  # Close profits
                        self.cash -= row.Close * op.n_shares * (1 + self.com)
                    else:
                        temp_operations.append(op)
            self.active_operations = temp_operations

            # Execute New Operations
            if self.cash >= row['Close'] * self.n_shares * (1 + self.com):

                if (row['xg_boost_sell'])&(row['reg_log_sell'])&(row['SVC_sell']):
                    self.active_operations.append(Operation(operation_type='Short',
                                                            bought_at=row['Close'],
                                                            timestamp=row.Timestamp,
                                                            n_shares=self.n_shares,
                                                            stop_loss=row['Close'] * (1 + self.stop_loss_short),
                                                            take_profit=row['Close'] * self.take_profit_short))

                    self.cash += row['Close'] * self.n_shares * (1 - self.com)

                    # Calculate Strategy Value
            open_positions_value = sum(op.n_shares * row['Close'] for op in self.active_operations)
            self.strategy_value.append(self.cash + open_positions_value)

        return self.strategy_value[-1]
