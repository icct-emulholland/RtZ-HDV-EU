"""
Created on Thu Sep 12 17:17:32 2024

@author: e.mulholland@theicct.org
Additional figures: a.musa@theicct.org ; Supervisor: Hussein Basma
"""
import pandas as pd
from pandas import ExcelWriter
from fuzzywuzzy import process
import os
import pdb

# =============================================================================
# Inputs - update with year/quarter and point towards local copy
# =============================================================================

def sorting_code(RtZ_folder_location, year, quarter, output_file):
    year = year
    quarter = quarter    
    #output file
    xls_path = RtZ_folder_location + output_file 
    
    # =============================================================================
    # Appending ihs_data with bus_data
    # =============================================================================

    historic_ihs_data = pd.read_csv(RtZ_folder_location + "/inputs/IHS_annual_master.csv")
    previous_year_quarterly = pd.read_csv(RtZ_folder_location + "/inputs/Dataforce_Q4_2024_axle_corrected.csv")
    ihs_data = pd.read_csv(RtZ_folder_location + "/inputs/Dataforce_Q1_2025_axle_corrected.csv")
    bus_data = pd.read_csv(RtZ_folder_location + "/outputs/bus_sales_corrected_Q1.csv") #bus_sales_with_types
    fuel_map = pd.read_csv(RtZ_folder_location + "/inputs/fuel_map.csv")
    list_of_zev_models = pd.read_csv(RtZ_folder_location + "/inputs/zev_models_chars.csv")
    city_buses_pt = pd.read_csv(RtZ_folder_location + "/inputs/city_bus_pt_share.csv")

    ihs_data = ihs_data[ihs_data["Body group"] != "Bus"]
    ihs_data = ihs_data.append(bus_data.drop('Base Model', axis=1))
    
    # =============================================================================
    # Formatting IHS data
    # =============================================================================
    
    # Creating lists for quarterly sales columns and the corresponding periods
    quarterly_sales_columns = []
    periods = []
    for qs in range(0,int(quarter[1])):
        periods.append(year + " Q" + str(qs+1))
        quarterly_sales_columns.append("Q" + str(qs+1) + "_" + year)
    period = year + " " + quarter
    quarterly_sales_column = quarter + "_" + year
    
    # Defining columns and ISO country codes for historical and quarterly sales
    historic_sales_column = "Sales"
    # quarterly_EU_27_ISOs = ['Austria', 'Denmark', 'Finland', 'France', 'Germany', 'Greece', 'Italy', 'Netherlands', 'Portugal', 'Spain', 'Sweden', 'aggregated Level EU 12', 'Belgium', 'Ireland', 'Luxembourg']
    historic_EU_27_ISOs = ['Austria', 'Belgium', 'Denmark', 'EU', 'Finland', 'France', 'Germany', 'Greece', 'Ireland', 'Italy', 'Luxembourg', 'Netherlands', 'Portugal', 'Spain', 'Sweden']
    
    # Identifying unique fuel types in the datasets and checking for new fuel types not in the fuel map
    unique_fuels_quarterly = set(list(ihs_data["Fuel type"].unique()))
    unique_fuels_annual = set(list(historic_ihs_data["Fuel type"].unique()))
    combined_unique_fuels = set(list(ihs_data["Fuel type"].unique()) + list(unique_fuels_annual - unique_fuels_quarterly))
    unique_fuel_map = set(list(fuel_map["Fuel type"].unique()))
    new_fuel_types = list(combined_unique_fuels - unique_fuel_map)
    
    # Warning if new fuel types are detected
    if len(new_fuel_types) > 0:
        print("CAUTION: New fuel types detected")
        print("list of new fuels:")
        for new_fuel in new_fuel_types:
            print(new_fuel)
    
    # Renaming 'sales' column in bus_data to match the format of the quarterly sales column
    bus_data = bus_data.rename(columns = {"sales":quarterly_sales_column})
    
    # Filtering IHS data for the relevant countries based on ISO codes
    # ihs_data = ihs_data[ihs_data["Country"].isin(quarterly_EU_27_ISOs)]
    historic_ihs_data = historic_ihs_data[historic_ihs_data["Country"].isin(historic_EU_27_ISOs)]
    # pdb.set_trace()
    # Classifying body groups into 'Truck', 'Bus', or other categories based on certain conditions
    ihs_data["RtZ Body group"] = "Truck"
    ihs_data.loc[(ihs_data["Body group"].str.contains("Unspec")) & (ihs_data["Body type"].str.contains("Truck")),"RtZ Body group"] = "Truck"
    ihs_data.loc[(ihs_data["Body group"].str.contains("Bus")) | (ihs_data["Body type"].str.contains("BUS")) ,"RtZ Body group"] = "Bus"
    
    ihs_data.loc[ihs_data["RtZ Body group"] == "Bus","RtZ_group"] = "Buses and coaches"
    ihs_data.loc[(ihs_data["RtZ Body group"] != "Bus") & (ihs_data["RtZ Body group"] != "Unknown") & (ihs_data["Gross vehicle weight"] >= 12000),"RtZ_group"] = "Heavy trucks"
    ihs_data.loc[(ihs_data["RtZ Body group"] != "Bus") & (ihs_data["RtZ Body group"] != "Unknown") & (ihs_data["Gross vehicle weight"] < 12000) & (ihs_data["Gross vehicle weight"] >= 0),"RtZ_group"] = "Light and medium trucks"
    
    # Similar classification for historic IHS data
    historic_ihs_data["Body group"] = "Truck"
    historic_ihs_data.loc[(historic_ihs_data["Body type"].str.contains("Unspec")) & (historic_ihs_data["Body type"].str.contains("Truck")),"Body group"] = "Truck"
    historic_ihs_data.loc[(historic_ihs_data["Body type"].str.contains("Bus")) | (historic_ihs_data["Body type"].str.contains("BUS")) ,"Body group"] = "Bus"
    
    historic_ihs_data.loc[(historic_ihs_data["Body group"] == "Bus"),"RtZ_group"] = "Buses and coaches"
    historic_ihs_data.loc[(historic_ihs_data["Body group"] != "Bus") & (historic_ihs_data["Body group"] != "Unknown") & (historic_ihs_data["Gross vehicle weight"] >= 12000),"RtZ_group"] = "Heavy trucks"
    historic_ihs_data.loc[(historic_ihs_data["Body group"] != "Bus") & (historic_ihs_data["Body group"] != "Unknown") & (historic_ihs_data["Gross vehicle weight"] < 12000) & (historic_ihs_data["Gross vehicle weight"] >= 0),"RtZ_group"] = "Light and medium trucks"
    
    # Merging fuel mapping data with IHS data
    ihs_data = ihs_data.merge(fuel_map,left_on = ["Fuel type"], right_on = ["Fuel type"], how = "left")
    historic_ihs_data = historic_ihs_data.merge(fuel_map,left_on = ["Fuel type"], right_on = ["Fuel type"], how = "left")
    
    
    ihs_data.loc[ihs_data["Manufacturer"]=="Karsan","RtZ_group"] = "Buses and coaches"
    historic_ihs_data.loc[historic_ihs_data["Manufacturer"]=="Karsan","RtZ_group"] = "Buses and coaches"
    # pdb.set_trace()
    
    # =============================================================================
    # pt_shares
    # =============================================================================
    
    ihs_trucks = ihs_data[ihs_data["RtZ_group"] != "Buses and coaches"].copy()
    ihs_buses = ihs_data[ihs_data["RtZ_group"] == "Buses and coaches"].copy()
    
    ihs_truck_shares = ihs_trucks[["RtZ_group","fuel",quarterly_sales_column]].groupby(["RtZ_group","fuel"]).sum().reset_index()
    ihs_bus_shares = ihs_buses[["bus_type","fuel",quarterly_sales_column]].groupby(["bus_type","fuel"]).sum().reset_index()
    ihs_bus_shares["RtZ_group"] = ihs_bus_shares["bus_type"]
    ihs_bus_shares = ihs_bus_shares.drop('bus_type', axis=1)
    ihs_data_shares = ihs_truck_shares.append(ihs_bus_shares)
    
    ihs_data_shares[quarterly_sales_column] = ihs_data_shares[quarterly_sales_column].fillna(0)
    ihs_data_shares = ihs_data_shares.merge(ihs_data_shares.groupby(["RtZ_group"]).sum().reset_index(), left_on = ["RtZ_group"], right_on = ["RtZ_group"], how = "left") 
    ihs_data_shares["shares"] = ihs_data_shares[quarterly_sales_column + "_x"]/ihs_data_shares[quarterly_sales_column + "_y"]
    ihs_data_shares = ihs_data_shares[["RtZ_group","fuel","shares"]]
    # pdb.set_trace()
    # =============================================================================
    # Total sales
    # =============================================================================
    
    historic_ihs_data_sales = historic_ihs_data[["RtZ_group","fuel","Sales","Year"]].groupby(["RtZ_group","fuel","Year"]).sum().reset_index().copy()
    
    historic_ihs_data_all_sales = historic_ihs_data[["RtZ_group","Sales","Year"]].groupby(["RtZ_group","Year"]).sum().reset_index()
    historic_ihs_data_all_sales = historic_ihs_data_all_sales.rename(columns = {"Year":"Period"})
          
    for i, quarterly_data in enumerate(quarterly_sales_columns):
        ihs_data_sales = ihs_data[["RtZ_group","fuel",quarterly_data]].groupby(["RtZ_group","fuel"]).sum().reset_index()   
        
        ihs_data_all_sales = ihs_data_sales.groupby(["RtZ_group"]).sum().reset_index()
        ihs_data_all_sales = ihs_data_all_sales.rename(columns = {quarterly_data:"Sales"})
        ihs_data_all_sales["Period"] = periods[i]
        if i == 0:
            quaterly_data_all_sales = ihs_data_all_sales
        else:
            quaterly_data_all_sales = quaterly_data_all_sales.append(ihs_data_all_sales)
        
    
        ihs_data_sales = ihs_data_sales[ihs_data_sales["fuel"].isin(["BEV","FCEV"])]
       
        
        ihs_data_sales = ihs_data_sales.rename(columns = {quarterly_data:"Sales"})
        ihs_data_sales["Period"] = periods[i]
        
        if i == 0:
            quaterly_data_ft = ihs_data_sales
        else:
            quaterly_data_ft = quaterly_data_ft.append(ihs_data_sales)


    quaterly_data_all_sales = quaterly_data_all_sales.append(historic_ihs_data_all_sales)    
    historic_ihs_data_sales = historic_ihs_data_sales[historic_ihs_data_sales["fuel"].isin(["BEV","FCEV"])]
    historic_ihs_data_sales = historic_ihs_data_sales.rename(columns = {"Year":"Period"})
    
    quaterly_data_ft = quaterly_data_ft.append(historic_ihs_data_sales)
    quaterly_data_ft = quaterly_data_ft.merge(quaterly_data_all_sales, left_on = ["RtZ_group","Period"], right_on = ["RtZ_group","Period"], how = "left")
    quaterly_data_ft["shares"] = quaterly_data_ft["Sales_x"]/quaterly_data_ft["Sales_y"]
    quaterly_data_ft = quaterly_data_ft.rename(columns = {"Sales_x":"Sales"})
    quaterly_data_ft = quaterly_data_ft[["RtZ_group","fuel","Sales","Period","shares"]]


    # =============================================================================
    # sales by vehicle type
    # =============================================================================
       
    ihs_data_sales_type = ihs_data.copy()
    ihs_data_sales_type["Axle configuration"] = ihs_data_sales_type["Axle configuration"].str.replace(' ', '')
    ihs_data_sales_type.loc[ihs_data_sales_type["fuel"].isin(["BEV","FCEV"]),"fuel_short"] = "ZEV"
    ihs_data_sales_type.loc[~ihs_data_sales_type["fuel"].isin(["BEV","FCEV"]),"fuel_short"] = "ICE"
    heavy_trucks = ihs_data_sales_type[ihs_data_sales_type["RtZ_group"]=="Heavy trucks"].copy()
    light_med_trucks = ihs_data_sales_type[ihs_data_sales_type["RtZ_group"]=="Light and medium trucks"].copy()
    buses = ihs_data_sales_type[ihs_data_sales_type["RtZ_group"]=="Buses and coaches"].copy()
    heavy_trucks["veh_type_short"] = "Other"
    
     
    heavy_trucks.loc[(heavy_trucks["Axle configuration"].str.upper() == "4X2") & (heavy_trucks["Body type"] == "HCV Tractor Truck"), "veh_type_short"] = "4x2 tractor trailer"
    # heavy_trucks.to_csv(RtZ_folder_location + "/inputs/tmp.csv", index = False)
    # # Count occurrences where "Axle configuration" is "4X2" and "Body type" is "HCV Tractor Truck"
    # count_4x2_hcv_tractor_truck = heavy_trucks[(heavy_trucks["Axle configuration"] == "4X2") & 
    #                                            (heavy_trucks["Body type"] == "HCV Tractor Truck")].shape[0]
    # print(count_4x2_hcv_tractor_truck)
    
    
    heavy_trucks.loc[(heavy_trucks["Axle configuration"].str.upper() == "4X2") & ~(heavy_trucks["Body type"] == "HCV Tractor Truck"), "veh_type_short"] = "4x2 rigid truck"
    heavy_trucks.loc[(heavy_trucks["Axle configuration"].str.upper() == "6X2") & (heavy_trucks["Body type"] == "HCV Tractor Truck"), "veh_type_short"] = "6x2 tractor trailer"
    heavy_trucks.loc[(heavy_trucks["Axle configuration"].str.upper() == "6X2") & ~(heavy_trucks["Body type"] == "HCV Tractor Truck"), "veh_type_short"] = "6x2 rigid truck"
    heavy_trucks = heavy_trucks[["veh_type_short","fuel_short",quarterly_sales_column]].groupby(["veh_type_short","fuel_short"]).sum().reset_index()
    heavy_trucks = heavy_trucks.merge(heavy_trucks.groupby(["fuel_short"]).sum().reset_index(), left_on = ["fuel_short"], right_on = ["fuel_short"], how = "left") 
    heavy_trucks["shares"] = heavy_trucks[quarterly_sales_column + "_x"]/heavy_trucks[quarterly_sales_column + "_y"]
    heavy_trucks = heavy_trucks[["veh_type_short","fuel_short","shares"]]
    heavy_trucks["RtZ_group"] = "Heavy trucks"

    light_med_trucks["veh_type_short"] = "Other"
    light_med_trucks.loc[(light_med_trucks["Axle configuration"].str.upper() == "4X2") & (light_med_trucks["Body type"].str.contains("Van")), "veh_type_short"] = "4x2 van"
    light_med_trucks.loc[(light_med_trucks["Axle configuration"].str.upper() == "4X2") & ~(light_med_trucks["Body type"].str.contains("Van")), "veh_type_short"] = "4x2 truck"
    light_med_trucks.loc[(light_med_trucks["Axle configuration"].str.upper() == "4X4") & (light_med_trucks["Body type"].str.contains("Van")), "veh_type_short"] = "4x4 van"
    light_med_trucks.loc[(light_med_trucks["Axle configuration"].str.upper() == "4X4") & ~(light_med_trucks["Body type"].str.contains("Van")), "veh_type_short"] = "4x4 truck"
    light_med_trucks = light_med_trucks[["veh_type_short","fuel_short",quarterly_sales_column]].groupby(["veh_type_short","fuel_short"]).sum().reset_index()
    light_med_trucks = light_med_trucks.merge(light_med_trucks.groupby(["fuel_short"]).sum().reset_index(), left_on = ["fuel_short"], right_on = ["fuel_short"], how = "left") 
    light_med_trucks["shares"] = light_med_trucks[quarterly_sales_column + "_x"]/light_med_trucks[quarterly_sales_column + "_y"]
    light_med_trucks = light_med_trucks[["veh_type_short","fuel_short","shares"]]
    light_med_trucks["RtZ_group"] = "Light and medium trucks"
    
    veh_types = heavy_trucks.append(light_med_trucks)
    
    # =============================================================================
    # sales by top member states
    # =============================================================================
             
    all_ihs_data_ms_sales = ihs_data[["RtZ_group","fuel","Country",quarterly_sales_column]].copy()
    
    all_ihs_data_ms_sales = all_ihs_data_ms_sales[all_ihs_data_ms_sales["RtZ_group"]!="Unknown"]
    all_ihs_data_ms_sales.loc[all_ihs_data_ms_sales["Country"] == "aggregated Level EU 12", "Country"] = "Rest of EU-27"
    zev_ihs_data_ms_sales = all_ihs_data_ms_sales[all_ihs_data_ms_sales["fuel"].isin(["BEV","FCEV"])]
    zev_ihs_data_ms_sales = zev_ihs_data_ms_sales.groupby(["RtZ_group","Country"]).sum().reset_index()
    
    for i, veh_group in enumerate(list(zev_ihs_data_ms_sales["RtZ_group"].unique())):
        zev_ihs_data_ms_sales_mini = zev_ihs_data_ms_sales[zev_ihs_data_ms_sales["RtZ_group"] == veh_group].copy()       
        all_ihs_data_ms_sales_mini = all_ihs_data_ms_sales[all_ihs_data_ms_sales["RtZ_group"] == veh_group].copy()
        top_countries = zev_ihs_data_ms_sales_mini.sort_values(by=[quarterly_sales_column], ascending = False)["Country"].unique()
        # pdb.set_trace()
        top_countries = zev_ihs_data_ms_sales_mini.sort_values(by=[quarterly_sales_column], ascending = False).head(5)["Country"].unique()
        
        zev_ihs_data_ms_sales_mini.loc[~zev_ihs_data_ms_sales_mini["Country"].isin(top_countries),"Country"] = "Rest of EU-27"
        all_ihs_data_ms_sales_mini.loc[~all_ihs_data_ms_sales_mini["Country"].isin(top_countries),"Country"] = "Rest of EU-27"
        
        zev_ihs_data_ms_sales_mini = zev_ihs_data_ms_sales_mini.groupby(["RtZ_group","Country"]).sum().reset_index()
        all_ihs_data_ms_sales_mini = all_ihs_data_ms_sales_mini.groupby(["RtZ_group","Country"]).sum().reset_index()
        zev_ihs_data_ms_sales_mini = zev_ihs_data_ms_sales_mini.rename(columns = {quarterly_sales_column:"zev_sales"})
        all_ihs_data_ms_sales_mini = all_ihs_data_ms_sales_mini.rename(columns = {quarterly_sales_column:"all_sales"})
        zev_ihs_data_ms_sales_mini = zev_ihs_data_ms_sales_mini.merge(all_ihs_data_ms_sales_mini, left_on = ["RtZ_group","Country"], right_on = ["RtZ_group","Country"], how = "left")
        if i == 0:
            master_data_ms = zev_ihs_data_ms_sales_mini
        else:
            master_data_ms = master_data_ms.append(zev_ihs_data_ms_sales_mini)
     
    # =============================================================================
    # sales by all member states
    # =============================================================================
    # pdb.set_trace()
    all_historic_data_ms_sales = historic_ihs_data[["RtZ_group","fuel","Country","Year","Sales"]].copy()
    
    for i, quarterly_data in enumerate(quarterly_sales_columns):
    
        all_ihs_data_ms_sales = ihs_data[["RtZ_group","fuel","Country",quarterly_data]]
        # pdb.set_trace()
        
        ############### Change #################
        all_countries = all_ihs_data_ms_sales['Country'].unique()
        ############### Change #################
        
        all_ihs_data_ms_sales = all_ihs_data_ms_sales[all_ihs_data_ms_sales["fuel"].isin(["BEV","FCEV"])]
        
        
        ############### Change #################
        filtered_countries = all_ihs_data_ms_sales['Country'].unique()
        missing_countries = [country for country in all_countries if country not in filtered_countries]
        
        # Add missing countries with zero sales
        for country in missing_countries:
            # Get unique RtZ groups from the historic data
            rtz_groups = historic_ihs_data['RtZ_group'].unique()
            
            for rtz_group in rtz_groups:
                # For each RtZ group, check and add missing fuel types
                for fuel_type in ['BEV', 'FCEV']:
                    # Check if the current fuel type is missing in the filtered data for this country and RtZ group
                    if not ((all_ihs_data_ms_sales['Country'] == country) & (all_ihs_data_ms_sales['RtZ_group'] == rtz_group) & (all_ihs_data_ms_sales['fuel'] == fuel_type)).any():
                        new_row = {'RtZ_group': rtz_group, 'fuel': fuel_type, 'Country': country, quarterly_data: 0}
                        all_ihs_data_ms_sales = all_ihs_data_ms_sales.append(new_row, ignore_index=True)
                        
        all_ihs_data_ms_sales = all_ihs_data_ms_sales.sort_values(by='Country')
    
        ############### Change #################
        
        
        
        # pdb.set_trace()
        all_ihs_data_ms_sales = all_ihs_data_ms_sales.groupby(["RtZ_group","Country"]).sum().reset_index()
    
        all_ihs_data_ms_sales.loc[all_ihs_data_ms_sales["Country"]=="aggregated Level EU 12","Country"] = "Rest of EU-27"
        all_ihs_data_ms_sales = all_ihs_data_ms_sales.rename(columns = {quarterly_data:"Sales"})
        all_ihs_data_ms_sales = all_ihs_data_ms_sales[all_ihs_data_ms_sales["RtZ_group"]!="Unknown"]
        all_ihs_data_ms_sales["Period"] = periods[i]
        if i == 0:
            quaterly_ms_data_all_sales = all_ihs_data_ms_sales
        else:
            quaterly_ms_data_all_sales = quaterly_ms_data_all_sales.append(all_ihs_data_ms_sales)
        
    all_historic_data_ms_sales = all_historic_data_ms_sales[all_historic_data_ms_sales["fuel"].isin(["BEV","FCEV"])]
    all_historic_data_ms_sales = all_historic_data_ms_sales.groupby(["RtZ_group","Country","Year"]).sum().reset_index()
    all_historic_data_ms_sales.loc[all_historic_data_ms_sales["Country"]=="EU","Country"] = "Rest of EU-27"
    all_historic_data_ms_sales = all_historic_data_ms_sales[all_historic_data_ms_sales["RtZ_group"]!="Unknown"]
    all_historic_data_ms_sales = all_historic_data_ms_sales.rename(columns = {"Year":"Period"})
    quaterly_ms_data_all_sales = quaterly_ms_data_all_sales.append(all_historic_data_ms_sales)
    quaterly_ms_data_all_sales = quaterly_ms_data_all_sales.groupby(["Country","Period"]).sum().reset_index()
    
    
    sales_only = quaterly_ms_data_all_sales.groupby(["Period"]).sum().reset_index()
    sales_only = sales_only.rename(columns = {"Sales":"total_sales"})
    quaterly_ms_data_all_sales = quaterly_ms_data_all_sales.merge(sales_only, left_on = ["Period"], right_on = ["Period"], how = "left")
    
    quaterly_ms_data_all_sales["Share"] = quaterly_ms_data_all_sales["Sales"]/quaterly_ms_data_all_sales["total_sales"]
    quaterly_ms_data_all_sales = quaterly_ms_data_all_sales.drop(columns = ["total_sales"])
    # pdb.set_trace()
    MS_under_5pc = quaterly_ms_data_all_sales[(quaterly_ms_data_all_sales["Period"] == period) & (quaterly_ms_data_all_sales["Share"] <= 0.03)]["Country"]
    quaterly_ms_data_all_sales.loc[quaterly_ms_data_all_sales["Country"].isin(MS_under_5pc),"Country"] = "Rest of EU-27"
    quaterly_ms_data_all_sales = quaterly_ms_data_all_sales.groupby(["Country","Period"]).sum().reset_index()
    
    ms_order_list = (quaterly_ms_data_all_sales[(quaterly_ms_data_all_sales["Period"] == period) & (quaterly_ms_data_all_sales["Country"] != "Rest of EU-27")].sort_values("Share", ascending=False))
    ms_order_list = ms_order_list[["Country"]]
    ms_order_list.loc[len(ms_order_list)] = ["Rest of EU-27"]
    ms_order_list["order"] = range(0, len(ms_order_list))
    
    quaterly_ms_data_all_sales = quaterly_ms_data_all_sales.merge(ms_order_list, left_on = "Country", right_on = "Country", how = "left")
    
    quaterly_ms_data_all_sales["Period"] = quaterly_ms_data_all_sales["Period"].astype("str")
    quaterly_ms_data_all_sales = quaterly_ms_data_all_sales.sort_values(["Period","order"])
    
    # pdb.set_trace()
    # =============================================================================
    # sales by manufacturer      
    # =============================================================================
               
    conventional_fuels = ['ICE Diesel', 'ICE LNG', 'ICE Ethanol', 'ICE Gasoline', 'ICE LPG']
    zero_emissions_fuels = ['BEV', 'FCEV']
    
    ihs_data_oem_sales = ihs_data[["RtZ_group","fuel","Manufacturer",quarterly_sales_column]]
    ihs_data_oem_sales = ihs_data_oem_sales[ihs_data_oem_sales["RtZ_group"]!="Unknown"]
    # ihs_data_oem_sales.loc[ihs_data_oem_sales["Manufacturer"] == "Unspecified", "Manufacturer"] = "Other"
    ####################### Change Ale ###############
    ihs_data_oem_sales.loc[ihs_data_oem_sales['Manufacturer'].str.lower().isin(['unspecified', 'other']), 'Manufacturer'] = 'Other'
    #######################
    
    zev_ihs_data_oem_sales = ihs_data_oem_sales[ihs_data_oem_sales["fuel"].isin(zero_emissions_fuels)]
    ice_ihs_data_oem_sales = ihs_data_oem_sales[ihs_data_oem_sales["fuel"].isin(conventional_fuels)]
    
    zev_ihs_data_oem_sales = zev_ihs_data_oem_sales.groupby(["RtZ_group","fuel","Manufacturer"]).sum().reset_index()
    ice_ihs_data_oem_sales = ice_ihs_data_oem_sales.groupby(["RtZ_group","fuel","Manufacturer"]).sum().reset_index()
    # pdb.set_trace()
    for i, veh_group in enumerate(list(ice_ihs_data_oem_sales["RtZ_group"].unique())):
        zev_ihs_data_oem_sales_mini = zev_ihs_data_oem_sales[zev_ihs_data_oem_sales["RtZ_group"] == veh_group].copy()
        if veh_group == 'Buses and coaches':
            top_oems = zev_ihs_data_oem_sales_mini.sort_values(by=[quarterly_sales_column], ascending = False).head(9)["Manufacturer"].unique() #8
        else:
            top_oems = zev_ihs_data_oem_sales_mini.sort_values(by=[quarterly_sales_column], ascending = False).head(8)["Manufacturer"].unique() #8
    
        # pdb.set_trace()
        zev_ihs_data_oem_sales_mini.loc[~zev_ihs_data_oem_sales_mini["Manufacturer"].isin(top_oems),"Manufacturer"] = "Other"
        zev_ihs_data_oem_sales_mini = zev_ihs_data_oem_sales_mini.groupby(["RtZ_group","Manufacturer"]).sum().reset_index()
        zev_ihs_data_oem_sales_mini = zev_ihs_data_oem_sales_mini.sort_values(by=[quarterly_sales_column], ascending = False)
        zev_ihs_data_oem_sales_mini = zev_ihs_data_oem_sales_mini.rename(columns = {quarterly_sales_column:"zev_sales"})
        
        ice_ihs_data_oem_sales_mini = ice_ihs_data_oem_sales[ice_ihs_data_oem_sales["RtZ_group"] == veh_group].copy()
        ice_ihs_data_oem_sales_mini.loc[~ice_ihs_data_oem_sales_mini["Manufacturer"].isin(top_oems),"Manufacturer"] = "Other"
        ice_ihs_data_oem_sales_mini = ice_ihs_data_oem_sales_mini.groupby(["RtZ_group","Manufacturer"]).sum().reset_index()
        ice_ihs_data_oem_sales_mini = ice_ihs_data_oem_sales_mini.rename(columns = {quarterly_sales_column:"ice_sales"})
        zev_ihs_data_oem_sales_mini = zev_ihs_data_oem_sales_mini.merge(ice_ihs_data_oem_sales_mini, left_on = ["RtZ_group","Manufacturer"], right_on = ["RtZ_group","Manufacturer"], how = "left")
        zev_ihs_data_oem_sales_mini = zev_ihs_data_oem_sales_mini.fillna(0)
        if i == 0:
            master_data_oem = zev_ihs_data_oem_sales_mini
        else:
            master_data_oem = master_data_oem.append(zev_ihs_data_oem_sales_mini)
    
    master_data_oem = master_data_oem.merge(master_data_oem.groupby(["RtZ_group"]).sum().reset_index(), left_on = ["RtZ_group"], right_on = ["RtZ_group"], how = "left") 
    master_data_oem["ice_shares"] = master_data_oem["ice_sales_x"]/master_data_oem["ice_sales_y"]
    master_data_oem["zev_shares"] = master_data_oem["zev_sales_x"]/master_data_oem["zev_sales_y"]
    
    master_data_oem = master_data_oem[["RtZ_group","Manufacturer","ice_shares","zev_shares"]]
    
    ice_df = master_data_oem[["RtZ_group","Manufacturer","ice_shares"]].rename(columns = {"ice_shares":"shares"})
    ice_df["pt"]="ICE"
    zev_df = master_data_oem[["RtZ_group","Manufacturer","zev_shares"]].rename(columns = {"zev_shares":"shares"})
    zev_df["pt"]="ZEV"
    master_data_oem = ice_df.append(zev_df)
    
    # =============================================================================
    # Unique models
    # =============================================================================
    # pdb.set_trace()
    def get_closest_match(x, list_models, threshold=80):
        best_match = process.extractOne(x, list_models, score_cutoff=threshold)
        return best_match[0] if best_match else None
    
    zev_models = ihs_data[["Axle configuration","RtZ_group","fuel","Model",quarterly_sales_column]].groupby(["Axle configuration","RtZ_group","fuel","Model"]).sum().reset_index()
    zev_models = zev_models[zev_models["fuel"].isin(["BEV","FCEV"])]
    zev_models = zev_models[(zev_models["RtZ_group"]!="Buses and coaches") & (zev_models["fuel"]=="BEV") & (zev_models[quarterly_sales_column]!=0) & ~((zev_models["Model"].str.contains("Unspec")) | (zev_models["Model"].str.contains("unspec")) | (zev_models["Model"].str.contains("Other")) | (zev_models["Model"].str.contains("other")))]
    
    # pdb.set_trace()
    list_models = list_of_zev_models['Model'].unique()
    
    zev_models['matched_model'] = zev_models['Model'].apply(lambda x: get_closest_match(x, list_models))
    
    # Merge the dataframes
    merged_df = pd.merge(zev_models, list_of_zev_models, left_on=['Axle configuration','matched_model','RtZ_group'], right_on=['Axle configuration','Model','RtZ_group'], how='left')
    
    zev_models = merged_df[['Axle configuration', 'RtZ_group', 'Model_x', 'matched_model','fuel', 'Q1_2025',
                          'Max battery capacity (kWh)', 'Battery range (kWh)', 'Chemistry']].copy()
    
    zev_models.rename(columns={ quarterly_sales_column:"Sales",
                                'RtZ_group_x': 'RtZ_group', 
                                'Model_x': 'Model'}, inplace=True)
    
    # =============================================================================
    # City buses by MS
    # =============================================================================
    
    city_buses = ihs_data[ihs_data["bus_type"] == "City bus"][["Country", "fuel", quarterly_sales_column]].copy()
    city_buses = city_buses.groupby(["Country", "fuel"]).sum().reset_index()
    
    ############################ Change ###########################################
    required_fuels = ['BEV', 'FCEV']
    
    # Trova le nazioni uniche presenti nel DataFrame
    unique_countries = city_buses['Country'].unique()
    # pdb.set_trace()
    # Per ogni combinazione di nazione e tipo di carburante richiesto, verifica se esiste già
    for country in unique_countries:
        for fuel in required_fuels:
            if not ((city_buses['Country'] == country) & (city_buses['fuel'] == fuel)).any():
                # Se una combinazione di Country e Fuel è mancante, aggiungi una riga con vendite zero
                new_row = {'Country': country, 'fuel': fuel, quarterly_sales_column: 0}
                city_buses = city_buses.append(new_row, ignore_index=True)
    
    ############################ Change ###########################################
    
    EU_city_buses = city_buses.groupby(["fuel"]).sum().reset_index()[["fuel",quarterly_sales_column]]
    EU_city_buses["Country"] = "EU-27"
    city_buses = city_buses.append(EU_city_buses)
    city_buses = city_buses.merge(city_buses.groupby(["Country"]).sum().reset_index(), left_on = "Country", right_on = "Country", how = "left")
    city_buses["shares"] = city_buses[quarterly_sales_column + "_x"]/city_buses[quarterly_sales_column + "_y"]
    city_buses["sales"] = city_buses[quarterly_sales_column + "_x"]
    city_buses = city_buses[["Country","fuel","shares","sales"]]
    
    # =============================================================================
    # City buses by powertrain
    # =============================================================================
    
    city_buses_pt_historic = city_buses_pt.copy()
    city_buses_pt_historic.loc[city_buses_pt_historic["fuel_type"].isin(["Diesel","Hybrid"]), "fuel_type"] = "Diesel incl. hybrid"
    city_buses_pt_historic = city_buses_pt_historic.groupby(["fuel_type","year_index", "year", "quarter"]).sum().reset_index()
    city_buses_pt_historic.loc[city_buses_pt_historic["fuel_type"] == "Electric", "fuel_type"] = "Battery Electric"
    city_buses_pt_historic.loc[city_buses_pt_historic["fuel_type"] == "Hydrogen", "fuel_type"] = "Hydrogen Fuel Cell"
    
    if city_buses_pt_historic["year_index"].str.contains(year+"_"+quarter).sum()>0:
        print("city_bus_pt_share.csv already has latest quarter available")
    else:
        city_buses_pt_quarter = ihs_data[ihs_data["bus_type"] == "City bus"][["Country", "fuel", quarterly_sales_column]].copy()
        city_buses_pt_quarter.loc[city_buses_pt_quarter["fuel"] == "BEV", "fuel"] = "Battery Electric"
        city_buses_pt_quarter.loc[city_buses_pt_quarter["fuel"] == "FCEV", "fuel"] = "Hydrogen Fuel Cell"
        city_buses_pt_quarter.loc[city_buses_pt_quarter["fuel"] == "ICE Diesel", "fuel"] = "Diesel incl. hybrid"
        city_buses_pt_quarter.loc[city_buses_pt_quarter["fuel"] == "ICE Gasoline", "fuel"] = "Diesel incl. hybrid"
        city_buses_pt_quarter.loc[city_buses_pt_quarter["fuel"] == "ICE LNG", "fuel"] = "Natural Gas"
        city_buses_pt_quarter = city_buses_pt_quarter.groupby(["fuel"]).sum().reset_index()
        
        ############# Modifications Alessia#############
        # Check and add missing fuel types for the current quarter
        required_fuel_types = ['Battery Electric', 'Hydrogen Fuel Cell']
        for fuel_type in required_fuel_types:
            if fuel_type not in city_buses_pt_quarter['fuel'].values:
                # Create a new row with all zeros for the missing fuel type
                new_row = {'fuel': fuel_type, quarterly_sales_column: 0}
                # Append the new row to the DataFrame
                city_buses_pt_quarter = city_buses_pt_quarter.append(new_row, ignore_index=True)
                
    #############
    
        # pdb.set_trace()
        city_buses_pt_quarter["year_index"] = year + "_" + quarter
        city_buses_pt_quarter["year"] = year
        city_buses_pt_quarter["quarter"] = quarter    
        city_buses_pt_quarter = city_buses_pt_quarter.rename(columns = {quarter + "_" + year:"sales", "fuel":"fuel_type"})
        city_buses_pt_quarter["Share"] = city_buses_pt_quarter["sales"]/city_buses_pt_quarter["sales"].sum()
        city_buses_pt_quarter = city_buses_pt_quarter[city_buses_pt_quarter["fuel_type"].isin(city_buses_pt_historic["fuel_type"].unique())]
        city_buses_pt_historic = city_buses_pt_historic.append(city_buses_pt_quarter)
    city_buses_pt_historic.to_csv(RtZ_folder_location + "/outputs/city_bus_pt_share_" + quarter + "_" + year + ".csv", index = False)
        
    
    
    # =============================================================================
    # sales by all member states - Full Market 
    # =============================================================================
    # historic_ihs_data['RtZ_group'] = historic_ihs_data['RtZ_group'].fillna('unspec')
    # pdb.set_trace()
    
    previous_year_quarterly_data = previous_year_quarterly.copy()
    if quarter == "Q1":
        grouped_quarter = "Q1"
    else:
        grouped_quarter = "Q1-" + quarter    
    prev_yr_grouped_quarter = str(int(year)-1) + " " + grouped_quarter
    curr_year_grouped_quarter = year + " " + grouped_quarter
    
    # Similar classification for historic IHS data
    truck_types = {
    "Aerial Platform Vehicle", "Armoured Transporter", "Box / Cube with Tailgate", "Box Van",
    "Car Transporter", "Chassis", "Commercial Vehicle", "Concrete Mixer", "Container Transporter",
    "Crane", "Cube Truck", "Dangerous Goods Transporter", "Dropside", "Dropside with Tarp",
    "Dump Vehicle", "Flatbed", "Flatbed with Crane", "HCV Tractor Truck", "Isothermic Vehicle",
    "Live Animal Transporter", "Pick Up", "Recovery Vehicle", "Special Duty Vehicle",
    "Street Sweeper", "Swap-Body Vehicle", "Tanker Vehicle", "Tipper", "Van",
    "Waste-handling Vehicle", "Workshop Vehicle"
    }
    
    bus_types = {
        "Bus", "Wheelchair Access Vehicle"
    }
    
    other_types = {
        "Ambulance", "Car Derived Utility", "Civil Defence", "Fire Service Vehicle", "Hatchback",
        "Mobile Home", "Mobile Shop", "Passenger Vehicle", "Police Vehicle",
        "Standard Station Wagon", "Unknown"
    }
    
    previous_year_quarterly_data["Body group"] = "na"
    previous_year_quarterly_data.loc[previous_year_quarterly_data["Body type"].isin(truck_types),"Body group"] = "Truck"
    previous_year_quarterly_data.loc[previous_year_quarterly_data["Body type"].isin(bus_types),"Body group"] = "Bus"
    previous_year_quarterly_data.loc[previous_year_quarterly_data["Body type"].isin(other_types),"Body group"] = "Other"

    previous_year_quarterly_data.loc[(previous_year_quarterly_data["Body group"] == "Bus"),"RtZ_group"] = "Buses and coaches"
    previous_year_quarterly_data.loc[(previous_year_quarterly_data["Body group"] != "Bus") & (previous_year_quarterly_data["Body group"] != "Other") & (previous_year_quarterly_data["Gross vehicle weight"] >= 12000),"RtZ_group"] = "Heavy trucks"
    previous_year_quarterly_data.loc[(previous_year_quarterly_data["Body group"] != "Bus") & (previous_year_quarterly_data["Body group"] != "Other") & (previous_year_quarterly_data["Gross vehicle weight"] < 12000) & (previous_year_quarterly_data["Gross vehicle weight"] >= 0),"RtZ_group"] = "Light and medium trucks"
    # Merging fuel mapping data with IHS data
    previous_year_quarterly_data = previous_year_quarterly_data.merge(fuel_map,left_on = ["Fuel type"], right_on = ["Fuel type"], how = "left")
    previous_year_quarterly_data.loc[previous_year_quarterly_data["Manufacturer"]=="Karsan","RtZ_group"] = "Buses and coaches"
    
    previous_year_all_veh = previous_year_quarterly_data[["Country",'Q1_2024','Q2_2024','Q3_2024','Q4_2024']].groupby(["Country"]).sum().reset_index().melt(id_vars=['Country'],var_name='Period',value_name='Sales')
    current_year_all_veh = ihs_data[["Country"] + ["Q" + str(s) + "_" + year for s in range(1,int(quarter[1])+1)]].groupby(["Country"]).sum().reset_index().melt(id_vars=['Country'],var_name='Period',value_name='Sales')
    prev_and_curr_all_veh = previous_year_all_veh.append(current_year_all_veh)
    
    tc_check = current_year_all_veh.copy()
    i=0
    while i == 0:
        curr_top_countries = tc_check[tc_check["Period"] == quarter+"_"+year].nlargest(6, "Sales")["Country"].tolist()
        prev_countries = previous_year_all_veh["Country"].unique().tolist()
        not_in_list = [item for item in curr_top_countries if item not in prev_countries]
        if len(not_in_list) == 0:
            i = i+1
            order_countries = curr_top_countries + ["Rest of EU"]
            order_df = df = pd.DataFrame({
                                        "Country": order_countries,
                                        "Order": [i + 1 for i in range(len(order_countries))]
                                    })
        else:
            tc_check = tc_check[~tc_check["Country"].isin(not_in_list)]
    
    prev_and_curr_all_veh["Country_agg"] = "Rest of EU"
    prev_and_curr_all_veh.loc[prev_and_curr_all_veh["Country"].isin(curr_top_countries),"Country_agg"] = prev_and_curr_all_veh.loc[prev_and_curr_all_veh["Country"].isin(curr_top_countries),"Country"]
    
    prev_and_curr_all_veh = prev_and_curr_all_veh[prev_and_curr_all_veh["Period"].isin(["Q" + str(s) + "_" + year for s in range(1,int(quarter[1])+1)] + ["Q" + str(s) + "_" + str(int(year)-1) for s in range(1,int(quarter[1])+1)])]

    prev_and_curr_all_veh["Period_agg"] = grouped_quarter
    prev_and_curr_all_veh["Year"] = prev_and_curr_all_veh["Period"].str.extract(r'_(\d{4})')
    prev_and_curr_all_veh["Period_agg"] = prev_and_curr_all_veh["Year"] + " " + prev_and_curr_all_veh["Period_agg"]
    
    prev_and_curr_all_veh = prev_and_curr_all_veh[["Country_agg","Period_agg","Sales"]].groupby(["Country_agg","Period_agg"]).sum().reset_index()
    prev_and_curr_all_veh = prev_and_curr_all_veh.merge(order_df, left_on = ["Country_agg"], right_on = ["Country"])
    prev_and_curr_all_veh = prev_and_curr_all_veh.sort_values(by="Order")[["Country","Period_agg","Sales"]]
    prev_and_curr_all_veh = prev_and_curr_all_veh.pivot(index="Country", columns="Period_agg", values="Sales")
    prev_and_curr_all_veh = prev_and_curr_all_veh.loc[df["Country"].drop_duplicates().values]
    prev_and_curr_all_veh[prev_yr_grouped_quarter + " share"] = prev_and_curr_all_veh[prev_yr_grouped_quarter]/prev_and_curr_all_veh[prev_yr_grouped_quarter].sum()
    prev_and_curr_all_veh[curr_year_grouped_quarter + " share"] = prev_and_curr_all_veh[curr_year_grouped_quarter]/prev_and_curr_all_veh[curr_year_grouped_quarter].sum()
    prev_and_curr_all_veh = prev_and_curr_all_veh.reset_index()

    # =============================================================================
    # sales by all member states - ZEV Market 
    # =============================================================================
    # historic_ihs_data['RtZ_group'] = historic_ihs_data['RtZ_group'].fillna('unspec')
    # pdb.set_trace()
    
        
    zev_previous_year_quarterly_data = previous_year_quarterly.copy()
    if quarter == "Q1":
        grouped_quarter = "Q1"
    else:
        grouped_quarter = "Q1-" + quarter    
    prev_yr_grouped_quarter = str(int(year)-1) + " " + grouped_quarter
    curr_year_grouped_quarter = year + " " + grouped_quarter
    
    # Similar classification for historic IHS data
    zev_previous_year_quarterly_data["Body group"] = "na"
    zev_previous_year_quarterly_data.loc[zev_previous_year_quarterly_data["Body type"].isin(truck_types),"Body group"] = "Truck"
    zev_previous_year_quarterly_data.loc[zev_previous_year_quarterly_data["Body type"].isin(bus_types),"Body group"] = "Bus"
    zev_previous_year_quarterly_data.loc[zev_previous_year_quarterly_data["Body type"].isin(other_types),"Body group"] = "Other"
    zev_previous_year_quarterly_data.loc[(zev_previous_year_quarterly_data["Body group"] == "Bus"),"RtZ_group"] = "Buses and coaches"
    zev_previous_year_quarterly_data.loc[(zev_previous_year_quarterly_data["Body group"] != "Bus") & (zev_previous_year_quarterly_data["Body group"] != "Unknown") & (zev_previous_year_quarterly_data["Gross vehicle weight"] >= 12000),"RtZ_group"] = "Heavy trucks"
    zev_previous_year_quarterly_data.loc[(zev_previous_year_quarterly_data["Body group"] != "Bus") & (zev_previous_year_quarterly_data["Body group"] != "Unknown") & (zev_previous_year_quarterly_data["Gross vehicle weight"] < 12000) & (zev_previous_year_quarterly_data["Gross vehicle weight"] >= 0),"RtZ_group"] = "Light and medium trucks"
    zev_previous_year_quarterly_data["ZEV_ICE"] = "ICE"
    zev_previous_year_quarterly_data.loc[zev_previous_year_quarterly_data['Fuel type'].isin(['Electric w/oREX','Fuel cell']),"ZEV_ICE"] = "ZEV"
    zev_previous_year_quarterly_data.loc[zev_previous_year_quarterly_data["Manufacturer"]=="Karsan","RtZ_group"] = "Buses and coaches"
    
    zev_previous_year_all_veh = zev_previous_year_quarterly_data[["Country","RtZ_group","ZEV_ICE",'Q1_2024','Q2_2024','Q3_2024','Q4_2024']].groupby(["Country","RtZ_group","ZEV_ICE"]).sum().reset_index().melt(id_vars=['Country','RtZ_group','ZEV_ICE'],var_name='Period',value_name='Sales')
    
    zev_current_year_all_veh = ihs_data.copy()
    zev_current_year_all_veh["ZEV_ICE"] = "ICE"
    zev_current_year_all_veh.loc[zev_current_year_all_veh["fuel"].isin(["BEV","FCEV"]),"ZEV_ICE"] = "ZEV"
    zev_current_year_all_veh = zev_current_year_all_veh[["Country","RtZ_group","ZEV_ICE"] + ["Q" + str(s) + "_" + year for s in range(1,int(quarter[1])+1)]].groupby(["Country","RtZ_group","ZEV_ICE"]).sum().reset_index().melt(id_vars=['Country','RtZ_group','ZEV_ICE'],var_name='Period',value_name='Sales')
    zev_prev_and_curr_all_veh = zev_previous_year_all_veh.append(zev_current_year_all_veh)
    
    tc_check = zev_current_year_all_veh[zev_current_year_all_veh["ZEV_ICE"]=="ZEV"].copy()
    # i=0
    # while i == 0:
    #     curr_top_countries = tc_check[tc_check["Period"] == quarter+"_"+year].groupby(["Country"]).sum().reset_index().nlargest(10, "Sales")["Country"].tolist()
    #     prev_countries = zev_previous_year_all_veh["Country"].unique().tolist()
    #     not_in_list = [item for item in curr_top_countries if item not in prev_countries]
    #     if len(not_in_list) == 0:
    #         i = i+1
    #         order_countries = curr_top_countries + ["Rest of EU"]
    #         order_df = df = pd.DataFrame({
    #                                     "Country": order_countries,
    #                                     "Order": [i + 1 for i in range(len(order_countries))]
    #                                 })
    #     else:
    #         tc_check = tc_check[~tc_check["Country"].isin(not_in_list)]
    
    # zev_prev_and_curr_all_veh["Country_agg"] = "Rest of EU"
    # zev_prev_and_curr_all_veh.loc[zev_prev_and_curr_all_veh["Country"].isin(curr_top_countries),"Country_agg"] = zev_prev_and_curr_all_veh.loc[zev_prev_and_curr_all_veh["Country"].isin(curr_top_countries),"Country"]
    zev_prev_and_curr_all_veh = zev_prev_and_curr_all_veh.groupby(["RtZ_group","ZEV_ICE","Period","Country"]).sum().reset_index()
    # if quarter == "Q1":
    #     zev_prev_and_curr_all_veh = zev_prev_and_curr_all_veh[zev_prev_and_curr_all_veh["Period"].isin([quarter + "_" + year,quarter + "_" + str(int(year)-1),"Q4" + "_" + str(int(year)-1)])]
    # else:
    #     zev_prev_and_curr_all_veh = zev_prev_and_curr_all_veh[zev_prev_and_curr_all_veh["Period"].isin([quarter + "_" + year,quarter + "_" + str(int(year)-1),"Q" + str(int(quarter[1])-1) + "_" + year])]
    zev_prev_and_curr_all_veh = zev_prev_and_curr_all_veh.pivot(index=["Country","RtZ_group","ZEV_ICE"], columns="Period", values="Sales").reset_index()

    
    # =============================================================================
    # Sales by weight - Full Market 
    # =============================================================================
    
    previous_year_OEMs = previous_year_quarterly_data.copy()
    previous_year_OEMs.loc[previous_year_OEMs["RtZ_group"] == "Buses and coaches", "oem_veh"] = "Buses and coaches"
    previous_year_OEMs.loc[previous_year_OEMs["RtZ_group"] == "Light and medium trucks", "oem_veh"] = "Light and medium trucks"
    previous_year_OEMs.loc[(previous_year_OEMs["RtZ_group"] == "Heavy trucks") & (previous_year_OEMs["Body type"].str.contains("Tractor")) & ~(previous_year_OEMs["Body type"].str.contains("Unknown")), "oem_veh"] = "Heavy trucks - Tractor"
    previous_year_OEMs.loc[(previous_year_OEMs["RtZ_group"] == "Heavy trucks") & ~(previous_year_OEMs["Body type"].str.contains("Tractor")) & ~(previous_year_OEMs["Body type"].str.contains("Unknown")), "oem_veh"] = "Heavy trucks - Rigid"
    previous_year_OEMs.loc[previous_year_OEMs["Manufacturer"] == "Renault Trucks","Manufacturer"] = "Renault"
    previous_year_OEMs.loc[previous_year_OEMs["Manufacturer"] == "Volvo Trucks","Manufacturer"] = "Volvo"
    previous_year_OEMs.loc[previous_year_OEMs["Manufacturer"] == "Volvo Bus","Manufacturer"] = "Volvo"
    previous_year_OEMs.loc[previous_year_OEMs["Manufacturer"] == "Iveco Bus","Manufacturer"] = "Iveco"

    previous_year_OEMs["man_agg"]="Others"
    previous_year_OEMs.loc[previous_year_OEMs["Manufacturer"].isin(["Mercedes","Iveco","Renault","MAN","DAF","Renault","Scania","Volvo"]), "man_agg"] = previous_year_OEMs["Manufacturer"]
    previous_year_OEMs = previous_year_OEMs[["man_agg",'oem_veh','Q1_2024','Q2_2024','Q3_2024','Q4_2024']].groupby(["man_agg","oem_veh"]).sum().reset_index().melt(id_vars=['man_agg','oem_veh'],var_name='Period',value_name='Sales')
    
    current_year_all_OEMs = ihs_data.copy()
    current_year_all_OEMs.loc[current_year_all_OEMs["RtZ_group"] == "Buses and coaches", "oem_veh"] = "Buses and coaches"
    current_year_all_OEMs.loc[current_year_all_OEMs["RtZ_group"] == "Light and medium trucks", "oem_veh"] = "Light and medium trucks"
    current_year_all_OEMs.loc[(current_year_all_OEMs["RtZ_group"] == "Heavy trucks") & (current_year_all_OEMs["Body type"].str.contains("Tractor")) & ~(current_year_all_OEMs["Body type"].str.contains("Unknown")), "oem_veh"] = "Heavy trucks - Tractor"
    current_year_all_OEMs.loc[(current_year_all_OEMs["RtZ_group"] == "Heavy trucks") & ~(current_year_all_OEMs["Body type"].str.contains("Tractor")) & ~(current_year_all_OEMs["Body type"].str.contains("Unknown")), "oem_veh"] = "Heavy trucks - Rigid"
    current_year_all_OEMs.loc[current_year_all_OEMs["Manufacturer"] == "Renault Trucks","Manufacturer"] = "Renault"
    current_year_all_OEMs.loc[current_year_all_OEMs["Manufacturer"] == "Volvo Trucks","Manufacturer"] = "Volvo"
    current_year_all_OEMs.loc[current_year_all_OEMs["Manufacturer"] == "Volvo Bus","Manufacturer"] = "Volvo"
    current_year_all_OEMs.loc[current_year_all_OEMs["Manufacturer"] == "Iveco Bus","Manufacturer"] = "Iveco"
    current_year_all_OEMs["man_agg"]="Others"
    current_year_all_OEMs.loc[current_year_all_OEMs["Manufacturer"].isin(["Mercedes","Iveco","Renault","MAN","DAF","Renault","Scania","Volvo"]), "man_agg"] = current_year_all_OEMs["Manufacturer"]
    current_year_all_OEMs = current_year_all_OEMs[["man_agg", "oem_veh"] + ["Q" + str(s) + "_" + year for s in range(1,int(quarter[1])+1)]].groupby(["man_agg", "oem_veh"]).sum().reset_index().melt(id_vars=['man_agg','oem_veh'],var_name='Period',value_name='Sales')
    
    prev_and_curr_all_OEMs = previous_year_OEMs.append(current_year_all_OEMs)
    
    prev_and_curr_all_OEMs = prev_and_curr_all_OEMs[prev_and_curr_all_OEMs["Period"].isin(["Q" + str(s) + "_" + year for s in range(1,int(quarter[1])+1)] + ["Q" + str(s) + "_" + str(int(year)-1) for s in range(1,int(quarter[1])+1)])]
    if quarter == "Q1":
        prev_and_curr_all_OEMs["Period_agg"] = "Q1"
    else:
        prev_and_curr_all_OEMs["Period_agg"] = "Q1-" + quarter
    prev_and_curr_all_OEMs["Year"] = prev_and_curr_all_OEMs["Period"].str.extract(r'_(\d{4})')
    prev_and_curr_all_OEMs["Period_agg"] = prev_and_curr_all_OEMs["Year"] + " " + prev_and_curr_all_OEMs["Period_agg"]
    
    prev_and_curr_all_OEMs = prev_and_curr_all_OEMs[["man_agg","oem_veh","Period_agg","Sales"]].groupby(["man_agg","oem_veh","Period_agg"]).sum().reset_index()
    
    if quarter == "Q1":
        curr_all_OEMs = prev_and_curr_all_OEMs[prev_and_curr_all_OEMs["Period_agg"] == year + " Q1"].copy()
    else:
        curr_all_OEMs = prev_and_curr_all_OEMs[prev_and_curr_all_OEMs["Period_agg"] == year + " Q1-" + quarter].copy()        
    
    # =============================================================================
    # Saving data as xls
    # =============================================================================
    
    list_dfs = [ihs_data_shares, quaterly_data_ft, master_data_ms, master_data_oem, zev_models, veh_types, quaterly_ms_data_all_sales, city_buses, prev_and_curr_all_veh, prev_and_curr_all_OEMs, curr_all_OEMs,zev_prev_and_curr_all_veh]
    sheet_names = ["pt_shares_by_group","sales_vol_by_group","sales_vol_by_ms","sales_share_by_oem","list_of_zev_models","sales_by_grouped_type","historic_sales_by_ms", "city_bus_shares", "all", "all_weight_previous_quarters", "all_weight","zevs_all_MS"]
    
    def save_xls(list_dfs, xls_path):
        with ExcelWriter(xls_path) as writer:
            for n, df in enumerate(list_dfs):
                df.to_excel(writer,sheet_names[n])
                
    save_xls(list_dfs, xls_path)
                          
    ############################################
    
    
    
    combined_ihs_data = ihs_data_sales_type.copy()    
    # combined_ihs_data["veh_type_short"] = "Other"    
    # combined_ihs_data.loc[(combined_ihs_data["RtZ_group"]=="Heavy trucks") & ~(combined_ihs_data["Body type"] == "HCV Tractor Truck"), "veh_type_short"] = "rigid truck"
    # combined_ihs_data.loc[(combined_ihs_data["RtZ_group"]=="Heavy trucks") & (combined_ihs_data["Body type"] == "HCV Tractor Truck"), "veh_type_short"] = "tractor trailer"
    
    
    
    # combined_ihs_data.loc[(combined_ihs_data["RtZ_group"] == "Light and medium trucks") & (combined_ihs_data["Body type"].str.contains("Van")), "veh_type_short"] = "van"
    # combined_ihs_data.loc[(combined_ihs_data["RtZ_group"] == "Light and medium trucks") & ~(combined_ihs_data["Body type"].str.contains("Van")), "veh_type_short"] = "truck"
    # combined_ihs_data.loc[(combined_ihs_data["RtZ_group"] == "Light and medium trucks") & (combined_ihs_data["Body type"].str.contains("Van")), "veh_type_short"] = "van"
    # combined_ihs_data.loc[(combined_ihs_data["RtZ_group"] == "Light and medium trucks") & ~(combined_ihs_data["Body type"].str.contains("Van")), "veh_type_short"] = "truck"
    
            
    combined_ihs_data.to_csv(RtZ_folder_location + "/outputs/2025_Q1_full_data.csv", index = False) 
            
 #pippo_spainAcea
 
 
 
 
 