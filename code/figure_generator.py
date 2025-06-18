import pandas as pd
import numpy as np
import squarify
import math
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import PercentFormatter
from matplotlib.lines import Line2D
from matplotlib import font_manager
import matplotlib.patches as patches
import os
import pdb

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import pandas as pd
plt.rcParams['pdf.fonttype'] = 42

# =============================================================================
# Input data
# =============================================================================

RtZ_folder_location = r"/Users/e.mulholland/Documents/Work 2025/EU/RtZ/Q1/RtZ_formatter_folder2025"
current_quarter = "2025 Q1"
bus_colour_col = "#632A7A"
heavy_col = "#9271A0"
light_med_col = "#BFACC8"

# =============================================================================
# summary page inputs
# =============================================================================

#summary figure inputs
fig_0_earliest_year = 2017 #summary figure; earliest year shown
fig_0_sale_vol_intervals = 3000 #summary figure; sales volume intervals
fig_0_sale_share_intervals = 0.05 #summary figure; sales share intervals
fig_0_max_y_axis_val = 15100
max_y_axis2_val = 0.25

# =============================================================================
# heavy trucks inputs
# =============================================================================

fig_1_2_earliest_year = 2019 #historic sales by powertrain; earliest year shown
fig_1_2_max_vol = 3500 #historic sales by powertrain; max sales volume value shown
fig_1_2_ax_y_tick_intervals = 500 #historic sales by powertrain; interval for sales volume
fig_1_2_max_share = 0.0175 #historic sales by powertrain; max sales share value shown
fig_1_2_ax2_y_tick_intervals = 0.0025 #historic sales by powertrain; interval for sales share

fig_1_4_ax_y_tick_intervals = 10 #sales by battery size; interval for sales volume

fig_1_6_max_val = 0.5 #sales by OEM; max sales volume shown
fig_1_6_interval = 0.1 #sales by OEM; interval between sales volume

# =============================================================================
# light and medium trucks input
# =============================================================================

fig_2_2_earliest_year = 2019 #historic sales by powertrain; earliest year shown
fig_2_2_max_vol = 5000 #historic sales by powertrain; max sales volume value shown
fig_2_2_ax_y_tick_intervals = 1000 #historic sales by powertrain; interval for sales volume
fig_2_2_max_share = 0.25 #historic sales by powertrain; max sales share value shown
fig_2_2_ax2_y_tick_intervals = 0.05 #historic sales by powertrain; interval for sales share

fig_2_4_ax_y_tick_intervals = 100 #sales by battery size; interval for sales volume

fig_2_6_max_val = 0.7 #sales by OEM; max sales volume shown
fig_2_6_interval = 0.1 #sales by OEM; interval between sales volume

# =============================================================================
# buses input
# =============================================================================

fig_3_2_earliest_year = 2019 #historic sales by powertrain; earliest year shown
fig_3_2_max_vol = 7500 #historic sales by powertrain; max sales volume value shown
fig_3_2_ax_y_tick_intervals = 1500 #historic sales by powertrain; interval for sales volume
fig_3_2_max_share = 0.25 #historic sales by powertrain; max sales share value shown
fig_3_2_ax2_y_tick_intervals = 0.05 #historic sales by powertrain; interval for sales share

fig_3_3_ax_y_tick_intervals = 0.15 #historic sales of city buses by powertrain; interval for sales shares

fig_3_6_max_val = 0.7 #sales by OEM; max sales volume shown
fig_3_6_interval = 0.1 #sales by OEM; interval between sales volume

# =============================================================================
# Master file
# =============================================================================

xls = RtZ_folder_location + "/outputs/Dataforce_Q1_2025_formatted_data.xlsx"
xls_Q = RtZ_folder_location + "/outputs/Q1_2024_formatted_data.xlsx"
figures_folder = RtZ_folder_location + "/figures/"

# =============================================================================
# Fonts
# =============================================================================

gotham_book_font_path = os.path.join(RtZ_folder_location, "fonts", "GothamBook.otf")

# gotham_book_font_path = RtZ_folder_location + "/fonts/GothamBook.otf"
gotham_book_font = font_manager.FontProperties(fname=gotham_book_font_path)
gotham_medium_font_path = os.path.join(RtZ_folder_location, "fonts", "GothamMedium.otf")
# gotham_medium_font_path = RtZ_folder_location + "/fonts/GothamMedium.otf"
gotham_medium_font = font_manager.FontProperties(fname=gotham_medium_font_path)

gotham_bold_font_path = os.path.join(RtZ_folder_location, "fonts", "Gotham-Bold.otf")
# gotham_bold_font_path = RtZ_folder_location + "/fonts/Gotham-Bold.otf"
gotham_bold_font = font_manager.FontProperties(fname=gotham_bold_font_path)

# Create a function to set font properties for the specified text element
def set_font_properties(element, font, size, colour):
    element.set_fontproperties(font)
    element.set_fontsize(size)
    element.set_color(colour)
   
# =============================================================================
# Import data
# =============================================================================

pt_shares_by_group = pd.read_excel(xls, "pt_shares_by_group")
sales_vol_by_group = pd.read_excel(xls, "sales_vol_by_group")
sales_vol_by_ms = pd.read_excel(xls, "sales_vol_by_ms")
sales_share_by_oem = pd.read_excel(xls, "sales_share_by_oem")
list_of_zev_models = pd.read_excel(xls, "list_of_zev_models")
sales_by_grouped_type = pd.read_excel(xls, "sales_by_grouped_type")
historic_sales_by_ms = pd.read_excel(xls, "historic_sales_by_ms")
city_bus_shares_by_ms = pd.read_excel(xls, "city_bus_shares")
city_bus_shares_by_pt = pd.read_csv(RtZ_folder_location + "/outputs/city_bus_pt_share_Q1_2025_EV_FC_combined.csv")
total_market_share_ms = pd.read_excel(xls, "all")
# city_bus_shares_by_pt_Chatrou_only = pd.read_excel(RtZ_folder_location + "/outputs/Chatrou_Q1_2024.xlsx", sheet_name="IHS_storical_value")

q_2024_data_tmp = pd.read_excel(xls_Q, "sales_vol_by_group")
q_2024_data = q_2024_data_tmp[q_2024_data_tmp['Period'].isin(['2024 Q1', '2024 Q2', '2024 Q3', '2024 Q4'])]

quaterly_ms_data_all_sales = pd.read_excel(xls, "all")

quaterly_weight_data_all_sales = pd.read_excel(xls, "all_weight")

# =============================================================================
# Summary Figure part 1
# =============================================================================

