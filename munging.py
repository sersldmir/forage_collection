import pandas as pd
from typing import List

FILE_LINK0 = "https://raw.githubusercontent.com/vagabond-systems/quantium-task-1-model-answer/main/data/daily_sales_data_0.csv"
FILE_LINK1 = "https://raw.githubusercontent.com/vagabond-systems/quantium-task-1-model-answer/main/data/daily_sales_data_1.csv"
FILE_LINK2 = "https://raw.githubusercontent.com/vagabond-systems/quantium-task-1-model-answer/main/data/daily_sales_data_2.csv"


def load_data(
    data_links: List[str] = [FILE_LINK0, FILE_LINK1, FILE_LINK2]
) -> pd.DataFrame:
    """The function loads data from a list of links, concats them into a DataFrame and returns it"""

    data = [pd.read_csv(data_link) for data_link in data_links]
    data = pd.concat(data, axis=0, ignore_index=True)

    return data


def transorm_data(
    df: pd.DataFrame = None, product_name: str = "pink morsel"
) -> pd.DataFrame:
    """The function transforms data.
    It chooses `product_name` products, calculates sales and deletes unnecessary columns
    """

    if df is None:
        raise ValueError("No data provided!")

    data = df[df["product"] == product_name]
    data["price"] = data["price"].str.replace("$", "").astype(float)
    data["sales"] = data["price"] * data["quantity"]
    data = data.drop(columns=["product", "price", "quantity"])

    return data


def save_data(df: pd.DataFrame = None, save_path: str = "data/sales_data.csv") -> None:
    """Saves data to `save_path`"""

    if df is None:
        raise ValueError("No data provised!")

    df.to_csv(save_path, index=False)


def main():
    data = load_data()
    data = transorm_data(data)
    save_data(data)


if __name__ == "__main__":
    main()
