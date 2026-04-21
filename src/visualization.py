import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import poc_merge as pm
import os
import seaborn as sns

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import os

def dataframe():
    fund_2019 = pd.read_csv("data/raw/2019contracts.csv", low_memory=False)
    fund_2022 = pd.read_csv("data/raw/2022contracts.csv", low_memory=False)
    fund_2024 = pd.read_csv("data/raw/2024contracts.csv", low_memory=False)
    fund_2019["Year"] = 2019
    fund_2022["Year"] = 2022
    fund_2024["Year"] = 2024
    All_contracts = pd.concat([fund_2019, fund_2022, fund_2024], ignore_index=True)
    print(len(All_contracts))#Number of rows when we concatonated the 2019, 2022, and 2024 contracts csv files
    contracts = All_contracts.groupby(["recipient_state_name", "Year"])["federal_action_obligation"].sum().reset_index()
    contracts = contracts.rename(columns={"recipient_state_name": "State", "federal_action_obligation": "Federal Funding"})
    contracts['State'] = contracts['State'].str.lower().str.strip()
    scores = pd.read_csv("data/raw/NAEP_State_Scores.csv")
    scores["State"] = scores["State"].str.lower().str.strip()
    print(len(scores)) #The number of rows in external dataset for the test scores in 2019 2022 2024
    df = pd.merge(scores, contracts, on=["State", "Year"], how = "inner") #The keys used to merge were the state and year
    print("The keys used to merge were State and Year.")
    print(df)
    print(len(df)) #Number of rows in final merged dataset
    output_dir = "data/clean"
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(f"{output_dir}/final_summary_table.csv", index=False)
    print(f"File successively saved.")
    return df

def trends(df):
    plt.figure(figsize=(12, 8))
    
    # Create the scatter plot
    # We use a dictionary to ensure each year gets a specific color
    colors = {2019: 'blue', 2022: 'red', 2024: 'green'}
    
    for year in [2019, 2022, 2024]:
        subset = df[df['Year'] == year]
        plt.scatter(subset['Federal Funding'], subset['AverageScaleScore'], 
                    label=year, color=colors[year], alpha=0.6, edgecolors='w')

    plt.title("Impact of Federal Funding on NAEP Scores")
    plt.xlabel("Federal Funding ($)")
    plt.ylabel("Average Scale Score")
    plt.legend(title="Year")
    plt.grid(True, linestyle='--', alpha=0.7)

    # Save to clean directory
    save_path = "data/clean/funding_vs_scores.png"
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"PNG version saved to: {save_path}")

def plot_map(df):
    years = [2019, 2022, 2024]
    
    # Lowercase dictionary for exact matching
    state_to_abbrev = {
        "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
        "colorado": "CO", "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA",
        "hawaii": "HI", "idaho": "ID", "illinois": "IL", "indiana": "IN", "iowa": "IA",
        "kansas": "KS", "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
        "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS", "missouri": "MO",
        "montana": "MT", "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ",
        "new mexico": "NM", "new york": "NY", "north carolina": "NC", "north dakota": "ND", "ohio": "OH",
        "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
        "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT", "vermont": "VT",
        "virginia": "VA", "washington": "WA", "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY"
    }

    for year in years:
        # 1. Filter data for the specific year
        df_year = df[df["Year"] == year].copy()
        
        # 2. Map the state codes
        df_year["State_Code"] = df_year["State"].str.strip().map(state_to_abbrev)

        # 3. Create the Choropleth
        fig = px.choropleth(
            df_year,
            locations="State_Code", 
            locationmode="USA-states",
            color="Federal Funding",
            scope="usa",
            title=f"{year} Federal Funding by State",
            color_continuous_scale="Reds",
            # This ensures the color scale is consistent across all years for comparison
            range_color=[df["Federal Funding"].min(), df["Federal Funding"].max()]
        )

        # 4. Save each year as a unique file in data/clean
        save_path = f"data/clean/funding_map_{year}.png"
        fig.write_image(save_path)
        print(f"Map successfully saved to {save_path}")


if __name__== "__main__":
    finaldf = dataframe()
    plot_map(finaldf)