def fig0(sales_vol_by_group, lab, historic_sales_by_ms, earliest_year, ax_y_tick_intervals, ax2_y_tick_intervals, max_y_axis_val, max_y_axis2_val):
    
    fig, (ax_1, ax_2) = plt.subplots(1, 2, figsize=(6.9, 3.66))  # Adjust size as needed
    
    # =============================================================================
    # Part 1    
    # =============================================================================
    
    sales_vol_by_group["Year"] = sales_vol_by_group["Period"].astype(str).str[0:4].astype(int)
    sales_vol_by_group = sales_vol_by_group[sales_vol_by_group["Year"] >= earliest_year]
    
    sales_summary = sales_vol_by_group[["RtZ_group","Sales","Period"]].groupby(["RtZ_group", "Period"]).sum().reset_index()
    shares_summary = sales_vol_by_group[["RtZ_group","Period","shares"]].groupby(["RtZ_group", "Period"]).sum().reset_index()
    # pdb.set_trace()
    sales_summary = sales_summary.pivot(index="Period", columns="RtZ_group", values="Sales")
    shares_summary = shares_summary.pivot(index="Period", columns="RtZ_group", values="shares")
    
    sales_summary.plot(kind='bar', stacked=True, color=[bus_colour_col, heavy_col, light_med_col], width=0.75, rot=0, ax=ax_1, zorder = 3)
    # pdb.set_trace()
    # Create a secondary axis for shares
    ax2 = ax_1.twinx()
    
    # Plotting code for shares_summary
    colors = [bus_colour_col, heavy_col, light_med_col]
    markers = ['o', 'o', 'o']  # Different markers for each category
    
    for i, column in enumerate(shares_summary.columns):
        x_values = np.arange(len(shares_summary))
        y_values = shares_summary[column]
        ax2.scatter(x_values, y_values, label=column, marker=markers[i], facecolor=colors[i], edgecolor='white', s=30)
    # pdb.set_trace()
    # Customize x and y ticks
    ax_1.tick_params(axis='both', which='both', bottom=False, top=False, left = False)
    ax2.tick_params(axis='both', which='both', bottom=False, top=False, left = False, right = False)
    ax_1.set_xticks(ax_1.get_xticks())
    
    # Set x and y labels
    ax_1.set_xlabel('', fontproperties=gotham_book_font, size=8, color = "#414D56")
    ax_1.set_ylabel('', fontproperties=gotham_book_font, size=8, color = "#414D56")
    
    # Set x and y tick labels font properties
    for label in ax_1.get_xticklabels() + ax_1.get_yticklabels():
        set_font_properties(label, gotham_book_font, 8, colour = "#414D56")
    # pdb.set_trace()
    # Set x and y tick labels font properties for the second axis (ax2)
    for label in ax2.get_xticklabels() + ax2.get_yticklabels():
        set_font_properties(label, gotham_book_font, 8, colour = "#414D56")
    # pdb.set_trace()
    # Set y-tick intervals
    ax_1.set_yticks(np.arange(0, max_y_axis_val, ax_y_tick_intervals))
    ax2.set_yticks(np.arange(0, max_y_axis2_val, ax2_y_tick_intervals))
    
    # Set y-axis limits
    ax_1.set_ylim([0, max_y_axis_val])
    ax2.set_ylim([0, max_y_axis2_val])
    
    # Add grid
    ax_1.grid(color="#C8C8CB", which='major', axis='y', linestyle='solid', linewidth=0.5)
    
    # Add grid without borders
    ax_1.spines['top'].set_visible(False)
    ax_1.spines['right'].set_visible(False)
    ax_1.spines['bottom'].set_visible(False)
    ax_1.spines['left'].set_visible(False)
    
    # Add grid without borders
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    
    #remove padding for x axis
    ax_1.tick_params(axis='x', pad=-0.5)
    
    # Offset every second year and add vertical line
    for i, label in enumerate(ax_1.get_xticklabels()):
        label.set_horizontalalignment('center')
        if int(i) % 2 != 0:
            label.set_y(label.get_position()[1] - 0.08)
            # Add a vertical line for offset years outside the chart
            x_coord = ax_1.get_xticks()[i]
            ax_1.annotate('', xy=(x_coord, 0), xytext=(x_coord, -400),
                        arrowprops=dict(arrowstyle='-', color='#414D56', linewidth=0.5))
    # pdb.set_trace()
    # Create a function to format y-axis labels with commas
    def format_with_commas(value, _):
        return "{:,.0f}".format(value)
    # pdb.set_trace()
    # Set y-axis formatter for percentages
    ax2.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    
    # Set the y-axis label formatter
    ax_1.yaxis.set_major_formatter(FuncFormatter(format_with_commas))
    
    # Add y-axis label above the left chart
    ax_1.text(-0.19, 1.02, 'Sales (bars)', transform=ax_1.transAxes, fontsize=8, verticalalignment='bottom', horizontalalignment='left', fontproperties=gotham_medium_font, color = "#414D56")
    
    # Add y-axis label above the right chart
    ax2.text(1.14, 1.02, 'Shares (dots)', transform=ax2.transAxes, fontsize=8, verticalalignment='bottom', horizontalalignment='right', fontproperties=gotham_medium_font, color = "#414D56")
    
    # Add a title to the chart
    #plt.title('Sales of zero-emission heavy-duty vehicle by segment', y=1.1, x=-0.15, horizontalalignment='left', fontproperties=gotham_medium_font, fontsize=8, color = "#414D56")
    
    # Retrieve the x-axis tick labels
    xticklabels = [label.get_text() for label in ax_1.get_xticklabels()]
    
    # Find the index of the label you want to make bold
    index_to_bold = xticklabels.index(current_quarter)
    
    # Retrieve the x-axis tick labels and modify them
    xticklabels = [label.get_text() for label in ax_1.get_xticklabels()]

    # Separate the year and quarter, move "Q" below the year
    modified_labels = []
    for label in xticklabels:
        if "Q" in label:
            year, quarter = label.split()
            modified_labels.append(f"{year}\n{quarter}")
        else:
            modified_labels.append(label)
    # pdb.set_trace()
    # Set the modified labels on the x-axis
    ax_1.set_xticklabels(modified_labels, fontproperties=gotham_book_font, size=8, color='#414D56')    
    
    # Make the specified label bold
    ax_1.get_xticklabels()[index_to_bold].set_fontproperties(gotham_bold_font)
    ax_1.get_xticklabels()[index_to_bold].set_size(8)
    
    # Create custom legend markers using Line2D for circles
    legend_markers_circles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, linewidth = 0) for color in colors]
    
    # Create custom legend rectangles with Rectangle for squares
    legend_rectangles_squares = [Line2D([0], [0], marker='s', color='w', markerfacecolor=color, markersize=10, linewidth = 0) for color in [light_med_col, heavy_col, bus_colour_col]]
    
    shares_summary = shares_summary.rename(columns = {"Buses and coaches":"Buses"})
    
    # Define the order of legend labels
    legend_labels_order = ['Light and medium trucks','Heavy trucks','Buses']
    
    # Create a list of custom legend handles in the desired order
    custom_handles = [legend_markers_circles[shares_summary.columns.tolist().index(label)] for label in legend_labels_order]
    
    
    ax2.legend(custom_handles, legend_labels_order,
            loc='upper right', bbox_to_anchor=(0.94, 1.0),  title_fontsize=8, fontsize=8, frameon=True, framealpha=0.4,
            prop=gotham_book_font)
    
    ax_1.legend(legend_rectangles_squares, [' ', ' ', ' '],
            loc='upper left', bbox_to_anchor=(-0.05, 1.0), title_fontsize=8, fontsize=8, frameon=True, framealpha=0.4,
            prop=gotham_book_font)
    # Hide the legend frame
    ax2.get_legend().get_frame().set_edgecolor('none')
    
    # Hide the legend frame
    ax_1.get_legend().get_frame().set_edgecolor('none')
    
    # Change legend title font properties
    legend_title = ax_1.get_legend().get_title()
    legend_title.set_font_properties(gotham_medium_font)
    set_font_properties(ax_1.get_legend().get_title(), gotham_medium_font, 8, colour = "#414D56")
    set_font_properties(ax2.get_legend().get_title(), gotham_medium_font, 8, colour = "#414D56")
    
    # Change the font color of the legend texts
    for text in ax_1.get_legend().get_texts():
        text.set_color("#414D56")
    for text in ax2.get_legend().get_texts():
        text.set_color("#414D56")
    
    leg = ax2.get_legend()
    leg._legend_box.align = "left"
    
    ax_1.set_frame_on(False)
    ax2.set_frame_on(False)
    
    # Country Colours
    colours = pd.read_csv(RtZ_folder_location + "/inputs/country_colours.csv")
    sorted_county_sales = historic_sales_by_ms[historic_sales_by_ms["Period"] == current_quarter][["Country","order"]].sort_values("order").copy()
    countries_in_order = list(sorted_county_sales["Country"])
    
    colours = colours[colours["country_name"].isin(countries_in_order)].merge(sorted_county_sales, left_on = "country_name", right_on = "Country", how = "left")
    colours = colours[["country_name","hex_code","order"]].sort_values("order")[["country_name","hex_code"]]
    country_colours_list = list(colours["hex_code"])
    
    # =============================================================================
    # Part 2
    # =============================================================================
    
    historic_sales_by_ms["Year"] = historic_sales_by_ms["Period"].astype(str).str[0:4].astype(int)
    historic_sales_by_ms = historic_sales_by_ms[historic_sales_by_ms["Year"] >= earliest_year]
    historic_sales_by_ms = historic_sales_by_ms.sort_values("order")
    
    country_shares = historic_sales_by_ms[["Country","Period","Share"]].groupby(["Country","Period"]).sum().reset_index().copy()
    country_shares = country_shares.pivot(index="Period", columns="Country", values="Share")
    country_shares = country_shares[countries_in_order]
    
    country_shares.plot(kind='bar', stacked=True, color = country_colours_list, width=0.75, rot=0, ax=ax_2, zorder = 3, legend=False)
    # pdb.set_trace()
    # Add grid
    ax_2.grid(color="#C8C8CB", which='major', axis='y', linestyle='solid', linewidth=0.5)
    
    # Add grid without borders
    ax_2.spines['top'].set_visible(False)
    ax_2.spines['right'].set_visible(False)
    ax_2.spines['bottom'].set_visible(False)
    ax_2.spines['left'].set_visible(False)
    
    #remove padding for x axis
    ax_2.tick_params(axis='x', pad=-0.5)
    
    # Offset every second year and add vertical line
    for i, label in enumerate(ax_2.get_xticklabels()):
        label.set_horizontalalignment('center')
        if int(i) % 2 != 0:
            label.set_y(label.get_position()[1] - 0.08)
            # Add a vertical line for offset years outside the chart
            x_coord = ax_2.get_xticks()[i]
            ax_2.annotate('', xy=(x_coord, 0), xytext=(x_coord, -0.09),
                        arrowprops=dict(arrowstyle='-', color='#414D56', linewidth=0.5))

    # Set y-axis limits
    ax_2.set_ylim([0, sales_summary.sum(axis=1).max()/np.arange(0, sales_summary.sum(axis=1).max(), ax_y_tick_intervals).max()])
    
    # Add y-axis label above the left chart
    ax_2.text(-0.18, 1.02, 'Shares', transform=ax_2.transAxes, fontsize=8, verticalalignment='bottom', horizontalalignment='left', fontproperties=gotham_medium_font, color = "#414D56")
    
    # Customize x and y ticks
    ax_2.tick_params(axis='both', which='both', bottom=False, top=False, left = False)
    
    # Set y-axis formatter for percentages
    ax_2.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))

    # Retrieve the x-axis tick labels
    xticklabels = [label.get_text() for label in ax_2.get_xticklabels()]
    
    # Separate the year and quarter, move "Q" below the year
    modified_labels = []
    for label in xticklabels:
        if "Q" in label:
            year, quarter = label.split()
            modified_labels.append(f"{year}\n{quarter}")
        else:
            modified_labels.append(label)

    # Set the modified labels on the x-axis
    ax_2.set_xticklabels(modified_labels, fontproperties=gotham_medium_font, size=7.3, color='#414D56')
    # pdb.set_trace()
    # Annotate bars with country names to the right
    for i, country in enumerate(countries_in_order):
        x_position = len(country_shares) - 0.3
        y_position = sum(country_shares.iloc[-1, :i]) + country_shares.iloc[-1, i] / 2  # Position in the middle of the stacked bar
        ax_2.text(x_position, y_position, country, color=country_colours_list[i],
                ha='left', va='center', fontproperties=gotham_book_font, fontsize = 8)

    # Set x and y labels
    ax_2.set_xlabel('', fontproperties=gotham_book_font, size=8, color = "#414D56")
    ax_2.set_ylabel('', fontproperties=gotham_book_font, size=8, color = "#414D56")
     
    # Set x and y tick labels font properties
    for label in ax_2.get_xticklabels() + ax_2.get_yticklabels():
        set_font_properties(label, gotham_book_font, 8, "#414D56")

    # Find the index of the label you want to make bold
    index_to_bold = xticklabels.index(current_quarter)
    
    # Make the specified label bold
    ax_2.get_xticklabels()[index_to_bold].set_fontproperties(gotham_bold_font)
    ax_2.get_xticklabels()[index_to_bold].set_size(8)    
    
    # Add a title to the chart
    #plt.title('Sales shares of zero-emission heavy-duty vehicle by Member State', y = 1.08, x = -0.14, horizontalalignment='left', fontproperties=gotham_medium_font, fontsize=8)
    
    # Remove the axes background
    ax = plt.gca()  # Get current axes
    ax.set_facecolor('none')  # Set the color of the axes to none

    ax_2.set_frame_on(False)
    
    # To remove the figure background and make it transparent
    fig = plt.gcf()  # Get current figure
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0)  # Set transparency
    
    # Adjust spacing between subplots
    plt.subplots_adjust(wspace=0.4)  # Adjust the value of hspace as needed
    if lab == 0:
        
        plt.savefig(figures_folder + 'page1 - summary//fig_0.pdf',bbox_inches='tight', pad_inches = 0)
    else:
      plt.savefig(figures_folder + 'page1 - summary//fig_0-new_total.pdf',bbox_inches='tight', pad_inches = 0)
   
    plt.show()
    
