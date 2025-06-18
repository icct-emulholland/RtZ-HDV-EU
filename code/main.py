"""
Created on Thu Sep 12 17:17:32 2024

@author: e.mulholland@theicct.org
Additional figures: a.musa@theicct.org ; Supervisor: Hussein Basma
"""

import sys
import os

# Define the path to the code directory
code_directory = r"/Users/e.mulholland/Documents/Work 2025/EU/RtZ/Q1/RtZ_formatter_folder2025/code"

# Add the code directory to the system path
sys.path.append(code_directory)

import preprocessing
import axle_mapping
import bus_assignment
import bus_manual_correct
import processing


def main():
    folder_location = r"/Users/e.mulholland/Documents/Work 2025/EU/RtZ/Q1/RtZ_formatter_folder2025"
    
    preprocessing.run_preprocessing(folder_location, "Dataforce ICCT CV 2025Q1.csv", "Dataforce_Q1_2025.csv")
    
    
    axle_mapping.axle_gvw_maps(
        RtZ_folder_location=folder_location,
        input_file_new="Dataforce_Q1_2025.csv",
        input_file_old="IHS_annual_master.csv",
        gvw_map_file="gvw_map_index.csv",
        output_file="Dataforce_Q1_2025_axle_corrected.csv")
    
    bus_assignment.bus_type_assignment(folder_location, "bus_types.csv",
                      "Dataforce_Q1_2025.csv", 
                      "bus_sales_with_types_dataforce_Q1.csv")
    bus_manual_correct.correct_bus_type_classification(folder_location, "bus_sales_with_types_dataforce_Q1.csv", "bus_sales_corrected_Q1.csv")

    
    processing.sorting_code(folder_location, "2025", "Q1","/outputs/Dataforce_Q1_2025_formatted_data.xlsx")
    

if __name__ == "__main__":
    main()

