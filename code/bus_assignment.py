# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 10:38:58 2024

@author: a.musa
"""

import os
import pandas as pd
from thefuzz import process

def load_data(folder_location: str, bus_types_file: str, bus_sales_file: str) -> tuple:
    """
    Load the bus types and sales data from the specified CSV files.

    :param folder_location: The directory where the input files are stored.
    :param bus_types_file: The name of the CSV file containing bus types data.
    :param bus_sales_file: The name of the CSV file containing bus sales data.
    :return: A tuple of DataFrames: (bus_types_df, bus_sales_df).
    """
    bus_types_df = pd.read_csv(os.path.join(folder_location, "inputs", bus_types_file), encoding='ISO-8859-1')
    bus_sales_df = pd.read_csv(os.path.join(folder_location, "inputs", bus_sales_file))
    return bus_types_df, bus_sales_df

def filter_bus_sales(bus_sales_df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter the bus sales data to include only entries where the body group is "Bus".

    :param bus_sales_df: The DataFrame containing the bus sales data.
    :return: A filtered DataFrame with only bus-related sales data.
    """
    return bus_sales_df[bus_sales_df["Body group"] == "Bus"].copy()

def match_bus_types(bus_sales_df: pd.DataFrame, bus_types_df: pd.DataFrame) -> pd.DataFrame:
    """
    Match the bus types to the sales data using fuzzy matching based on manufacturer and sub-model.

    :param bus_sales_df: The DataFrame containing the bus sales data.
    :param bus_types_df: The DataFrame containing the bus types data.
    :return: The bus sales DataFrame with the bus types and base model columns added.
    """
    choices = list(bus_types_df.apply(lambda row: f"{row['manufacturer']} {row['model']}", axis=1))
    
    def find_closest_match(row):
        manufacturer_model_sales = f"{row['Manufacturer']} {row['Sub-Model-Short']}"
        match, score = process.extractOne(manufacturer_model_sales, choices)
        return match, score

    matches = bus_sales_df.apply(find_closest_match, axis=1)
    
    bus_sales_df['bus_type'] = [bus_types_df[bus_types_df['manufacturer'] + " " + bus_types_df['model'] == m]['type'].iloc[0] if m else None for m, s in matches]
    bus_sales_df['Base Model'] = [m if m else None for m, s in matches]

    return bus_sales_df

def handle_unspecified_models(bus_sales_df: pd.DataFrame) -> pd.DataFrame:
    """
    Update the bus types for entries with unspecified sub-models based on the fuel type.

    :param bus_sales_df: The DataFrame containing the bus sales data with matched bus types.
    :return: The updated DataFrame with corrected bus types for unspecified models.
    """
    electric_condition = (bus_sales_df["Fuel type"] == "Electric w/oREX") & (bus_sales_df["Sub-Model-Short"].str.contains("unspec", case=False))
    non_electric_condition = (bus_sales_df["Fuel type"] != "Electric w/oREX") & (bus_sales_df["Sub-Model-Short"].str.contains("unspec", case=False))
    
    bus_sales_df.loc[electric_condition, "bus_type"] = "City bus"
    bus_sales_df.loc[non_electric_condition, "bus_type"] = "Unknown"
    
    return bus_sales_df

def save_data(bus_sales_df: pd.DataFrame, folder_location: str, output_file: str):
    """
    Save the updated bus sales data to a CSV file.

    :param bus_sales_df: The DataFrame containing the updated bus sales data.
    :param folder_location: The directory where the output file should be saved.
    :param output_file: The name of the output CSV file.
    """
    output_path = os.path.join(folder_location, "outputs", output_file)
    bus_sales_df.to_csv(output_path, index=False)

def bus_type_assignment(folder_location: str, bus_types_file: str, bus_sales_file: str, output_file: str):
    """
    Main function to process the bus sales data, match bus types, and handle unspecified models.

    :param folder_location: The directory where the input and output files are stored.
    :param bus_types_file: The name of the CSV file containing bus types data.
    :param bus_sales_file: The name of the CSV file containing bus sales data.
    :param output_file: The name of the output CSV file.
    """
    # Load data
    bus_types_df, bus_sales_df = load_data(folder_location, bus_types_file, bus_sales_file)
    
    # Filter bus sales data to include only buses
    bus_sales_df = filter_bus_sales(bus_sales_df)
    
    # Match bus types using fuzzy matching
    bus_sales_df = match_bus_types(bus_sales_df, bus_types_df)
    
    # Handle unspecified models based on fuel type
    bus_sales_df = handle_unspecified_models(bus_sales_df)
    
    # Save the updated data
    save_data(bus_sales_df, folder_location, output_file)
