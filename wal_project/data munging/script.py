import pandas as pd
import sqlite3
import os
from typing import List

def create_connection(path:str) -> sqlite3.Connection | int:
    """Creates connection to SQLite3 database and returns it. Returns -1 if fails"""

    try:
        conn = sqlite3.connect(database=path)
    except sqlite3.Error:
        conn = -1

    return conn

def extract_data(folder_path:str) -> List[pd.DataFrame]:
    """Extracts data from csv files.\n
    Accepts a path string, return a dataframe"""
    paths = [folder_path + csv_path for csv_path in sorted(os.listdir(folder_path))]
    res = []
    for path in paths:
        res.append(pd.read_csv(path))

    return res

def transform_data(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """For data 1 and 2. Aggregate the first one and join with the second one.\n
    Accepts two dataframes, returns a transformed dataframe"""

    product_quantity = df1.groupby("product")["on_time"].count().reset_index()
    product_quantity = dict(zip(product_quantity["product"], product_quantity["on_time"]))
    joined_tables = pd.merge(left=df1, right=df2, on="shipment_identifier")
    joined_tables = joined_tables.drop_duplicates().drop(columns="shipment_identifier")
    joined_tables["product_quantity"] = joined_tables["product"].apply(lambda x: product_quantity[x])

    return joined_tables

def get_products(dfs:List[pd.DataFrame]) -> pd.DataFrame:
    """Gets products from all the data"""

    products = pd.DataFrame({"name":[""]})
    for df in dfs:
        products = pd.concat([products, df[["product"]]], axis=0, ignore_index=True)
    products = pd.DataFrame({"name":products["product"].unique()}).dropna()

    return products

def send_data_to_sql(df:pd.DataFrame, table:str, conn:sqlite3.Connection) -> int:
    """Saves data to SQLite3 database.\n
    Accepts a dataframe, table name, and connection, then returns a staus code."""
    try:
        df.to_sql(name=table, con=conn, index_label="id", method="multi", if_exists="replace")
        return 0
    except Exception as e:
        print(e)
        return 1

def main():
    """Main function"""

    conn = create_connection(path="../shipment_database.db")

    # checking connection status
    if conn == -1:
        print("Connection failed")
        return
    
    dfs = extract_data("../data/")
    products = get_products(dfs[0:2])
    joined_first_second = transform_data(dfs[1], dfs[2])

    # joining all shipment data
    all_data = pd.concat([dfs[0], joined_first_second], ignore_index=True, axis=0)

    # sending products to sql
    not_sqled_products = send_data_to_sql(products, table="product", conn=conn)
    if not not_sqled_products:
        print("Products sql-ed successfully!")
    else:
        print("Products are still here!")

    # sending shipment data to sql
    not_sqled_data = send_data_to_sql(all_data, table="shipment", conn=conn)
    if not not_sqled_data:
        print("Data sql-ed successfully!")
    else:
        print("Data are still here!")


if __name__ == "__main__":
    main()