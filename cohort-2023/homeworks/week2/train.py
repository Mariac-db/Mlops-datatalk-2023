# train model to use mlflow :D 

import argparse
import os
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import mlflow


def load_pickle(filename: str):
    with open(filename, "rb") as f_in: 
        return pickle.load(f_in)

def run(data_path): 
    mlflow.sklearn.autolog()
    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_valid , y_valid = load_pickle(os.path.join(data_path, "valid.pkl"))

    print("Start training ...")
    rf = RandomForestRegressor(max_depth=10, random_state=0)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_valid)

    rmse = mean_squared_error(y_valid, y_pred, squared=False)
    print(f"rmse: {rmse}")


if __name__ == "__main__":

    mlflow.set_tracking_uri("/Users/mdurango/Documents/Mlops-datatalk-2023/cohort-2023/homeworks/week2/random-forest-experiments")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path",
        default= "/output", 
        help = "the location where the processed NYC taxi trip data was saved (pickles). "
    )

    args = parser.parse_args()

    with mlflow.start_run():

        run(args.data_path)




