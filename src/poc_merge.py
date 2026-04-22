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


if __name__ == '__main__':
    finaldf = dataframe()