import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler
from typing import Tuple

SPLIT = 0.75
K = 10


def load_data(path: str = "/path/to/csv/") -> pd.DataFrame:
    """
    This function takes a path string to a CSV file and loads it into
    a Pandas DataFrame.

    :param      path (optional): str, relative path of the CSV file

    :return     df: pd.DataFrame
    """

    df = pd.read_csv(f"{path}")
    df = df.drop(columns=["Unnamed: 0"])

    return df


def create_target_and_predictors(data: pd.DataFrame = None, target: str = "estimated_stock_pct") -> Tuple[pd.DataFrame, pd.Series]:
    """
    This function takes in a Pandas DataFrame and performs a `train_test_split`
    This data will be used to train the Random Forest Regressor.

    :param      data: pd.DataFrame, dataframe containing data for the model
    :param      target: str (optional), target variable that you want to predict

    :return     X: pd.DataFrame, y: pd.Series
    """

    # Check if data is provided
    if data is None:
        raise Exception("No data!")

    # Check to see if the target variable is present in the data
    if target not in data.columns:
        raise Exception(f"Target: {target} is not present in the data")
    
    X = data.drop(columns=[target])
    y = data[target]

    return X, y


def train_algorithm_with_cross_validation(X: pd.DataFrame = None, y: pd.Series = None) -> None:
    """
    This function takes the predictor and target variables and trains a Random Forest Regressor model across K folds.
    Using cross-validation, performance metrics will be output for each fold during training.

    :param      X: pd.DataFrame, predictor variables
    :param      y: pd.Series, target variable

    :return
    """

    # Check if data has been provided
    if X is None:
        raise Exception("No training data!")
    
    if y is None:
        raise Exception("No target data!")

    accuracy = []

    for fold in range(0, K):

        model = RandomForestRegressor()
        scaler = StandardScaler()

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=SPLIT, random_state=42)

        # We scale the data because it helps the algorithm to converge and helps the algorithm to not be greedy with large values
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

        trained_model = model.fit(X_train, y_train)

        y_pred = trained_model.predict(X_test)

        mae = mean_absolute_error(y_true=y_test, y_pred=y_pred)
        accuracy.append(mae)
        print(f"Fold {fold + 1}: MAE = {mae:.3f}")

    print(f"Average MAE: {(sum(accuracy) / len(accuracy)):.2f}")