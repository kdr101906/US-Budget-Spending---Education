import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import poc_merge as pm
import os
import seaborn as sns


def dataframe():
    fund_2019 = pd.read_csv("data/raw/2019contracts.csv", low_memory=False)
    fund_2022 = pd.read_csv("data/raw/2022contracts.csv", low_memory=False)
    fund_2024 = pd.read_csv("data/raw/2024contracts.csv", low_memory=False)
    fund_2019["Year"] = 2019
    fund_2022["Year"] = 2022
    fund_2024["Year"] = 2024
    All_contracts = pd.concat([fund_2019, fund_2022, fund_2024], ignore_index=True)
    print(len(All_contracts))#Number of rows when we concatonated the 2019, 2022, and 2024 contracts csv files
    All_contracts["recipient_state_name"] = All_contracts["recipient_state_name"].astype(str).str.lower().str.strip()
    contracts = All_contracts.groupby(["recipient_state_name", "Year"])["federal_action_obligation"].sum().reset_index()
    contracts = contracts.rename(columns={"recipient_state_name": "State", "federal_action_obligation": "Federal Funding"})
    scores = pd.read_csv("data/raw/NAEP_State_Scores.csv")
    scores["State"] = scores["State"].astype(str).str.lower().str.strip()
    scores["Year"] = scores["Year"].astype(int)
    print(len(scores)) #The number of rows in external dataset for the test scores in 2019 2022 2024
    df = pd.merge(scores, contracts, on=["State", "Year"], how = "left") #The keys used to merge were the state and year
    df["Federal Funding"] = df["Federal Funding"].fillna(0) #11 states are not in the 2022contracts.csv so we fill the NaN values with 0 instead
    print("The keys used to merge were State and Year.")
    print(df)
    print(len(df)) #Number of rows in final merged dataset
    output_dir = "data/clean"
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(f"{output_dir}/final_summary_table.csv", index=False)
    print(f"File successively saved.")
    return df


def map(df, start_year, end_year):
    selected_states = ["louisiana", "west virginia", "mississippi", "kentucky", "tennessee", "idaho", "florida", "nebraska", "wyoming", "alaska"]
    df_start = df[df["Year"] == start_year].groupby("State")["Federal Funding"].first()
    df_end = df[df["Year"] == end_year].groupby("State")["Federal Funding"].first()
    #The difference
    full_diff = pd.DataFrame({'funding_start': df_start,'funding_end': df_end})
    full_diff["Funding_Change"] = full_diff["funding_end"] - full_diff["funding_start"]
    full_diff = full_diff.reset_index()
    #Chloropeth maps only take the state abbreviations
    state_to_code = {
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
    full_diff["Code"] = full_diff["State"].str.strip().map(state_to_code)
    full_diff["Group"] = full_diff["State"].apply(lambda x: "Focus State" if x in selected_states else "Other State")
    fig = px.choropleth(
        full_diff,
        locations="Code",
        locationmode="USA-states",
        color="Funding_Change",
        scope="usa",
        color_continuous_scale="RdBu",
        color_continuous_midpoint=0,
        title=f"Change in Federal Funding ({start_year}-{end_year})",
        labels={'Funding_Change': 'Change in Funding ($)', 'Group': 'Dataset Group'},
        hover_data=["Group", "Funding_Change"] 
    )
    save_path = f"data/clean/funding{start_year}_{end_year}.png"
    fig.write_image(save_path)

if __name__ == "__main__":
    finaldf = dataframe()
    comparisons = [(2019, 2022), (2019, 2024), (2022, 2024)]
    for start, end in comparisons:
        map(finaldf, start, end)






