import pandas as pd


def read_address_table():
    return pd.read_csv("addresses.csv", sep=";")


def add_to_table(name, address):
    name = name.replace(";", "")
    address = address.replace(";", "")

    with open("addresses.csv", "a") as f:
        f.write(f"{name}; {address}\n")
