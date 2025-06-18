# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 10:06:13 2024

@author: a.musa
"""

import os
import pandas as pd

def load_data(folder_location: str, gvw_map_file: str, input_file_old: str, input_file_new: str):
    """
    Load the necessary input data files.

    :param folder_location: The directory where the input files are stored.
    :param gvw_map_file: The name of the CSV file containing the axle configuration mapping.
    :param input_file_old: The name of the old input CSV file.
    :param input_file_new: The name of the new input CSV file.
    :return: A tuple of DataFrames: (axle_map, ihs_old, ihs_new).
    """
    axle_map = pd.read_csv(os.path.join(folder_location, "inputs", gvw_map_file))
    ihs_old = pd.read_csv(os.path.join(folder_location, "inputs", input_file_old))
    ihs_new = pd.read_csv(os.path.join(folder_location, "inputs", input_file_new))
    
    return axle_map, ihs_old, ihs_new

def prepare_input_data(ihs_old: pd.DataFrame, unknown_axles: list) -> pd.DataFrame:
    """
    Prepares the input data by removing unknown axle configurations and invalid GVWs.

    :param ihs_old: The DataFrame containing the old input data.
    :param unknown_axles: List of unknown axle configurations.
    :return: A DataFrame with cleaned data.
    """
    ihs_df_input_no_unknowns = ihs_old[~ihs_old["Axle configuration"].isin(unknown_axles)].copy()
    ihs_df_input_no_unknowns["Axle configuration"] = ihs_df_input_no_unknowns["Axle configuration"].str.replace(" ", "")
    ihs_df_input_no_unknowns = ihs_df_input_no_unknowns[ihs_df_input_no_unknowns["Gross vehicle weight"] > 0]
    return ihs_df_input_no_unknowns

def create_gvw_map(ihs_df_input_no_unknowns: pd.DataFrame, axle_map: pd.DataFrame, unknown_axles: list) -> pd.DataFrame:
    """
    Create the GVW/axle map by analyzing the input data.

    :param ihs_df_input_no_unknowns: The cleaned input data.
    :param axle_map: DataFrame containing the axle configuration mapping.
    :param unknown_axles: List of unknown axle configurations.
    :return: A DataFrame representing the GVW/axle map.
    """
    gvw_map_list = []
    upper_gvw = 101000

    for gvw in range(0, upper_gvw, 1000):
        row = {"low_gvw": gvw, "high_gvw": gvw + 1000}
        for unknown_axle in unknown_axles:
            ihs_df_input_mini = ihs_df_input_no_unknowns[
                (ihs_df_input_no_unknowns["Axle configuration"].isin(axle_map[axle_map[unknown_axle]]["axle_config"])) &
                (ihs_df_input_no_unknowns["Gross vehicle weight"] >= gvw) &
                (ihs_df_input_no_unknowns["Gross vehicle weight"] < gvw + 1000)
            ]
            if ihs_df_input_mini.empty:
                row[unknown_axle] = ""
            else:
                most_popular_seg = ihs_df_input_mini[["Axle configuration", "Sales"]].groupby(["Axle configuration"]).sum().reset_index()
                if most_popular_seg["Sales"].value_counts().max() > 1:
                    most_popular_seg = most_popular_seg.sort_values('Sales', ascending=False).head(1)["Axle configuration"].item()
                else:
                    most_popular_seg = most_popular_seg[most_popular_seg["Sales"] == most_popular_seg["Sales"].max()]["Axle configuration"].item()
                row[unknown_axle] = most_popular_seg
        gvw_map_list.append(row)

    gvw_map = pd.DataFrame(gvw_map_list)
    gvw_map = pd.melt(gvw_map, id_vars=["low_gvw", "high_gvw"])
    gvw_map = gvw_map.dropna()
    gvw_map = gvw_map[gvw_map["value"] != ""]
    gvw_map.loc[gvw_map['high_gvw'] == upper_gvw, 'high_gvw'] = 999999
    
    return gvw_map

def create_axle_map_for_unspecified_gvw(ihs_old: pd.DataFrame, axle_map: pd.DataFrame, unknown_axles: list) -> pd.DataFrame:
    """
    Create a mapping for unspecified GVWs using the most popular axle configurations.

    :param ihs_old: DataFrame containing the old input data.
    :param axle_map: DataFrame containing the axle configuration mapping.
    :param unknown_axles: List of unknown axle configurations.
    :return: A DataFrame mapping unknown axles to the most popular configurations.
    """
    ihs_df_input_no_unknowns_all_gvw = ihs_old[~ihs_old["Axle configuration"].isin(unknown_axles)].copy()
    ihs_df_input_no_unknowns_all_gvw["Axle configuration"] = ihs_df_input_no_unknowns_all_gvw["Axle configuration"].str.replace(" ", "")
    
    gvw_unk_map = pd.DataFrame(data=unknown_axles, columns=["unknown_axles"])

    for unknown_axle in unknown_axles:
        ihs_df_input_mini = ihs_df_input_no_unknowns_all_gvw[
            ihs_df_input_no_unknowns_all_gvw["Axle configuration"].isin(axle_map[axle_map[unknown_axle]]["axle_config"])
        ]
        most_popular_seg = ihs_df_input_mini[["Axle configuration", "Sales"]].groupby(["Axle configuration"]).sum().reset_index()
        if most_popular_seg["Sales"].value_counts().max() > 1:
            most_popular_seg = most_popular_seg.sort_values('Sales', ascending=False).head(1)["Axle configuration"].item()
        else:
            most_popular_seg = most_popular_seg[most_popular_seg["Sales"] == most_popular_seg["Sales"].max()]["Axle configuration"].item()
        gvw_unk_map.loc[gvw_unk_map["unknown_axles"] == unknown_axle, "new_val"] = most_popular_seg

    return gvw_unk_map

def replace_unspecified_axles(ihs_new: pd.DataFrame, gvw_map: pd.DataFrame, gvw_unk_map: pd.DataFrame, unknown_axles: list) -> pd.DataFrame:
    """
    Replace unspecified axle configurations with the most likely ones based on GVW.

    :param ihs_new: DataFrame containing the new input data.
    :param gvw_map: DataFrame representing the GVW/axle map.
    :param gvw_unk_map: DataFrame mapping unknown axles to the most popular configurations.
    :param unknown_axles: List of unknown axle configurations.
    :return: A DataFrame with corrected axle configurations.
    """
    gvw_map = pd.pivot_table(gvw_map, values='value', index=['low_gvw', 'high_gvw'], columns='variable', aggfunc=','.join).reset_index()

    for ax in unknown_axles:
        GVW_map_mini = gvw_map[['low_gvw', 'high_gvw', ax]].copy()
        GVW_map_mini = GVW_map_mini.rename(columns={ax: 'Axle configuration'})

        unspec_axle = ihs_new[(ihs_new['Axle configuration'] == ax) & (ihs_new['Gross vehicle weight'] > 0)].copy()
        ihs_new = ihs_new[~((ihs_new['Axle configuration'] == ax) & (ihs_new['Gross vehicle weight'] > 0))]

        GVW_map_mini.index = pd.IntervalIndex.from_arrays(GVW_map_mini['low_gvw'], GVW_map_mini['high_gvw'], closed='left')
        unspec_axle['Axle configuration'] = unspec_axle['Gross vehicle weight'].apply(
            lambda x: GVW_map_mini.iloc[GVW_map_mini.index.get_loc(x)]['Axle configuration']
        )

        ihs_new = pd.concat((ihs_new, unspec_axle), axis=0)

    ihs_new = ihs_new.merge(gvw_unk_map, left_on="Axle configuration", right_on="unknown_axles", how="left")
    ihs_new.loc[ihs_new["Axle configuration"].isin(unknown_axles), "Axle configuration"] = ihs_new["new_val"]
    ihs_new["Axle configuration"] = ihs_new["Axle configuration"].str.replace(" ", "")
    ihs_new = ihs_new.drop(['unknown_axles', 'new_val'],axis = 1)
    
    return ihs_new

def axle_gvw_maps(RtZ_folder_location: str, input_file_new: str, input_file_old: str, gvw_map_file: str, output_file: str):
    """
    Main function to process the input data files to create a GVW/axle map and correct unspecified axle configurations.

    :param RtZ_folder_location: The directory where the input and output files are stored.
    :param input_file_new: The name of the new input CSV file.
    :param input_file_old: The name of the historical data input CSV file.
    :param gvw_map_file: The name of the CSV file containing the axle configuration mapping.
    :param output_file: The name of the output CSV file.
    """
    # Load input data
    axle_map, ihs_old, ihs_new = load_data(RtZ_folder_location, gvw_map_file, input_file_old, input_file_new)
    
    # Define unknown axles
    unknown_axles = list(axle_map.columns)
    unknown_axles.remove('axle_config')

    # Prepare the input data
    ihs_df_input_no_unknowns = prepare_input_data(ihs_old, unknown_axles)

    # Create GVW map
    gvw_map = create_gvw_map(ihs_df_input_no_unknowns, axle_map, unknown_axles)
    
    # Create axle map for unspecified GVWs
    gvw_unk_map = create_axle_map_for_unspecified_gvw(ihs_old, axle_map, unknown_axles)
    
    # Replace unspecified axles with likely configurations
    ihs_new = replace_unspecified_axles(ihs_new, gvw_map, gvw_unk_map, unknown_axles)
    
    # Save the corrected data
    ihs_new.to_csv(os.path.join(RtZ_folder_location, "inputs", output_file), index=False)