# =============================================================================
# Figure 1.1 - Full market share by country    
# =============================================================================
    
def fig1_1(tot_ms):
    def format_with_commas(value, _):
        return "{:,.0f}".format(value)

    countries_in_order = tot_ms["Country"].tolist()

    # Load and process colours
    colours = load_colours(RtZ_folder_location + "/inputs/country_colours.csv", countries_in_order)

    # Create plot
    fig, ax = plt.subplots(figsize=(6, 3.66))
    countries = tot_ms["Country"]
    values_2024 = tot_ms["2024 Q1"]
    values_2025 = tot_ms["2025 Q1"]

    # Create a mapping of country to color
    color_mapping = colours.set_index("country_name")["hex_code"].to_dict()

    # Set up default color for any country not in the mapping
    default_color = "#007D93"

    # Assign colors to each country
    tot_ms["Color"] = tot_ms["Country"].map(color_mapping).fillna(default_color)

    # Prepare data for stacking
    bottom_2024 = 0
    bottom_2025 = 0
    bar_width = 0.75
    # Define custom positions for the bars
    x_pos_2023 = 0  # Position for 2024 bar
    x_pos_2024 = 1.5  # Position for 2024 bar (increase this value for more space)

    for i, (country, color, share_2024, share_2025) in enumerate(
        zip(tot_ms["Country"], tot_ms["Color"], tot_ms["2024 Q1 share"], tot_ms["2025 Q1 share"])
    ):
        ax.bar("2024", values_2024[i], bottom=bottom_2024, color=color, width = bar_width, label=country)
        ax.bar("2025", values_2025[i], bottom=bottom_2025, color=color, width = bar_width)
        # Add percentage labels to the right of the stacked bars
        ax.text(
            0.4,  # x-coordinate (to the right of the "2023" bar)
            bottom_2024 + values_2024[i] / 2,  # y-coordinate (middle of the bar)
            f"{share_2024 * 100:.1f}%",  # Text for the share in percentage
            va="center", ha="left", color=color, fontproperties=gotham_bold_font, fontsize=12
        )
        ax.text(
            1.4,  # x-coordinate (to the right of the "2024" bar)
            bottom_2025 + values_2025[i] / 2,  # y-coordinate (middle of the bar)
            f"{share_2025 * 100:.1f}%",  # Text for the share in percentage
            va="center", ha="left", color=color, fontproperties=gotham_bold_font, fontsize=12
        )

        bottom_2024 += values_2024[i]
        bottom_2025 += values_2025[i]

    # Add labels and legend
    ax.set_ylabel("Sales")
    ax.set_title(
        "Full market share by country",
        fontproperties=gotham_book_font,
        size=12,
        color="#414D56",
        loc="left",
        x=-0.15,
    )
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.grid(color="#C8C8CB", which="major", axis="y", linestyle="solid", linewidth=0.5)
    ax.set_axisbelow(True)
    # Customize plot
    ax.set_xlabel("", fontproperties=gotham_book_font, size=8, color="#414D56")
    ax.set_ylabel("Sales", fontproperties=gotham_book_font, size=12, color="#414D56")
    ax.tick_params(axis="x", colors="#414D56", labelsize=8, labelrotation=0)
    ax.tick_params(axis="y", colors="#414D56", labelsize=8)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(gotham_book_font)
        label.set_color("#414D56")
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#414D56")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_facecolor("none")
    ax.yaxis.set_major_formatter(FuncFormatter(format_with_commas))
    ax.tick_params(axis="both", which="both", bottom=False, top=False, left=False)

    if "Q1" in current_quarter:
        ax.set_xticklabels(
            ["Q1 " + str(int(current_quarter[0:4]) - 1), "Q1 " + str(int(current_quarter[0:4]))]
        )
    else:
        ax.set_xticklabels(
            [
                "Q1-" + current_quarter[5:7] + " " + str(int(current_quarter[0:4]) - 1),
                "Q1-" + current_quarter[5:7] + " " + str(int(current_quarter[0:4])),
            ]
        )

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        bbox_to_anchor=(1.1, 0.75),
        loc="upper left",
        handlelength=1,
        handleheight=1,
        markerscale=1.5,
        labels=reversed(labels),
        handles=reversed(handles),
        frameon=False,
        facecolor="none",
        prop=gotham_book_font,
        labelcolor="#414d56",
    )
    ax.get_legend().get_frame().set_edgecolor("none")
    fig.patch.set_facecolor("none")
    fig.patch.set_alpha(0)

    # Save and show plot
    plt.savefig(
        figures_folder + "page2 - market/fig_1_1.pdf",
        bbox_inches="tight",
        transparent=True,
        pad_inches=0,
    )
    plt.show()    
      
# =============================================================================
# Figure X.3 - sales by configuration
# =============================================================================

