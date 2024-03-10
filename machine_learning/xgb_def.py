import optuna
import xgboost as xgb
from sklearn.metrics import f1_score
import time


class XGBOptimizer:
    def __init__(self, x_train, y_train, x_test, y_test):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test

    def opt_xgb(self, trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 5, 150),
            'max_depth': trial.suggest_int('max_depth', 3, 100),
            'max_leaves': trial.suggest_int('max_leaves', 3, 100),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 2),
            'booster': trial.suggest_categorical('booster', ['gbtree', 'gblinear', 'dart']),
            'gamma': trial.suggest_float('gamma', 0.01, 50),
            'reg_alpha': trial.suggest_float('reg_alpha', 0.01, 10),
            'reg_lambda': trial.suggest_float('reg_lambda', 0.01, 10),
            'random_state': 42,
        }
        model = xgb.XGBClassifier(**params)
        model.fit(self.x_train, self.y_train)
        y_pred = model.predict(self.x_test)
        f1 = f1_score(self.y_test, y_pred)
        return f1

    def xgb_optuna(self):
        start_time = time.time()
        study = optuna.create_study(direction='maximize')
        study.optimize(lambda trial: self.opt_xgb(trial), n_trials=10)
        trial = study.best_trial
        print('F1: {}'.format(trial.value))
        print("Best hyperparameters: {}".format(trial.params))
        end_time = time.time()
        execution_time_minutes = (end_time - start_time) / 60
        print("Execution time: {} minutes".format(execution_time_minutes))
        best_model = xgb.XGBClassifier(**trial.params)
        best_model.fit(self.x_train, self.y_train)
        return trial.params, best_model
