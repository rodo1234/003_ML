import numpy as np
import optuna
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import time
import xgboost as xgb

class Combined_xgb_logreg:
        def __init__(self, x_train, y_train, x_test, y_test):
            self.x_train = x_train
            self.y_train = y_train
            self.x_test = x_test
            self.y_test = y_test

        def opt_combined(self, trial):
            # XGBoost parameters
            xgb_params = {
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

            # Logistic Regression parameters
            reglog_params = {
                'C': trial.suggest_float("reglog_C", 0.001, 10),
                'fit_intercept': trial.suggest_categorical("reglog_fit_intercept", [True, False]),
                'l1_ratio': trial.suggest_float("reglog_l1_ratio", 0, 1),
                'max_iter': 10000,
                'penalty': "elasticnet",
                'solver': "saga",
                'random_state': 42
            }

            # XGBoost model
            xgb_model = xgb.XGBClassifier(**xgb_params)
            xgb_model.fit(self.x_train, self.y_train)
            xgb_pred = xgb_model.predict_proba(self.x_test)[:, 1]  # Probabilidad de la clase positiva

            # Logistic Regression model
            reglog_model = LogisticRegression(**reglog_params)
            reglog_model.fit(self.x_train, self.y_train)
            reglog_pred = reglog_model.predict_proba(self.x_test)[:, 1]  # Probabilidad de la clase positiva

            # Combine predictions
            combined_pred_proba = (xgb_pred + reglog_pred) / 2  # Promedio de las probabilidades
            combined_pred_binary = np.where(combined_pred_proba > 0.5, 1, 0)  # Conversión a predicciones binarias
            f1 = f1_score(self.y_test, combined_pred_binary)
            return f1

        def combined_optuna(self):
            start_time = time.time()
            study = optuna.create_study(direction='maximize')
            study.optimize(lambda trial: self.opt_combined(trial), n_trials=100)
            trial = study.best_trial
            best_f1 = trial.value
            print('F1 Score: {}'.format(best_f1))
            print("Best hyperparameters: {}".format(trial.params))
            end_time = time.time()
            execution_time_minutes = (end_time - start_time) / 60
            print("Execution time: {} minutes".format(execution_time_minutes))
            return trial.params,best_f1