def figX_3(vehicle, sales_by_grouped_type):

    if vehicle == "Heavy trucks":
        save_file = "fig_2_3"
        config_order = ['4x2 tractor trailer', '4x2 rigid truck', '6x2 rigid truck', '6x2 tractor trailer', 'Other']
        config_order_new_lines = ['4x2 \ntractor \ntrailers', '4x2 \nrigid \ntrucks', '6x2 \nrigid \ntrucks', '6x2 \ntractor \ntrailers', 'Other']
        vehicle_folder = "page3 - heavy trucks/"

    if vehicle == "Light and medium trucks":
        save_file = "fig_3_3"
        config_order = ['4x2 truck', '4x2 van', '4x4 truck', '4x4 van', 'Other']
        config_order_new_lines = ['4x2 \nrigid \ntrucks', '4x2 \nvans', '4x4 \nrigid \ntrucks', '4x4 \nvans', 'Other']
        vehicle_folder = "page4 - light and medium trucks/"

    # Create a figure and a set of subplots (axes)
    fig, ax = plt.subplots(figsize=(6.75, 1.92), dpi=80)
        
    config_ht = sales_by_grouped_type[sales_by_grouped_type["RtZ_group"] == vehicle].copy()
    # pdb.set_trace()
    # Defining colors and font properties
    config_colors = ['#404C56', '#007E93', '#E15B42', '#9C1B3E', '#F2AE1D']
    
    # Pivoting the DataFrame
    config_ht = config_ht.pivot_table(index='fuel_short', columns='veh_type_short', values='shares', aggfunc='sum')
    
    # Reordering the columns
    config_ht = config_ht[config_order]
    
    # Swapping ICE and ZEV rows and renaming
    config_ht = config_ht.reindex(index=['ZEV', 'ICE'])
    config_ht.index = ['Zero-emission vehicles', 'Conventional vehicles']
    
    # Adjusting the index names to include a newline
    config_ht.index = config_ht.index.map(lambda x: x.replace("Conventional vehicles", "Conventional\nvehicles"))
    config_ht.index = config_ht.index.map(lambda x: x.replace("Zero-emission vehicles", "Zero-emission\nvehicles"))
    
    # Plotting the stacked bar chart
    config_ht.plot(kind='barh', stacked=True, ax=ax, color=config_colors, width=0.75)
    
    # Customizing the title
    #plt.title('Sales of zero-emission ' + vehicle_name_lower + ' by configuration \nand powertrain', fontproperties=gotham_bold_font, fontsize = 9, loc="left", y=1.2, x=-0.35, color='#414D56')
    
    # Add a second title
    #fig.text(-0.07, 1.2, figure_name, fontsize=7, ha='center', fontproperties=gotham_bold_font, color="#662D89")
    
    # Customizing the axis labels and ticks
    plt.xlabel('Shares', fontproperties=gotham_book_font, color='#414D56')
    plt.ylabel('')
    ax.set_xticklabels(['{:.0f}%'.format(x*100) for x in ax.get_xticks()], fontproperties=gotham_book_font, color='#414D56', fontsize = 7.8)
    
    for label in ax.get_yticklabels():
        # label.set_fontproperties(gotham_medium_font)
        # label.set_color('#414D56')
        set_font_properties(label, gotham_medium_font, 7.8, '#414D56')
    
    # Removing horizontal grid lines but keeping vertical grid lines
    ax.set_axisbelow(True)  # This moves the grid lines behind the plot elements
    ax.yaxis.grid(False)  # Remove horizontal grid lines
    ax.xaxis.grid(True, linestyle='-', linewidth=0.5, color='#414D56')  # Keep vertical grid lines
    
    # Adds a rectangle to hide some of the grid which was overlapping with the labels.
    rect = patches.Rectangle((0, 1.43), 1.5, 0.5, linewidth=0, edgecolor=None, facecolor='white', zorder=3)
    ax.add_patch(rect)
    
    # Removing the x-axis label
    plt.xlabel('')
    
    # Removing all tick marks
    ax.tick_params(axis='both', which='both', length=0)
    
    # Removing axis lines
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Removing the legend
    ax.get_legend().remove()
        
    # Annotate bars with country names to the right
    for i, config in enumerate(config_order_new_lines):
        if int(i) % 2 != 0:
            x_coord = sum(config_ht.iloc[-1, :i]) + config_ht.iloc[-1, i] / 2
            ax.annotate('', xy=(x_coord, 1.4), xytext=(x_coord, 1.85),
            arrowprops=dict(arrowstyle='-', color='black', linewidth=0.5))
            offset = 0.35
        else:
            offset = 0
        y_position = len(config_ht) - 0.3 + offset
        x_position = sum(config_ht.iloc[-1, :i]) + config_ht.iloc[-1, i] / 2  # Position in the middle of the stacked bar
        ax.text(x_position, y_position, config, color=config_colors[i],
                ha='center', va='center', fontproperties=gotham_medium_font, fontsize = 6.8)

    # Remove the axes background
    ax = plt.gca()  # Get current axes
    ax.set_facecolor('none')  # Set the color of the axes to none
    
    # To remove the figure background and make it transparent
    fig = plt.gcf()  # Get current figure
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0)  # Set transparency

    plt.savefig(figures_folder + vehicle_folder + save_file + '.pdf', bbox_inches='tight', transparent=True, pad_inches = 0)  
    
    # Show the plot
    plt.show()    

# =============================================================================
# Figure X.5 - sales share by Member State
# =============================================================================

def figX_5(vehicle, sales_vol_by_ms):
    # pdb.set_trace()
    if vehicle == "Heavy trucks":
        save_file = "fig_2_4"
        vehicle_folder = "page3 - heavy trucks/"
   
    if vehicle == "Light and medium trucks":
        save_file = "fig_3_4"
        vehicle_folder = "page4 - light and medium trucks/"
            
    # Create a figure and a set of subplots (axes)
    # fig, ax = plt.subplots(figsize=(6.369202115019011, 7.669014817150062), dpi = 80)
    fig, ax = plt.subplots(figsize=(6.369202115019011, 3.83450740857503), dpi = 80)
    # pdb.set_trace()
    # Creating a DataFrame
    sales_by_country = sales_vol_by_ms[sales_vol_by_ms["RtZ_group"]==vehicle][["Country","zev_sales"]]
    sales_by_country["zev_shares"] = sales_by_country["zev_sales"]/sales_by_country["zev_sales"].sum()
    zev_shares = ["{:.0%}".format(num) for num in sales_by_country["zev_shares"]]
    # Creating a color map
    colors = ["#E7E1EF"]
    # pdb.set_trace()
    # Creating a treemap
    squarify.plot(sizes=sales_by_country['zev_sales'], alpha=.8, color=colors, ax=ax, edgecolor="white", linewidth=3)
    
    # # # Filter the DataFrame to only include rows where 'zev_sales' > 0
    # filtered_sales = sales_by_country[sales_by_country['zev_sales'] > 0]
    
    # # Pass the filtered data to squarify.plot
    # squarify.plot(
    #     sizes=filtered_sales['zev_sales'], 
    #     alpha=.8, 
    #     color=colors, 
    #     ax=ax, 
    #     edgecolor="white", 
    #     linewidth=3
    # )

    
    # Add a title to the chart
    #plt.title('Sales of zero-emission ' + vehicle_name_lower + ' by Member State', y=1, x=0.01, horizontalalignment='left', fontproperties=gotham_bold_font, fontsize=9, color = "#414D56")
    
    # Add a second title
    #fig.text(0.178, 0.91, figure_name, fontsize=7, ha='center', fontproperties=gotham_bold_font, color="#662D89")

    plt.axis('off')
    
    # Extracting the rectangles from the plot
    rects = [patch.get_bbox() for patch in ax.patches]  
    
    # Add labels
    for rect, label, share in zip(rects, sales_by_country['Country'], zev_shares):
    # for rect, label, share in zip(rects, filtered_sales['Country'], zev_shares):
    
        x, y, dx, dy = rect.x0, rect.y0, rect.width, rect.height

        label_x = x + 0.02 * dx + 2
        label_y = y + 0.98 * dy - 1.5

        ax.text(label_x, label_y-3, label, ha='left', va='top', fontsize=8, fontproperties=gotham_medium_font, color = "#414D56")
        ax.text(label_x, label_y, share, ha='left', va='top', fontsize=8, fontproperties=gotham_bold_font, color = "#414D56")
    
    plt.savefig(figures_folder + vehicle_folder + save_file + '.pdf', bbox_inches='tight', pad_inches = 0)
        
    plt.show()

# =============================================================================
# Figure X.6 - sales share by OEM
# =============================================================================

