Second Idea:Education

Question: Do states that recieve higher federal funding get higher scores on the NAEP for math and reading in 2019 (National Assessment of Educational Progress)?
For the columns in the usaspending.gov data (columns.csv), we will be looking atr the recipient_state_name for the total funding per state as well as the federal_action_obligation to see the amount of money the government spent for that transaction. We will also be looking at the awarding_agency_name and filter it to only show the Department of Education. 
For the externalk dataset, we will be looking at the Nation's Report Card dataset which averages the scores of students in 4th grade and 8th grade per state on the NAEP test for reading and math. We will be looking at the Jurisdiction header which contains the state as well as the Average scale score which is the average score for that state.
We will be merging on the state so we will rename Jurisdiction for the Nation's Report Card dataset to state to match the csv file. 

Our proposed conclusion is that there may be a positive correlation in that more federal money spent for schools will will lead to greater test scores on the NAEP. 


New Question: To what extent is the change in state NAEP scores in 2019, 2022, and 2024 correlated with the level of federal Department of Education funding each state recieves? 

Look at maybe top 5 and bottom 5 states for NAEP scores and see if it is associated with Federal funding?