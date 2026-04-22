import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/raw/NAEP_State_Scores.csv", low_memory=False)

#Pivot the data to compare years side-by-side
df_pivot = df.pivot_table(
    index=['State', 'Subject', 'Grade'], 
    columns='Year', 
    values='AverageScaleScore'
).reset_index()

#Calculate the improvement (difference) for each category
df_pivot['Improvement_2022_2024'] = df_pivot[2024] - df_pivot[2022]

#Calculate the average improvement per state across all subjects/grades
state_improvement = df_pivot.groupby('State')['Improvement_2022_2024'].mean().reset_index()

#Identify Top 5 and Bottom 5
top_5 = state_improvement.sort_values(by='Improvement_2022_2024', ascending=False).head(5)
bottom_5 = state_improvement.sort_values(by='Improvement_2022_2024', ascending=True).head(5)

#Combine and Plot
plot_df = pd.concat([bottom_5, top_5]).sort_values(by='Improvement_2022_2024')

plt.figure(figsize=(10, 6))
colors = ['red' if x < 0 else 'green' for x in plot_df['Improvement_2022_2024']]
plt.barh(plot_df['State'], plot_df['Improvement_2022_2024'], color=colors)
plt.xlabel('Average Score Change (2022-2024)')
plt.title('Top 5 vs Bottom 5 States by Score Improvement')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.savefig("../top_5_vs_bottom_5.png")
print("Plot saved as top_5_vs_bottom_5.png in the project root.")


#2019-2022
# Load the dataset
df = pd.read_csv("../data/raw/NAEP_State_Scores.csv", low_memory=False)

# Pivot the data to compare years side-by-side
df_comparison = df.pivot_table(
    index=['State', 'Subject', 'Grade'], 
    columns='Year', 
    values='AverageScaleScore'
).reset_index()

# Calculate the improvement (difference) for 2019 to 2022
# Note: In most cases this will be a negative number due to the 2022 score drops
df_comparison['Score_Change_19_22'] = df_comparison[2022] - df_comparison[2019]

# Calculate the average improvement per state across all subjects/grades
state_trends_19_22 = df_comparison.groupby('State')['Score_Change_19_22'].mean().reset_index()

# Identify Top 5 (least decline/most growth) and Bottom 5 (most decline)
top_5_states = state_trends_19_22.sort_values(by='Score_Change_19_22', ascending=False).head(5)
bottom_5_states = state_trends_19_22.sort_values(by='Score_Change_19_22', ascending=True).head(5)

# Combine for visualization
df_plot_19_22 = pd.concat([bottom_5_states, top_5_states]).sort_values(by='Score_Change_19_22')

# Plotting
plt.figure(figsize=(10, 6))
# Define colors: Red for decline, Green for improvement
colors = ['red' if x < 0 else 'green' for x in df_plot_19_22['Score_Change_19_22']]

plt.barh(df_plot_19_22['State'], df_plot_19_22['Score_Change_19_22'], color=colors)
plt.xlabel('Average Score Change (2019-2022)')
plt.title('Top 5 vs Bottom 5 States: Score Trends (2019-2022)')
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Saving with a specific name for the 19-22 period
plt.savefig("../state_trends_2019_2022.png")
print("Plot saved as state_trends_2019_2022.png in the project root.")
