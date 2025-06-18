"""
Created on Thu Sep 12 17:17:32 2024

@author: e.mulholland@theicct.org
Additional figures: a.musa@theicct.org ; Supervisor: Hussein Basma
"""

import sys

# Inputs to be defined
# some error
folder_location = r"/Users/e.mulholland/Documents/Work 2025/EU/RtZ/Q1/RtZ_formatter_folder2025"
code_directory = folder_location + "/code"
input_file_name = "Dataforce ICCT CV 2025Q1.csv"
year = "2025"
quarter = "Q1"

# Add the code directory to the system path
sys.path.append(code_directory)

import preprocessing
import axle_mapping
import bus_assignment
import bus_manual_correct
import processing


def main():    
    preprocessing.run_preprocessing(folder_location, input_file_name, "Dataforce_" +quarter+"_"+year+".csv")
    axle_mapping.axle_gvw_maps(
        RtZ_folder_location=folder_location,
        input_file_new="Dataforce_" +quarter+"_"+year+".csv",
        input_file_old="IHS_annual_master.csv",
        gvw_map_file="gvw_map_index.csv",
        output_file="Dataforce_" +quarter+"_"+year+"_axle_corrected.csv")
    
    bus_assignment.bus_type_assignment(folder_location, "bus_types.csv",
                      "Dataforce_" +quarter+"_"+year+".csv", 
                      "bus_sales_with_types_dataforce_"+year+"_"+quarter+".csv")
    
    bus_manual_correct.correct_bus_type_classification(folder_location, "bus_sales_with_types_dataforce_"+year+"_"+quarter+".csv", "bus_sales_corrected_"+year+"_"+quarter+".csv")
    processing.sorting_code(folder_location, year, quarter,"/outputs/Dataforce_"+quarter+"_"+year+"_formatted_data.xlsx")
    

if __name__ == "__main__":
    main()
