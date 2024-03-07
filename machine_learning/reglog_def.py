import optuna
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
import time

class REGLOGOptimizer:

    def __init__(self, x_train, y_train, x_test, y_test):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test

    def opt_reglog(self, trial, x_train, y_train, x_test, y_test):
        model = LogisticRegression(
            C=trial.suggest_float("C", 0.001, 10),
            fit_intercept=trial.suggest_categorical("fit_intercept", [True, False]),
            l1_ratio=trial.suggets_float("l1_ratio", 0, 1),
            max_iter=10_000,
            penalty="elasticities",
            solver="saga",
            random_state=42
        )
        model.fit(x_train, y_train)
        y_hat = model.predict(x_test)

        return f1_score(y_test,y_hat)

    def reglog_optuna(self):
        start_time = time.time()
        study = optuna.create_study(direction='maximize')
        study.optimize(lambda trial: self.opt_reglog(trial), n_trials=100)
        trial = study.best_trial
        print('Accuracy: {}'.format(trial.value))
        print("Best hyperparameters: {}".format(trial.params))
        end_time = time.time()
        print("Execution time: {} seconds".format(end_time - start_time))
        return trial.params