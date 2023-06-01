import os
import pickle
import argparse
import mlflow
import optuna
from optuna.samplers import TPESampler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from hyperopt import STATUS_OK
import click

# el servidor donde está running el mlflow (en mi caso)
# mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_tracking_uri("/Users/mdurango/Documents/Mlops-datatalk-2023/cohort-2023/homeworks/week2/random-forest-experiments")
# name of hiperparameter tuning of lr
mlflow.set_experiment("random-forest-hyper-optuna")

def load_pickle(filename):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)

@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
@click.option(
    "--num_trials",
    default=10,
    help="The number of parameter evaluations for the optimizer to explore"
)
def run_optimization(data_path: str, num_trials: int):

    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "valid.pkl"))

    def objective(trial):
        with mlflow.start_run():
            params = {
                'n_estimators': trial.suggest_int('n_estimators', 10, 50, 1),
                'max_depth': trial.suggest_int('max_depth', 1, 20, 1),
                'min_samples_split': trial.suggest_int('min_samples_split', 2, 10, 1),
                'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 4, 1),
                'random_state': 42,
                'n_jobs': -1
            }
            mlflow.log_params(params)
            rf = RandomForestRegressor(**params)
            rf.fit(X_train, y_train)
            y_pred = rf.predict(X_val)
            rmse = mean_squared_error(y_val, y_pred, squared=False)
            mlflow.log_metric("rmse", rmse)
        
        return rmse

    sampler = TPESampler(seed=42)
    study = optuna.create_study(direction="minimize", sampler=sampler)
    study.optimize(objective, n_trials=num_trials)


if __name__ == '__main__':
    run_optimization()

# @click.command()
# @click.option(
#     "--data_path",
#     default="./output",
#     help="Location where the processed NYC taxi trip data was saved"
# )
# @click.option(
#     "--num_trials",
#     default=10,
#     help="The number of parameter evaluations for the optimizer to explore"
# )

# def load_pickle(filename):
#     with open(filename, "rb") as f_in:
#         return pickle.load(f_in)
        

# def run_optimization(data_path: str, num_trials: int):

#     X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
#     X_val, y_val = load_pickle(os.path.join(data_path, "valid.pkl"))

#     def objective(trial):

#         with mlflow.start_run(run_name="rl-optuna"):

#             params = {
#                 'n_estimators': trial.suggest_int('n_estimators', 10, 50, 1),
#                 'max_depth': trial.suggest_int('max_depth', 1, 20, 1),
#                 'min_samples_split': trial.suggest_int('min_samples_split', 2, 10, 1),
#                 'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 4, 1),
#                 'random_state': 42,
#                 'n_jobs': -1
#             }

#             mlflow.log_params(params)

#             rf = RandomForestRegressor(**params)
#             rf.fit(X_train, y_train)
#             y_pred = rf.predict(X_val)
#             rmse = mean_squared_error(y_val, y_pred, squared=False)

#             mlflow.log_metric('rmse', rmse)

#         return {'loss': rmse, 'status': STATUS_OK}


#     sampler = TPESampler(seed=42)
#     study = optuna.create_study(direction="minimize", sampler=sampler)
#     study.optimize(objective, n_trials=num_trials)

# if __name__ == '__main__':

#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "--data_path",
#         default="output",
#         help="the location where the processed NYC taxi trip data was saved."
#     )
#     parser.add_argument(
#         "--num_trials",
#         default=10,
#         help="The number of parameter evaluations for the optimizer to explore"
#     )

#     args = parser.parse_args()

#     run_optimization(args.data_path, args.num_trials)