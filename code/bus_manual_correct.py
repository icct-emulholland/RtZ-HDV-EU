import pandas as pd
import os

def correct_bus_type_classification(folder_location: str, input_file: str, output_file: str):
    """
    Correct the bus type classification by setting the bus_type to an empty cell
    for specific models that are incorrectly classified as "City bus."

    :param folder_location: The directory where the input and output files are stored.
    :param input_file: The name of the CSV file containing the bus sales data to be corrected.
    :param output_file: The name of the output CSV file to save the corrected data.
    """
    # Load the data
    file_path = os.path.join(folder_location, "outputs", input_file)
    bus_sales_df = pd.read_csv(file_path)
    
    # List of model names to check for (exact match)
    models_to_correct = [
        "DAF LF Series", "Ford Transit", "MAN HOCL Chassis A67", "Mercedes Sprinter", 
        "Peugeot Boxer","Renault Master", "VDL Bova Futura", "VW Crafter"
    ]
    
    # Correct bus_type for specific models if classified as "City bus"
    for model in models_to_correct:
        condition = (bus_sales_df['Model'] == model) & (bus_sales_df['bus_type'] == "City bus")
        bus_sales_df.loc[condition, 'bus_type'] = ""

    # Save the corrected data
    output_path = os.path.join(folder_location, "outputs", output_file)
    bus_sales_df.to_csv(output_path, index=False)
