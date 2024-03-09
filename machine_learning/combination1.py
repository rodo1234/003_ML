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
                'n_estimators': trial.suggest_int('xgb_n_estimators', 100, 1000),
                'max_depth': trial.suggest_int('xgb_max_depth', 3, 10),
                'max_leaves': trial.suggest_int('xgb_max_leaves', 3, 10),
                'learning_rate': trial.suggest_float('xgb_learning_rate', 0.01, 0.3),
                'booster': trial.suggest_categorical('xgb_booster', ['gbtree', 'gblinear', 'dart']),
                'gamma': trial.suggest_float('xgb_gamma', 0.1, 1),
                'reg_alpha': trial.suggest_float('xgb_reg_alpha', 0.1, 1),
                'reg_lambda': trial.suggest_float('xgb_reg_lambda', 0.1, 1),
                'eval_metric': 'logloss',
                'use_label_encoder': False,
                'device': 'cuda'
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