def figX_6(vehicle, sales_share_by_oem, max_value, interval):
    
    if vehicle == "Heavy trucks":
        veh_colour = "#9C1B3E"
        save_file = "fig_2_5"
        vehicle_folder = "page3 - heavy trucks/"
    
    elif vehicle == "Light and medium trucks":
        veh_colour = "#902581"
        save_file = "fig_3_5"
        vehicle_folder = "page4 - light and medium trucks/"
        
    elif vehicle == "Buses and coaches":
        veh_colour = "#419541"
        save_file = "fig_4_5"
        vehicle_folder = "page5 - buses/"

    oem_sales = sales_share_by_oem[sales_share_by_oem["RtZ_group"] == vehicle]
    
    # It appears the shares were not correctly scaled to percentages for the matplotlib plot. Correcting this issue.
    fig, ax = plt.subplots(figsize=(5.9, 6.594928503336511))
    
    zev_shares = oem_sales[oem_sales["pt"]=="ZEV"]
    ice_shares = oem_sales[oem_sales["pt"]=="ICE"]
    
    zev_shares_list = list(zev_shares.sort_values("shares", ascending = False)["Manufacturer"])
    zev_shares_list.remove("Other")
    zev_shares_list.append("Other") #puts others at the end
    
    zev_shares = zev_shares.set_index('Manufacturer').loc[zev_shares_list].reset_index()
    zev_shares = zev_shares["shares"].tolist()
    ice_shares = ice_shares.set_index('Manufacturer').loc[zev_shares_list].reset_index()
    ice_shares = ice_shares["shares"].tolist()

    # Calculating bar positions
    bar_width = 0.4
    index = [i * 1.4 for i in range(len(zev_shares_list))]  # The 1.1 multiplier increases the space between groups    
    # Increase the gap between ZEV and ICE bars within each group
    gap = 0.05  # This is the additional space you want to add between the bars
    
    # Adjusting bar positions to include the gap
    zev_positions = [i - bar_width / 2 - gap / 2 for i in index]
    ice_positions = [i + bar_width / 2 + gap / 2 for i in index]

    # Plotting the bars with correct scaling
    ax.bar(zev_positions, zev_shares, bar_width, label='ZEV', zorder = 2, color = veh_colour)
    ax.bar(ice_positions, ice_shares, bar_width, label='ICE', zorder = 2, color = "#9FA0A6")
    
    # Setting labels, title and axes ticks
    ax.set_xticks(index)
    ax.set_xticklabels(zev_shares_list)
    ax.set_yticks(np.arange(0, max_value + 0.01, interval))

    # Adjusting the grid lines
    ax.grid(axis='y', linestyle='-', linewidth=0.5, color='#C8C8CB')
    ax.xaxis.grid(False)
    ax.yaxis.grid(True)    

    # Create custom legend rectangles with Rectangle for squares
    legend_rectangles_squares = [Line2D([0], [0], marker='s', color='w', markerfacecolor=color, markersize=10, linewidth = 0) for color in [veh_colour,"#9FA0A6"]]
    
    # Reverse the order of the legend items
    legend_rectangles_squares.reverse()
    
    # Move the legend to the left side and use custom squares
    ax.legend(legend_rectangles_squares, ["Conventional vehicles","Zero-emission vehicles"], loc='upper left', bbox_to_anchor=(0.1, 0.97), frameon=False,
              prop=gotham_book_font, handletextpad=0.1)
    # ax.legend(legend_rectangles_squares, ["Conventional vehicles","Zero-emission vehicles"], loc='upper left', bbox_to_anchor=(0.1, 0.97), frameon=False,
    #           prop={'family': gotham_book_font.get_name(), 'size': 8}, handletextpad=0.1)
    
    # Hide the legend frame
    ax.get_legend().get_frame().set_edgecolor('none')

    # Create a function to format y-axis labels with commas
    def format_with_commas(value, _):
        return "{:,.0f}".format(value)
    
    # Set y-axis formatter for percentages
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))

    # Removing x and y axis labels
    ax.set_xlabel('')
    ax.set_ylabel('')

    # Add grid without borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Add y-axis label above the left chart
    ax.text(-0.08, 1.05, 'Shares', transform=ax.transAxes, fontsize=8, verticalalignment='bottom', horizontalalignment='left', fontproperties=gotham_medium_font, color = "#414D56")

    # Customizing the title
    #plt.title('Shares of ' + vehicle_name_lower + ' by powertrain and manufacturer', fontproperties=gotham_bold_font, fontsize = 9, loc="left", y=1.075, x=-0.08, color='#414D56')
    
    # Add a second title
    #fig.text(0.11, 0.97, figure_name, fontsize=7, ha='center', fontproperties=gotham_bold_font, color="#662D89")

    # Customize x and y ticks
    ax.tick_params(axis='both', which='both', bottom=False, top=False, left = False)

    # # Add grid
    # ax.grid(color="#C8C8CB", which='major', axis='y', linestyle='-', linewidth=0.5, zorder = 1)
    
    # Set x and y tick labels font properties
    for label in ax.get_yticklabels():
        set_font_properties(label, gotham_book_font, 8, colour = "#414D56")
        
    for label in ax.get_xticklabels():
        set_font_properties(label, gotham_medium_font, 8, colour = "#414D56")

    # Offset every second year and add vertical line
    for i, label in enumerate(ax.get_xticklabels()):
        label.set_horizontalalignment('center')
        if int(i) % 2 != 0:
            label.set_y(label.get_position()[1] - 0.05)
            # Add a vertical line for offset years outside the chart
            x_coord = ax.get_xticks()[i]
            ax.annotate('', xy=(x_coord, 0), xytext=(x_coord, -max_value/16.66),
                        arrowprops=dict(arrowstyle='-', color='#414D56', linewidth=0.5))

    # Remove the axes background
    ax = plt.gca()  # Get current axes
    ax.set_facecolor('none')  # Set the color of the axes to none
    
    # To remove the figure background and make it transparent
    fig = plt.gcf()  # Get current figure
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0)  # Set transparency

    plt.savefig(figures_folder + vehicle_folder + save_file + '.pdf', bbox_inches='tight', pad_inches = 0)
        
    plt.show()

# =============================================================================
# Figure 3.4 - sales of city buses by Member State
# =============================================================================

def fig4_4(city_bus_shares_by_ms):
    # pdb.set_trace()
    vehicle_folder = "page5 - buses/"
    save_file = "fig_4_4"
    
    # Pivot data to have fuel types as columns and countries as rows
    pivoted_data = city_bus_shares_by_ms.pivot(index='Country', columns='fuel', values='shares')
    pivoted_data = pivoted_data.fillna(0)
    # Moving "EU-27" to the bottom and "aggregated Level EU 12" to second from the bottom
    eu_27_row = pivoted_data.loc['EU-27']
    # aggregated_eu_12_row = pivoted_data.loc['aggregated Level EU 12']
    # pivoted_data = pivoted_data.drop(['EU-27', 'aggregated Level EU 12'])
    pivoted_data["ZEV_share"] = pivoted_data["BEV"]+pivoted_data["FCEV"]
    pivoted_data = pivoted_data.sort_values(["ZEV_share", "Country"], ascending=False)
    pivoted_data = pivoted_data.drop("ZEV_share", axis = 1)
    # pivoted_data = pivoted_data.append(aggregated_eu_12_row)
    pivoted_data = pivoted_data.append(pd.Series(name=''))  # Adding a gap
    pivoted_data = pivoted_data.drop(index="EU-27")
    pivoted_data = pivoted_data.append(eu_27_row)
     #######33333 Change
    expected_columns = [ "Gasoline"]
    # pdb.set_trace()
    # Add missing columns with default value of 0
    # for col in expected_columns:
    #     if col not in pivoted_data.columns:
    #         pivoted_data[col] = 0
    #######33333 Change 
    
    # pdb.set_trace()
    pivoted_data = pivoted_data.rename(columns = {"BEV":"Battery electric", "FCEV":"Fuel cell electric", "ICE LNG":"Natural gas", "ICE Diesel":"Diesel incl. hybrid","ICE Gasoline":"Gasoline"})
   
    pivoted_data = pivoted_data[["Battery electric","Fuel cell electric","Natural gas","Gasoline","Diesel incl. hybrid", 'PHEV Diesel']]
    
    # Setting custom colors for each fuel type
    custom_colors = {
        'Battery electric': '#419541',
        'Fuel cell electric': '#9CBE8F',
        'Diesel incl. hybrid': '#8E8F96',
        'Natural gas': '#C9C8CB',
        'Gasoline': '#C9C8CB',
        'PHEV Diesel': '#414d56'  # Placeholder for any missing type
    }
    
    # Plotting the chart
    fig, ax = plt.subplots(figsize=(4.6, 7.48))
    pivoted_data.plot(kind='barh', stacked=True, color=custom_colors, ax=ax, width=0.75)
    
    # Customizations
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis='both', which='both', length=0)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_xticklabels(['{:.0f}%'.format(x*100) for x in ax.get_xticks()])
    ax.invert_yaxis()
    
    # Adjusting the grid lines
    ax.grid(axis='y', linestyle='-', linewidth=0.5, color='#C8C8CB')
    ax.xaxis.grid(True)
    ax.yaxis.grid(False)

    ax.set_axisbelow(True)
    
    ax.legend().set_visible(False)  # Ensuring the legend is not displayed
    
    
    # Adding raised labels over the last bar (EU-27)
    eu_27_data = pivoted_data.loc['EU-27']
    
    # cumulative_width = 0
    # for fuel_type in eu_27_data.index:
    #     if pd.notna(eu_27_data[fuel_type]) and eu_27_data[fuel_type] > 0:
    #         label_position = cumulative_width + eu_27_data[fuel_type]/2
    #         ax.text(label_position, len(pivoted_data)-1.7, fuel_type, ha='center', va='center', color=custom_colors[fuel_type], fontsize=8, fontproperties=gotham_medium_font)
    #         cumulative_width += eu_27_data[fuel_type]
    # Change
    cumulative_width = 0
    # Initialize a variable to dynamically adjust the y position
    y_pos = len(pivoted_data) - 1.7
    y_offset = 0.3  # Define an offset to move the labels up or down
    
    
    
    

    for fuel_type in eu_27_data.index:
        # pdb.set_trace()
        if pd.notna(eu_27_data[fuel_type]) and eu_27_data[fuel_type] > 0:
            label_position = cumulative_width + eu_27_data[fuel_type]/2
            # Use the y_pos variable for the y position, and modify it for each label
            ax.text(label_position, y_pos, fuel_type, ha='center', va='center', color=custom_colors[fuel_type], fontsize=8, fontproperties=gotham_medium_font)
            
            # Dynamically adjust y_pos for the next label to avoid overlap
            # This example simply toggles the y position, but you can implement more complex logic
            if y_pos == len(pivoted_data) - 1.7:
                y_pos -= y_offset  # Move label up
            else:
                y_pos = len(pivoted_data) - 1.7  # Reset to original position
            
            cumulative_width += eu_27_data[fuel_type]
    
    # Apply font to x-axis and y-axis labels
    for label in ax.get_xticklabels():
        label.set_fontproperties(gotham_book_font)
        label.set_color('#414D56')
        label.set_size(8)  
    for label in ax.get_yticklabels():
        label.set_fontproperties(gotham_medium_font)
        label.set_color('#414D56')
        label.set_size(8)  
    
    # Customizing the title
    #plt.title('Sales of zero-emission city buses by conﬁguration and powertrain', fontproperties=gotham_bold_font, fontsize = 9, loc="left", y=1.0, x=-0.15, color='#414D56')
    
    # Add a second title
    #fig.text(0.06, 0.91, "FIGURE 3.4", fontsize=7, ha='center', fontproperties=gotham_bold_font, color="#662D89")

    # Remove the axes background
    ax = plt.gca()  # Get current axes
    ax.set_facecolor('none')  # Set the color of the axes to none
    
    # To remove the figure background and make it transparent
    fig = plt.gcf()  # Get current figure
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0)  # Set transparency

    plt.savefig(figures_folder + vehicle_folder + save_file + '.pdf', bbox_inches='tight', pad_inches = 0)
    plt.show()





