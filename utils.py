import pandas as pd

from db import Connection


def read_address_table():
    with Connection() as conn:
        conn
    return pd.read_csv("addresses.csv", sep=";")


def add_to_table(name, address):
    name = name.replace(";", "")
    address = address.replace(";", "")

    with open("addresses.csv", "a") as f:
        f.write(f"{name}; {address}\n")
