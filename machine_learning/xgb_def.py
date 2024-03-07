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
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
            'max_depth': trial.suggest_int('max_depth', 3, 10),
            'max_leaves': trial.suggest_int('max_leaves', 3, 10),
            'learning_rate': trial.suggest_loguniform('learning_rate', 0.01, 0.3),
            'booster': trial.suggest_categorical('booster', ['gbtree', 'gblinear', 'dart']),
            'gamma': trial.suggest_loguniform('gamma', 0.1, 1),
            'reg_alpha': trial.suggest_loguniform('reg_alpha', 0.1, 1),
            'reg_lambda': trial.suggest_loguniform('reg_lambda', 0.1, 1),
            'eval_metric': 'binary:logistic',
            'use_label_encoder': False
            # 'device': 'cuda' # Si no tienen GPU y linux comentar esta linea
        }
        model = xgb.XGBClassifier(**params)
        model.fit(self.x_train, self.y_train)
        y_pred = model.predict(self.x_test)
        f1 = f1_score(self.y_test, y_pred)
        return f1

    def xgb_optuna(self):
        start_time = time.time()
        study = optuna.create_study(direction='maximize')
        study.optimize(lambda trial: self.opt_xgb(trial), n_trials=100)
        trial = study.best_trial
        print('Accuracy: {}'.format(trial.value))
        print("Best hyperparameters: {}".format(trial.params))
        end_time = time.time()
        print("Execution time: {} seconds".format(end_time - start_time))
        return trial.params
