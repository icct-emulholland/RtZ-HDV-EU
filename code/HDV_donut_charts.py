import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import os
import pdb

def process_and_plot_data():
    # Load data
    # pdb.set_trace()
    RtZ_folder_location = r"/Users/e.mulholland/Documents/Work 2025/EU/RtZ/Q1/RtZ_formatter_folder2025"
    raw_data = pd.read_csv(RtZ_folder_location + "/outputs/2025_Q1_full_data.csv")
    # raw_data['RtZ_group'] = raw_data['RtZ_group'].fillna('unspec')
    raw_data = raw_data.dropna(subset=['RtZ_group'])

    raw_data_2024_Q1 = pd.read_csv(RtZ_folder_location + "/outputs/2025_Q1_full_data.csv")
    # raw_data_2024_Q1['RtZ_group'] = raw_data_2024_Q1['RtZ_group'].fillna('unspec')
    raw_data_2024_Q1 = raw_data_2024_Q1.dropna(subset=['RtZ_group'])
    font_paths = {
        "GothamBook": os.path.join(RtZ_folder_location, "fonts", "GothamBook.otf"),
        "GothamMedium": os.path.join(RtZ_folder_location, "fonts", "GothamMedium.otf"),
        "GothamBold": os.path.join(RtZ_folder_location, "fonts", "Gotham-Bold.otf"),
    }
    fonts = {key: font_manager.FontProperties(fname=path) for key, path in font_paths.items()}

    # Process and group data
    base_map = {}
    for name in sorted(raw_data['Manufacturer'], key=len):
        if not any(base in name for base in base_map):
            base_map[name] = name
        else:
            for base in base_map:
                if name.startswith(base):
                    base_map[name] = base
                    break

    # Function to determine body type
    def determine_body_type(row):
        if row['RtZ_group'] == 'Heavy trucks':
            if row['Body type'] == 'HCV Tractor Truck':
                return 'Heavy trucks - Tractor'
            else:
                return 'Heavy trucks - Rigid'
        else:
            return row['RtZ_group']

    raw_data['Body_Type_Grouped'] = raw_data.apply(determine_body_type, axis=1)
    raw_data['Standardized_Manufacturer'] = raw_data['Manufacturer'].apply(lambda x: base_map.get(x, x))

    # Aggregate Q1, Q2, Q3, and Q4 for 2025
    # raw_data['Q1_Q2_Q3_Q4_2025'] = raw_data['Q1_2025'] + raw_data['Q2_2025'] + raw_data['Q3_2025'] + raw_data['Q4_2025']
    raw_data['Q1_2025'] = raw_data['Q1_2025']

    grouped_sales = raw_data.groupby(['Standardized_Manufacturer', 'Body_Type_Grouped'])['Q1_2025'].sum()
    total_market_sales = raw_data['Q1_2025'].sum()
    total_sales_by_manufacturer = grouped_sales.groupby(level=0).sum()

    # Select top 7 manufacturers
    top_manufacturers = total_sales_by_manufacturer.sort_values(ascending=False).head(7)
    top_7_manufacturers = top_manufacturers.index.tolist()
    raw_data['Standardized_Manufacturer'] = raw_data['Standardized_Manufacturer'].apply(
        lambda x: x if x in top_7_manufacturers else 'Others'
    )
    grouped_sales = raw_data.groupby(['Standardized_Manufacturer', 'Body_Type_Grouped'])['Q1_2025'].sum()
    total_market_sales = raw_data['Q1_2025'].sum()
    total_sales_by_manufacturer = grouped_sales.groupby(level=0).sum()
    top_manufacturers = total_sales_by_manufacturer.sort_values(ascending=False)

    # Aggregate Q1 and Q2 for 2024
    # raw_data_2024_Q1['Q1_Q2_Q3_Q4_2024'] = raw_data_2024_Q1['Q1_2024'] + raw_data_2024_Q1['Q2_2024'] + raw_data_2024_Q1['Q3_2024'] + raw_data_2024_Q1['Q4_2024']
    raw_data_2024_Q1['Q1_2024'] = raw_data_2024_Q1['Q1_2024']

    raw_data_2024_Q1['Standardized_Manufacturer'] = raw_data_2024_Q1['Manufacturer'].apply(
        lambda x: base_map.get(x.split('/')[0].split('-')[0].strip(), x.split('/')[0].split('-')[0].strip())
    )

    raw_data_2024_Q1['Body_Type_Grouped'] = raw_data_2024_Q1.apply(determine_body_type, axis=1)
    grouped_sales_2024_Q1 = raw_data_2024_Q1.groupby(['Standardized_Manufacturer', 'Body_Type_Grouped'])['Q1_2024'].sum()
    total_market_sales_2024_Q1 = raw_data_2024_Q1['Q1_2024'].sum()
    total_sales_by_manufacturer_2024_Q1 = grouped_sales_2024_Q1.groupby(level=0).sum()

    # Select top 7 manufacturers
    top_manufacturers_2024_Q1 = total_sales_by_manufacturer_2024_Q1.sort_values(ascending=False).head(7)
    top_7_manufacturers_2024_Q1 = top_manufacturers_2024_Q1.index.tolist()
    raw_data_2024_Q1['Standardized_Manufacturer'] = raw_data_2024_Q1['Standardized_Manufacturer'].apply(
        lambda x: x if x in top_7_manufacturers_2024_Q1 else 'Others'
    )
    grouped_sales_2024_Q1 = raw_data_2024_Q1.groupby(['Standardized_Manufacturer', 'Body_Type_Grouped'])['Q1_2024'].sum()
    total_market_sales_2024_Q1 = raw_data_2024_Q1['Q1_2024'].sum()
    total_sales_by_manufacturer_2024_Q1 = grouped_sales_2024_Q1.groupby(level=0).sum()

    # Create list of vectors for pie chart divisions with percentages
    pie_chart_percentages = []

    for manufacturer in top_manufacturers.index:
        sizes = grouped_sales.loc[manufacturer]
        total = sizes.sum()
        percentages = (sizes / total) * 100  # Calculate percentages for the pie chart
        pie_chart_percentages.append(percentages.values.tolist())  # Convert to list and append

    print("Pie Chart Percentages (RtZ Groups):")
    for i, percentages in enumerate(pie_chart_percentages):
        print(top_manufacturers.index[i], ":", percentages)
    
    colors = ['#414D56', '#007D93', '#ce6832', '#9c1b3e', '#e5dee9']  # Added grey 
    
    legend_labels_in = ['Buses and coaches', 'Heavy trucks - Tractor', 'Heavy trucks - Rigid', 'Light and medium trucks']
    legend_labels = sorted(legend_labels_in)
    legend_labels

    # Create patches for legend
    legend_patches = [plt.Line2D([0], [0], marker='o', color='w', label=label, markerfacecolor=color, markersize=10) 
                      for label, color in zip(legend_labels, colors)]

    # Calculate market shares for 2025
    market_shares = (total_sales_by_manufacturer / total_market_sales) * 100
    top_manufacturers_market_shares = market_shares[top_manufacturers.index]

    # Calculate market shares for 2024
    market_shares_2024_Q1 = (total_sales_by_manufacturer_2024_Q1 / total_market_sales_2024_Q1) * 100
    top_manufacturers_market_shares_2024_Q1 = market_shares_2024_Q1[top_manufacturers_2024_Q1.index]

    # Calculate change in market share from 2024 to 2025
    market_share_change_not_round = top_manufacturers_market_shares - top_manufacturers_market_shares_2024_Q1

    rounded_market_share_change = market_share_change_not_round.round(1)

    # Calculate the difference from zero
    total_diff = rounded_market_share_change.sum()

    # Adjust the last element to ensure the sum is exactly zero
    if total_diff != 0:
        smallest_abs_idx = rounded_market_share_change.abs().idxmin()
        rounded_market_share_change[smallest_abs_idx] -= total_diff

    print(rounded_market_share_change)
    print(f"Sum after adjustment: {rounded_market_share_change.sum()}")

    market_share_change = rounded_market_share_change.copy()
    market_share_change_with_sign = []

    # Create a vector that includes the sign of the change
    for manufacturer in top_manufacturers.index:
        change = market_share_change[manufacturer]
        if change > 0:
            change_with_sign = f"+{change:.2f}pp"
        elif change < 0:
            change_with_sign = f"{change:.2f}pp"
        else:
            change_with_sign = "0.00%"
        market_share_change_with_sign.append(change_with_sign)

    # Display the changes
    print("Market Share Change from 2024 Q1 to 2025 Q1:")
    for i, manufacturer in enumerate(top_manufacturers.index):
        print(f"{manufacturer}: {market_share_change_with_sign[i]}")

    # Normalize radii so the max radius is 300
    max_radius = 480  # 480
    scaled_radii = (top_manufacturers_market_shares / top_manufacturers_market_shares.max()) * max_radius
    scaled_radii_array = scaled_radii.round().astype(int).values  # Convert to integer and numpy array

    print("Scaled Radii:")
    print(scaled_radii_array)

    top_manufacturers_names = np.array(top_manufacturers.index.tolist())

    class C():
        def __init__(self, r, fette):
            self.N = len(r)
            self.x = np.ones((self.N, 3))
            self.x[:, 2] = r
            self.fette = fette
            maxstep = 2 * self.x[:, 2].max()
            length = np.ceil(np.sqrt(self.N))
            grid = np.arange(0, length * maxstep, maxstep)
            gx, gy = np.meshgrid(grid, grid)
            self.x[:, 0] = gx.flatten()[:self.N]
            self.x[:, 1] = gy.flatten()[:self.N]
            self.x[:, :2] = self.x[:, :2] - np.mean(self.x[:, :2], axis=0)
            self.step = self.x[:, 2].min()
            self.p = lambda x, y: np.sum((x**2 + y**2)**2)
            self.E = self.energy()
            self.iter = 1.

        def minimize(self):
            while self.iter < 1000 * self.N:
                for i in range(self.N):
                    rand = np.random.randn(2) * self.step / self.iter
                    self.x[i, :2] += rand
                    e = self.energy()
                    if e < self.E and self.isvalid(i):
                        self.E = e
                        self.iter = 1.
                    else:
                        self.x[i, :2] -= rand
                        self.iter += 1.

        def energy(self):
            return self.p(self.x[:, 0], self.x[:, 1])

        def isvalid(self, i):
            for j in range(self.N):
                if i != j:
                    if self.distance(self.x[i, :], self.x[j, :]) < 0:
                        return False
            return True

        def distance(self, x1, x2):
            return np.sqrt((x1[0] - x2[0])**2 + (x1[1] - x2[1])**2) - x1[2] - x2[2]

        def plot(self, ax):
            for i in range(self.N):
                radius = self.x[i, 2]
                data = self.fette[i]
                x_center, y_center = self.x[i, 0], self.x[i, 1]
                radius_normalized = radius / (ax.figure.bbox.width / 2)
                pie_ax = plt.axes([x_center / ax.figure.bbox.width - radius_normalized / 2,
                                   y_center / ax.figure.bbox.height - radius_normalized / 2,
                                   radius_normalized, radius_normalized], aspect='equal', frameon=False)
                if top_manufacturers_names[i] == 'Mercedes':
                    leg = fig.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(3, 0.5), fontsize=20, prop={'size': 18})
                    
                pie_ax.pie(data, colors=colors, autopct='%1.1f%%', pctdistance=0.85, textprops={'fontsize': 18, 'color': 'white'})
                
                white_circle_radius = radius_normalized * .08  # 1/3 del raggio del cerchio
                if top_manufacturers_names[i] == 'Renault':
                    white_circle_radius *= 2.3
                elif top_manufacturers_names[i] == 'DAF':
                    white_circle_radius *= 1.2
                circle = plt.Circle((0.5, 0.5), white_circle_radius, color='white', transform=pie_ax.transAxes)
                pie_ax.add_artist(circle)

                x_pos, y_pos = 0.5, 0.5
                alignment = {'ha': 'center', 'va': 'center', 'transform': pie_ax.transAxes}
                font_settings = {'color': 'black', 'fontsize': 20, 'fontproperties': fonts['GothamMedium']}
                
                pie_ax.text(x_pos, y_pos, f'{top_manufacturers_names[i]}\n{top_manufacturers_market_shares[i]:.1f}%',
                            **alignment, **font_settings)
                
                change_color = 'green' if '+' in market_share_change_with_sign[i] else 'red'
                
                if top_manufacturers_names[i] == 'Renault':
                    pie_ax.text(x_pos, y_pos - 0.1, f'({market_share_change_with_sign[i]})',
                                **alignment, color=change_color, fontsize=15, fontproperties=fonts['GothamMedium'])
                else:
                    pie_ax.text(x_pos, y_pos - 0.08, f'({market_share_change_with_sign[i]})',
                                **alignment, color=change_color, fontsize=15, fontproperties=fonts['GothamMedium'])
            
    c = C(scaled_radii_array, pie_chart_percentages)

    fig, ax = plt.subplots(figsize=(3.66, 3.66), subplot_kw=dict(aspect="equal"), dpi=80)
    fig.subplots_adjust(right=0.75)
    ax.axis("off")

    ax = plt.gca()
    ax.set_facecolor('none')
    fig = plt.gcf()
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0)
    c.minimize()
    c.plot(ax)
    plt.title('Q1',fontsize=8, color = "#414D56")
    
    plt.savefig(RtZ_folder_location + '/figures/page2 - market/fig_1_2.pdf', bbox_inches='tight', pad_inches=0)
    plt.show()

    raw_data.to_csv(RtZ_folder_location + "/outputs/update_fig_new_0_Q1.csv", index=False)


process_and_plot_data()