def figX_2(vehicle, sales_vol_by_group, q_2023_data_tmp, earliest_year, ax_max, ax_2_max, ax_y_tick_intervals, ax2_y_tick_intervals):
    def round_to_2_significant_figures(num):
        if num >= 1000:
            if num == 0:
                return 0
            else:
                d = int(math.floor(math.log10(abs(num))) - 1)
                return round(num, -d)
        else:
            remainder = num % 10
            if remainder < 5:
                return num - remainder
            else:
                return num + (10 - remainder)
    if vehicle == "Heavy trucks":
        Q1_colour = "#AB4B56"
        Q2_colour = "#BC7173"
        Q3_colour = "#CE9897"
        Q4_colour = "#E2C5C3"
        
        
        veh_colour = "#9C1B3E"
        total_q_colour = "#a43549"  # Green for total shares
        save_file = "fig_2_2"
        vehicle_folder = "page3 - heavy trucks/"
    
    elif vehicle == "Light and medium trucks":       
        Q1_colour = "#A05393"
        Q2_colour = "#B278A8"
        Q3_colour = "#C79FC0"
        Q4_colour = "#DFCBDD"
        veh_colour = "#902581"
        total_q_colour = "#6e3c82"  # Green for total shares
        save_file = "fig_3_2"
        vehicle_folder = "page4 - light and medium trucks/"
        
    elif vehicle == "Buses and coaches":
        Q1_colour = "#6AA45C"
        Q2_colour = "#8CB57F"
        Q3_colour = "#AEC8A2"
        Q4_colour = "#D3DFCB"

        veh_colour = "#419541"
        total_q_colour = "#508C4A"  # Green for total shares
        save_file = "fig_4_2"
        vehicle_folder = "page5 - buses/"
    
    # Prepare the data
    q1_2024_data = q_2024_data_tmp[q_2024_data_tmp['Period'].isin(['2024 Q1', '2024 Q2', '2024 Q3', '2024 Q4'])]
    sales_vol_ht = sales_vol_by_group.copy()

    sales_vol_ht["Year"] = sales_vol_by_group["Period"].astype(str).str[0:4].astype(int)
    sales_vol_ht["Period"] = sales_vol_ht["Period"].astype(str)
    q1_2024_data["Year"] = 2024
    sales_vol_ht = pd.concat([sales_vol_ht, q1_2024_data], ignore_index=True)
    
    sales_vol_ht = sales_vol_ht[(sales_vol_ht["Year"] >= earliest_year) & (sales_vol_ht["RtZ_group"] == vehicle)]
    
    annual_sales_summary = sales_vol_ht[["Sales", "Period"]].groupby(["Period"]).sum().reset_index()
    
    total_sales_df = sales_vol_ht.copy()
    total_sales_df["total_sales"] = total_sales_df["Sales"]/total_sales_df["shares"]
    total_sales_df = total_sales_df[total_sales_df["fuel"] == "BEV"][["Period","total_sales"]]
    
    annual_shares_summary = annual_sales_summary.copy()
    annual_shares_summary = annual_shares_summary.rename(columns = {"Sales":"ze_sales"})
    annual_shares_summary = annual_shares_summary.merge(total_sales_df, left_on = ["Period"], right_on = ["Period"])
    annual_shares_summary['Quarter_FullYear'] = annual_shares_summary['Period'].astype(str).apply(lambda x: "FY" if "Q" not in x else x.split()[-1])
    annual_shares_summary["Year"] = annual_shares_summary['Period'].astype(str).apply(lambda x: x[0:4] if "Q" not in x else x[0:4] + " Q1-Q4")
    annual_shares_summary = annual_shares_summary.groupby(["Year"]).sum().reset_index()
    annual_shares_summary["shares"] = annual_shares_summary["ze_sales"]/annual_shares_summary["total_sales"]
    annual_shares_summary = annual_shares_summary[["Year","shares"]]
    
    annual_sales_summary['Quarter_FullYear'] = annual_sales_summary['Period'].astype(str).apply(lambda x: "FY" if "Q" not in x else x.split()[-1])
    annual_sales_summary["Year"] = annual_sales_summary['Period'].astype(str).apply(lambda x: x[0:4] if "Q" not in x else x[0:4] + " Q1-Q4")
    all_periods = list(annual_sales_summary[annual_sales_summary["Quarter_FullYear"]=="FY"].Period) + ["2025 Q1", "2024 Q1"]
    
    annual_sales_summary = annual_sales_summary.pivot(index="Year", columns="Quarter_FullYear", values="Sales")

    # Combine annual and quarterly indices for proper x-axis placement

    # Increase the figure width to provide more space for x-axis
    fig, ax = plt.subplots(figsize=(3.375, 1.969), dpi=80)  # Increased width from 3.375 to 6.75 #3.375, 1.969  #4.75, 1.969
    annual_sales_summary.plot(kind='bar', stacked=True, width=0.75, rot=0, ax=ax, zorder = 3, color=[veh_colour, Q1_colour, Q2_colour, Q3_colour, Q4_colour])

    # Adjust x-tick labels to include the years and "2023 Q1+Q2", "2024 Q1+Q2"
    year_positions = list(range(len(annual_sales_summary.index))) + [all_periods.index("2024 Q1"), all_periods.index("2025 Q1")]
    ax.set_xticks(year_positions)
    ax.set_xticklabels([str(year) for year in annual_sales_summary.index] + ["2024 Q1", "2025 Q1"])

    # Add padding to the x-axis limits to ensure all bars are fully visible
    ax.set_xlim(-0.5, len(all_periods) - 0.5)

    # Create a secondary axis for shares
    ax2 = ax.twinx()
    
    annual_shares_summary['x_position'] = annual_shares_summary['Year'].apply(lambda x: annual_sales_summary.reset_index()[annual_sales_summary.reset_index()['Year'].str.contains(x)].index[0])
    ax2.scatter(annual_shares_summary['x_position'], annual_shares_summary["shares"], label="Total ZEV", marker='o', facecolor=total_q_colour, edgecolor='white', s=65, zorder=5)
    
    
    def get_periods_based_on_current_quarter(current_quarter):
        # Extract the year and quarter from the input
        year, quarter = current_quarter.split()
    
        # Convert year to integer for calculations
        year = int(year)
    
        periods = []
        
        # Dynamically construct period strings based on the current quarter input
        if quarter == "Q1":
            periods.append(f"{year} Q1")
        elif quarter == "Q2":
            periods.append(f"{year} Q1+Q2")
        elif quarter == "Q3":
            periods.append(f"{year} Q1-Q3")
        elif quarter == "Q4":
            periods.append(f"{year} Q1-Q4")
        
        return periods, year
    
    def calculate_total_shares(period, year, shares_summary, sales_summary):
        # Split the quarters from the period (e.g., "2023 Q1+Q2" -> ["Q1", "Q2"])
        quarters = period.split()[1].split('+')
    
        total_shares = 0
        total_sales = 0
        total_bev_sales = 0
        total_fcev_sales = 0
    
        for quarter in quarters:
            quarter_label = f"{year} {quarter}"
            if quarter_label in shares_summary.index and quarter_label in sales_summary.index:
                # Sum up BEV and FCEV shares for the given quarter
                total_shares += shares_summary.loc[quarter_label]["BEV"] + shares_summary.loc[quarter_label]["FCEV"]
    
                # Sales and shares for the given quarter
                bev_sales = sales_summary.loc[quarter_label]["BEV"]
                fcev_sales = sales_summary.loc[quarter_label]["FCEV"]
                bev_share = shares_summary.loc[quarter_label]["BEV"]
                
                # Avoid division by zero
                total_sales_quarter = bev_sales / bev_share if bev_share > 0 else 0
                
                total_bev_sales += bev_sales
                total_fcev_sales += fcev_sales
                total_sales += total_sales_quarter
    
        # Calculate total shares only if total sales is non-zero
        total_shares_2 = (total_bev_sales + total_fcev_sales) / total_sales if total_sales > 0 else 0
        return total_shares_2 if total_shares > 0 else None
    
    
    # # Get the periods dynamically based on the current quarter
    # periods, year = get_periods_based_on_current_quarter(current_quarter)
    
    # # Also include the previous year for the same quarters
    # previous_year = year - 1
    # previous_periods, _ = get_periods_based_on_current_quarter(f"{previous_year} {current_quarter.split()[1]}")
    
    # # Combine current year periods and previous year periods
    # all_periods_to_plot = periods + previous_periods
    
    # # Now process the periods
    # for period in all_periods_to_plot:
    #     period_year = int(period.split()[0])
    #     total_shares_2 = calculate_total_shares(period, period_year, shares_summary, sales_summary)
    
    #     if total_shares_2 is not None:
    #         position = all_periods.index(period)
    #         ax2.scatter(position, total_shares_2, label=f"Total ZEV share {period_year}", marker='o', facecolor=total_q_colour, edgecolor='white', s=65, zorder=5)

    
    # Customize x and y ticks
    ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False)
    ax2.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False)
    ax.set_xticks(ax.get_xticks())
    
    # Set x and y labels
    ax.set_xlabel('', fontproperties=gotham_book_font, size=7.3, color='#414D56')
    ax.set_ylabel('', fontproperties=gotham_book_font, size=7.3, color='#414D56')
    
    # Set x and y tick labels font properties
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        set_font_properties(label, gotham_book_font, 7.3, '#414D56')
    
    # Set x and y tick labels font properties for the second axis (ax2)
    for label in ax2.get_xticklabels() + ax2.get_yticklabels():
        set_font_properties(label, gotham_book_font, 7.3, '#414D56')

    # Set y-axis limits
    ax.set_ylim([0, ax_max])
    ax2.set_ylim([0, ax_2_max])
    
    # Set y-axis intervals for ax
    ax.set_yticks(np.arange(0, ax_max + ax_max / 1000, ax_y_tick_intervals))

    # Set y-axis intervals for ax2
    ax2.set_yticks(np.arange(0, ax_2_max + ax_2_max / 1000, ax2_y_tick_intervals))
    
    # Set x and y tick labels font properties for the second axis (ax2)
    for label in ax2.get_xticklabels() + ax2.get_yticklabels():
        label.set_color(veh_colour)
        set_font_properties(label, gotham_book_font, 7.3, veh_colour)
    
    # Add grid
    ax.grid(color="#C8C8CB", which='major', axis='y', linestyle='solid', linewidth=0.5)

    # Add grid without borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)
        
    def format_with_commas(value, _):
        return "{:,.0f}".format(value)
    
    xticklabels = [label.get_text() for label in ax.get_xticklabels()]
    modified_labels = []
    for label in xticklabels:
        if "Q" in label:
            year, quarter = label.split()
            modified_labels.append(f"{year}\n{quarter}")
        else:
            modified_labels.append(label)
    
    ax.set_xticklabels(modified_labels, fontproperties=gotham_medium_font, size=7.3, color='#414D56')
    ax2.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=len(str(ax2_y_tick_intervals))-4))
    ax.yaxis.set_major_formatter(FuncFormatter(format_with_commas))
    
    ax.text(-0.155, 1.05, 'Sales (bars)', transform=ax.transAxes, fontsize=7.3, verticalalignment='bottom', horizontalalignment='left', fontproperties=gotham_medium_font, color="#414D56")
    ax2.text(1.16, 1.05, 'Shares (dots)', transform=ax2.transAxes, fontsize=7.3, verticalalignment='bottom', horizontalalignment='right', fontproperties=gotham_medium_font, color=veh_colour)
    
    legend_rectangles_squares = [Line2D([0], [0], marker='s', color='w', markerfacecolor=color, markersize=10, linewidth=0) for color in [Q1_colour, Q2_colour, Q3_colour, Q4_colour]]
    legend_rectangles_squares.reverse()
    
    legend = ax.legend([Line2D([0], [0], marker='s', color='w', markerfacecolor=veh_colour, markersize=7), 
                        Line2D([0], [0], marker='s', color='w', markerfacecolor=Q1_colour, markersize=7),
                        Line2D([0], [0], marker='s', color='w', markerfacecolor=Q2_colour, markersize=7),
                        Line2D([0], [0], marker='s', color='w', markerfacecolor=Q3_colour, markersize=7),
                        Line2D([0], [0], marker='o', color='w', markerfacecolor=total_q_colour, markersize=7)],
                       ["ZEV sales", "Q1", "Q2", "Q3", "Q4", "ZEV shares"],
                       loc='upper left', bbox_to_anchor=(0.01, 1.1), frameon=False,
                       prop=font_manager.FontProperties(fname=gotham_book_font_path, size = 8), handletextpad=0.1)

    for text, color in zip(legend.get_texts(), ["#414D56", "#414D56", "#414D56", "#414D56", "#414D56"]):
        text.set_color(color)
    
    ax.get_legend().get_frame().set_edgecolor('none')
    
    last_non_quarterly_index = max([int(i) for i in annual_sales_summary.index.to_list() if "Q" not in i])
    ax.axvline(x=annual_sales_summary.index.to_list().index(str(last_non_quarterly_index)) + 0.5, color='#414D56', linewidth=0.5)
    
    for i in range(len(annual_sales_summary.index)):
        p = ax.patches[i]
        width = p.get_width()
        x, y = p.get_xy()
        sales_combined = annual_sales_summary.loc[annual_sales_summary.index[i], "FY"]
        rounded_value = round_to_2_significant_figures(sales_combined)
        annotation_text = f"{rounded_value:,.0f}"
    
        ax.annotate(annotation_text, (x + width / 2, y + sales_combined + ax_max / 22.22), ha='center', va='center',
                    fontproperties=gotham_bold_font, size=7.3, color=veh_colour)
    
    ax = plt.gca()
    ax.set_facecolor('none')
    
    fig = plt.gcf()
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0)
    
    # Save the figure with padding to avoid cutting off the bars
    plt.savefig(figures_folder + vehicle_folder + save_file + '.pdf', bbox_inches='tight', transparent=True, pad_inches=0.2)
    
    plt.show()       


