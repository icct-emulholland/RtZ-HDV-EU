"""
Created on Thu Sep 12 17:17:32 2024

@author: e.mulholland@theicct.org
Additional figures: a.musa@theicct.org ; Supervisor: Hussein Basma
"""

import os
import pandas as pd
import pdb
def load_data(folder_location: str, data_file: str) -> pd.DataFrame:
    """
    Load the data from the specified CSV file located in the folder.

    :param folder_location: The directory where the input files are stored.
    :param data_file: The name of the CSV file to load.
    :return: A DataFrame containing the loaded data.
    """
    data_path = os.path.join(folder_location, "inputs", data_file)
    data = pd.read_csv(data_path)
    return data

def clean_drivetrain_labels(label: str) -> str:
    """
    Clean and standardize the drivetrain labels from the input data.

    :param label: The drivetrain label to clean.
    :return: A cleaned and standardized drivetrain label.
    """
    parts = label.split()
    
    # Check if the label contains an 'x' and if it represents a valid axle configuration
    if len(parts) > 0 and 'x' in parts[0]:
        number_parts = parts[0].split('x')
        
        if len(number_parts) == 2 and all(part.isdigit() for part in number_parts):
            # Return the upper-cased label if it matches the format
            if len(parts) == 1 or (len(parts) > 1 and parts[1] in ['RWD', 'FWD', 'AWD']):
                return parts[0].upper()
        
        # Handle cases where the label indicates the number of axles
        if len(number_parts) == 2 and number_parts[1] == '' and number_parts[0].isdigit():
            number = int(int(number_parts[0])/2)
            return f"{number} axles"
    
    # Return "Unspecified" if the label doesn't meet the criteria
    return "Unspecified"

def preprocess_axle_gvw(ihs_new: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the axle and gross vehicle weight data.

    :param ihs_new: The DataFrame containing the raw input data.
    :return: A DataFrame with the cleaned axle configuration and gross vehicle weight.
    """
    # Apply the drivetrain label cleaning function
    ihs_new['Axle configuration'] = ihs_new['DRIVETRAIN_2'].apply(clean_drivetrain_labels)
    
    # Copy TOTALWEIGHT to a new column if it exists
    if 'TOTALWEIGHT' in ihs_new.columns:
        ihs_new['Gross vehicle weight'] = ihs_new['TOTALWEIGHT']
    
    return ihs_new

def preprocess_bus_assignment(ihs_new: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the bus assignment data, creating separate columns for each quarter's registrations.

    :param ihs_new: The DataFrame containing the raw input data.
    :return: A DataFrame with separate columns for each quarter's registrations, if present.
    """
    # Create a new column that strips the brand from the model name
    ihs_new['Sub-Model-Short'] = ihs_new.apply(lambda row: row['MODEL'].replace(row['BRAND'], '').strip(), axis=1)

    # List of quarters to check
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    years = ihs_new["REG_DATE"].str[:4].astype(int).unique()

    # Initialize and populate columns for each present quarter
    for year in years:
        for quarter in quarters:
            # Only create the column if that quarter's data is present
            if f'{year}-{quarter}' in ihs_new['REG_DATE'].unique():
                ihs_new[f'{quarter}_{year}'] = 0
                ihs_new.loc[ihs_new['REG_DATE'] == f'{year}-{quarter}', f'{quarter}_{year}'] = ihs_new['REGS']

    # Standardize fuel type names
    ihs_new['Fuel type'] = ihs_new['FUELTYPE'].replace({
        'Gas': 'Natural Gas',
        'Electric': 'Electric w/oREX',
        'Plug-In-Hybrid': 'HEV/Dsl.PlugIn',
        'Hybrid': 'HEV/Dsl.',
        'Other': 'Unspecified'
    })
    
    # Aggregate specific countries into a single category and filter out others
    ihs_new['Country'] = ihs_new['COUNTRY']
    
    ihs_new = ihs_new[~ihs_new['Country'].isin(['Iceland', 'Norway', 'Switzerland'])]
    
    # Standardize body group and body type columns
    ihs_new['Body group'] = ihs_new['BODYSTYLE_2'].copy()
    ihs_new['Body type'] = ihs_new['BODYSTYLE_3'].replace('Semi-Trailer Truck', 'HCV Tractor Truck').copy()
    
    # Rename specific columns for consistency
    ihs_new.rename(columns={
        'BRAND': 'Manufacturer',       
        'COUNTRY': 'COUNTRY_OR',
        'MODEL': 'Model',
    }, inplace=True)
    
    return ihs_new

def save_preprocessed_data(ihs_new: pd.DataFrame, folder_location: str, output_file: str):
    """
    Save the preprocessed data to a CSV file.

    :param ihs_new: The DataFrame containing the preprocessed data.
    :param folder_location: The directory where the output file should be saved.
    :param output_file: The name of the CSV file to save the data.
    """
    output_path = os.path.join(folder_location, "inputs", output_file)
    # pdb.set_trace()
    
    ihs_new.to_csv(output_path, index=False)

def run_preprocessing(folder_location: str, input_file: str, output_file: str):
    """
    The main function to load, preprocess, and save the data.

    :param folder_location: The directory where the input and output files are stored.
    :param input_file: The name of the CSV file to load.
    :param output_file: The name of the CSV file to save the processed data.
    """
    
    # Load the data from the specified file
    ihs_new = load_data(folder_location, input_file)
    
    # Preprocess the axle and gross vehicle weight data
    ihs_new = preprocess_axle_gvw(ihs_new)
    
    # Preprocess the bus assignment data and handle quarterly registrations
    ihs_new = preprocess_bus_assignment(ihs_new)
    
    # Save the preprocessed data to the output file
    save_preprocessed_data(ihs_new, folder_location, output_file)
