import optuna
from sklearn.metrics import f1_score
from sklearn.svm import SVC
import time

class SVMOptimizer:

    def __init__(self, x_train, y_train, x_test, y_test):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test

    def opt_svm(self, trial):
        params = {
            'C': trial.suggest_float("C", 0.001, 10),
            'kernel': trial.suggest_categorical("kernel", ["linear", "rbf", "poly", "sigmoid"]),
            'degree': trial.suggest_int("degree", 2, 5),
            'gamma': trial.suggest_categorical("gamma", ["scale", "auto"] + [float(val) for val in range(1, 6)]),
            'random_state': 42,
            'max_iter': 10_000
        }
        model = SVC(**params)
        model.fit(self.x_train, self.y_train)
        y_pred = model.predict(self.x_test)
        f1 = f1_score(self.y_test, y_pred)
        return f1

    def svm_optuna(self):
        start_time = time.time()
        study = optuna.create_study(direction='maximize')
        study.optimize(lambda trial: self.opt_svm(trial), n_trials=10)
        trial = study.best_trial
        print('F1 Score: {}'.format(trial.value))
        print("Best hyperparameters: {}".format(trial.params))
        end_time = time.time()
        execution_time_minutes = (end_time - start_time) / 60
        print("Execution time: {} minutes".format(execution_time_minutes))
        best_model = SVC(**trial.params)
        best_model.fit(self.x_train, self.y_train)
        return trial.params, best_model