# =============================================================================
# Figure 3.3 - historic sales of city buses by powertrain
# =============================================================================

def fig4_3(city_bus_shares_by_pt, ax_y_tick_intervals):
    
    city_bus_shares_by_pt = city_bus_shares_by_pt.sort_values(by='year')
    vehicle_folder = "page5 - buses/"
    save_file = "fig_4_3"

    # Creates a dictionary for mapping colors
    color_map = {"Diesel incl. hybrid": "#404C56", "Natural Gas": "#8E8F96", 
              "Hydrogen Fuel Cell": "#007D93", "Battery Electric": "#419541"}  
    years = city_bus_shares_by_pt.year.unique()
    powertrains = city_bus_shares_by_pt.fuel_type.unique()
    fig, ax = plt.subplots(figsize=(7.24409, 2.6378))
    city_bus_shares_by_pt_fig = city_bus_shares_by_pt.pivot(index=['year','quarter'], columns='fuel_type', values='Share')
    
    city_bus_shares_by_pt_fig.plot(style='-', ax=ax, color = color_map, linewidth = 3.3)

    # Add grid without borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Add grid
    ax.grid(color="#C8C8CB", which='major', axis='y', linestyle='solid', linewidth=0.5)

    # remove x and y ticks
    ax.tick_params(axis='both', which='both', bottom=False, top=False, left = False)

    # Set y-axis formatter for percentages
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    # pdb.set_trace()
    # Set y-axis limits
    # ax.set_ylim([0, city_bus_shares_by_pt_fig.max().max().round(1)+ax_y_tick_intervals])
    ax.set_ylim([0, round(city_bus_shares_by_pt_fig.max().max(), 1) + ax_y_tick_intervals])

    # Set y-tick intervals
    # ax.set_yticks(np.arange(0, city_bus_shares_by_pt_fig.max().max().round(1)+ax_y_tick_intervals, ax_y_tick_intervals))
    ax.set_yticks(np.arange(0, round(city_bus_shares_by_pt_fig.max().max(),1)+ax_y_tick_intervals, ax_y_tick_intervals))
    # pdb.set_trace()
    # Modify x-axis labels to only show quarters
    quarters_labels = [quarter for _, quarter in city_bus_shares_by_pt_fig.index]
    
    ax.set_xticks(range(len(quarters_labels)))
    ax.set_xticklabels(quarters_labels, fontproperties=gotham_book_font)
        
    # Function to calculate year label positions along with the corresponding year
    def calculate_year_label_positions(quarters_labels):
        positions = []
        i = 0
        while i < len(quarters_labels):
            if len(quarters_labels)-i < 4:
                position = i + (len(quarters_labels)-i)/2 - 0.5
            else:
                position = i + 1.5  # Position directly below Q2
            positions.append(position)
            i += 4
        return positions
    
    # Calculate positions for year labels
    year_label_positions = calculate_year_label_positions(quarters_labels)
    
    # Add year labels to the plot
    for i, year in enumerate(years):
        if i < len(year_label_positions):
            ax.text(year_label_positions[i], -0.25, str(year), ha='center', transform=ax.get_xaxis_transform(), fontproperties=gotham_medium_font, size=13.4, color = "#414D56")
 
    #remove x-axis label
    ax.set_xlabel('')

    # Set x and y tick labels font properties
    for label in ax.get_xticklabels():
        set_font_properties(label, gotham_medium_font, 13.4, "#414D56")

    for label in ax.get_yticklabels():
        set_font_properties(label, gotham_book_font, 13.4, "#414D56")
    
    for i, quarter in enumerate(quarters_labels):
        if quarter == "Q4":
            ax.axvline(i + 0.5, color='#414D56', linewidth=0.5)  # Adding 0.5 to center the line within the bar    
    
    ax.get_legend().remove()
    
    # Annotate bars with country names to the right
    df_annotations = city_bus_shares_by_pt.copy()
    df_annotations["year_index"] = df_annotations["year_index"].str.replace("_"," ")

    for i, pt in enumerate(powertrains):     
        x_position = len(quarters_labels)-0.5
        y_position = df_annotations[(df_annotations["year_index"]==current_quarter) & (df_annotations["fuel_type"]==pt)]["Share"]
        ax.text(x_position, y_position, pt, 
                ha='left', va='center', fontproperties=gotham_medium_font, fontsize = 13.4, color = color_map[pt])
    
    # Remove the axes background
    ax = plt.gca()  # Get current axes
    ax.set_facecolor('none')  # Set the color of the axes to none
    
    # To remove the figure background and make it transparent
    fig = plt.gcf()  # Get current figure
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0)  # Set transparency
    # pdb.set_trace()

    plt.savefig(figures_folder + vehicle_folder + save_file + '.pdf', bbox_inches='tight', pad_inches = 0)    
    plt.show()
      
