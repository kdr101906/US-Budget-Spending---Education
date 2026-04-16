import pandas as pd

contracts = pd.read_csv("../data/raw/All_Contracts.csv", low_memory=False)
print(len(contracts))#Number of rows in the USASpending dataset sample
contracts = contracts[contracts['awarding_agency_name'] == "Department of Education"]
contracts['recipient_state_name'] = contracts['recipient_state_name'].str.lower().str.strip()
funding = contracts.groupby("recipient_state_name")["federal_action_obligation"].sum().reset_index() #groups by state names and adds the funding values up for each state
funding.columns = ["State", "Federal Funding"]

scores = pd.read_csv("../data/raw/NAPE_State_Scores.csv")
print(len(scores)) #The number of rows in external dataset for the test scores in 2019
scores['State'] = scores['State'].str.lower().str.strip()
df = pd.merge(scores, funding, on="State", how="inner") 
print("The key we merged on was State") #Merged on the Key State
print(df)
print(len(df)) #The length of the merged dataset