def load_data(file_path, sheet_name):
    return pd.read_excel(file_path, sheet_name)

def prepare_hist_data(df, start_year):
    df_copy = df.copy()
    df_copy["Year"] = df_copy["Period"].astype(str).str[0:4].astype(int)
    return df_copy[df_copy["Year"] >= start_year]

def create_pivot_table(df, index, columns, values, fill_value=0):
    return df.pivot_table(index=index, columns=columns, values=values, fill_value=fill_value)

def load_colours(file_path, countries):
    colours = pd.read_csv(file_path)
    return colours[colours["country_name"].isin(countries)]

def merge_and_sort_colours(colours, sorted_sales, on_col="country_name", sort_col="order"):
    return colours.merge(sorted_sales, left_on=on_col, right_on="Country", how="left").sort_values(sort_col)[["country_name", "hex_code"]]

def calculate_share(df):
    return df / df.sum() * 100

# def plot_stacked_bar(ax, data, shares, countries, colours, year_label):
    # bottom = 0
    # for country, color in zip(countries, colours):
    #     sales = data[country]
    #     share = shares[country]
    #     ax.bar(year_label, sales, bottom=bottom, color=color, edgecolor=None)
    #     ax.text(year_label, bottom + sales / 2, f'{share:.1f}%', ha='center', va='center', color='white', fontproperties=gotham_bold_font, size=6)
    #     bottom += sales
def plot_stacked_bar(ax, data, shares, countries, colours, year_label):
    bottom = 0
    rounded_shares = []
    total_sales = sum(data[country] for country in countries)

    # Calculate the initial rounded shares
    for country in countries:
        share = shares[country]
        rounded_share = round(share, 1)
        rounded_shares.append(rounded_share)

    # Adjust the rounded shares to sum to 100%
    rounding_error = 100 - sum(rounded_shares)
    if rounding_error != 0:
        adjustment_index = np.argmax(rounded_shares) if rounding_error > 0 else np.argmin(rounded_shares)
        rounded_shares[adjustment_index] += rounding_error

    for country, color, rounded_share in zip(countries, colours, rounded_shares):
        sales = data[country]
        ax.bar(year_label, sales, bottom=bottom, color=color, edgecolor=None)
        ax.text(year_label, bottom + sales / 2, f'{rounded_share:.1f}%', ha='center', va='center', color='white', fontproperties=gotham_bold_font, size=6)
        bottom += sales

    # Ensure the total share is exactly 100%
    assert abs(sum(rounded_shares) - 100) < 1e-9, f"Rounded shares do not sum to 100%: {sum(rounded_shares)}"

    
    

# fig0(sales_vol_by_group, 0, historic_sales_by_ms, fig_0_earliest_year, fig_0_sale_vol_intervals, fig_0_sale_share_intervals, fig_0_max_y_axis_val, max_y_axis2_val)
# figX_3("Heavy trucks", sales_by_grouped_type)
# figX_3("Light and medium trucks", sales_by_grouped_type)

# figX_5("Heavy trucks", sales_vol_by_ms)
# figX_5("Light and medium trucks", sales_vol_by_ms)

# figX_6("Heavy trucks", sales_share_by_oem, max_value = fig_1_6_max_val, interval = fig_1_6_interval)
# figX_6("Light and medium trucks", sales_share_by_oem, max_value = fig_2_6_max_val, interval = fig_2_6_interval)
# figX_6("Buses and coaches", sales_share_by_oem, max_value = fig_3_6_max_val, interval = fig_3_6_interval)

# fig4_4(city_bus_shares_by_ms)

# fig4_3(city_bus_shares_by_pt, ax_y_tick_intervals = fig_3_3_ax_y_tick_intervals)

# figX_2("Heavy trucks", sales_vol_by_group,q_2024_data, earliest_year = fig_1_2_earliest_year, 
#             ax_max = fig_1_2_max_vol, ax_2_max = fig_1_2_max_share, ax_y_tick_intervals = fig_1_2_ax_y_tick_intervals, ax2_y_tick_intervals = fig_1_2_ax2_y_tick_intervals)
# figX_2("Light and medium trucks", sales_vol_by_group,q_2024_data, earliest_year = fig_2_2_earliest_year,
#             ax_max = fig_2_2_max_vol, ax_2_max = fig_2_2_max_share, ax_y_tick_intervals = fig_2_2_ax_y_tick_intervals, ax2_y_tick_intervals = fig_2_2_ax2_y_tick_intervals)
figX_2("Buses and coaches", sales_vol_by_group, q_2024_data,earliest_year = fig_3_2_earliest_year, 
            ax_max = fig_3_2_max_vol, ax_2_max = fig_3_2_max_share, ax_y_tick_intervals = fig_3_2_ax_y_tick_intervals, ax2_y_tick_intervals = fig_3_2_ax2_y_tick_intervals)

# fig1_1(total_market_share_ms)


