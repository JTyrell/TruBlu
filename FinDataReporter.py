""" 
This is a based on a loan approval prediction tool, to use statistical analysis to present
information in useful graphical representations. I chose this based on the nature 
of the cool company I'm about to work with.
 """
 
 #Data manipulation packages
import pandas as pd
import numpy as np

#Data visualization packages
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import io
print("Package imports successful")

# Load data from a CSV file or website
datafl = pd.read_csv('loan_data.csv')  # where the data file or URL can be inputed.
datafl.head()

# Capture DataFrame info
buffer = io.StringIO()
datafl.info(buf=buffer)
info_str = buffer.getvalue()

# Parse the info string into a structured format
info_lines = info_str.split('\n')
info_data = []

# Total number of entries in the DataFrame
total_count = len(datafl)

# Extracting relevant lines (ignoring empty lines)
for line in info_lines[3:-2]:  # Skip the first three lines and last two lines (memory usage)
    if line.strip():  # Ignore empty lines
        parts = line.split()
        
# Check for the redundant header-like line and skip it
        if len(parts) < 5 or parts[0] == '#':  # Assuming '#' is at the start of the redundant row
            continue

        # Extracting column number, column name, non-null count, and dtype
        column_number = parts[0]  # The first part is the column index (number)
        column_name = parts[1]  # Use the parts except the first and last three for column name
        non_null_count = parts[-2]  # Second last part is non-null count
        dtype = parts[-1]  # Last part is dtype

        # Append in desired order: Column #, Column Name, Non-Null Count, Count, Dtype
        info_data.append([column_number, column_name, non_null_count, total_count, dtype])

# Create a table with headers in the desired order
headers = ["Column #", "Column Name", "Non-Null Count", "Count", "Dtype"]

# Print the tabulated info with specified column order
print ("DataFile Info\n")
print(tabulate(info_data, headers=headers, tablefmt='grid'))


# Grouping data by a specified column (e.g., 'Category'), here I chose Loan status,
datafl.isnull().sum()
grouped_data = datafl.groupby('loan_status').sum().reset_index()

# which provides summary statistics of the DataFrame

# This will limit the statistical summary to only the columns we specify, 
# rather than summarizing all numeric columns in the DataFrame.
# #Count: Total number of non-null values in the column.
# Mean: Average value of the column.
# Standard Deviation (std): Measure of the column's spread or variability.
# Minimum (min): Smallest value in the column.
# 25% (1st Quartile): Value below which 25% of the data falls.
# 50% (Median): Middle value of the data.
# 75% (3rd Quartile): Value below which 75% of the data falls.
# Maximum (max): Largest value in the column.

data_summary = datafl.describe()


data_summary = datafl[['person_age', 'person_income', 'loan_amnt', 'loan_int_rate', 'credit_score']].describe()
print("\ndata_summary\n")
print(tabulate(data_summary, headers='keys', tablefmt='grid'))

# Sorting the results in ascending order based on a specific numerical column.
# Extracting the mean row and converting it to a DataFrame
mean_values = data_summary.loc['mean'].reset_index()
mean_values.columns = ['Variable', 'Mean']  # Renaming columns for clarity

# Sorting by the Mean.
sorted_data_mean = mean_values.sort_values(by='Mean', ascending=True)

# Sort by 'std' to see columns ordered by their variability
# Extracting the standard deviation row and converting it to a DataFrame
std_values = data_summary.loc['std'].reset_index()
std_values.columns = ['Variable', 'Standard Deviation']  # Renaming columns for clarity

# Now sort by Standard Deviation
sorted_data_std = std_values.sort_values(by='Standard Deviation', ascending=True)

# Sort by loan interest rate in ascending order
low_interest_loans = datafl[['person_age', 'loan_int_rate', 'loan_amnt', 'credit_score']].sort_values(by='loan_int_rate', ascending=True).head()


# Displaying numerical values
# Displaying numerical values with tabulate for better readability
print("\nTrending Data ordered by the Averages:\n")
print(tabulate(sorted_data_mean, headers='keys', tablefmt='grid'))

print("\nStandard Deviation of Variables:\n")
print(tabulate(sorted_data_std, headers='keys', tablefmt='grid'))

print("\nLoans with Lowest Interest Rates:\n")
print(tabulate(low_interest_loans, headers='keys', tablefmt='grid'))

# Group by loan intent and calculate the average loan amount
average_loan_by_intent = datafl.groupby('loan_intent')['loan_amnt'].mean().reset_index()

# Define the Rasta color scheme
Jamaica_colors = ['#FFFF00', '#008000', '#000000']
rasta_colors = ['#FF0000', '#FFFF00', '#008000', '#000000']  # Red, Yellow, Green, Black 
blue_palette = ['#003366', '#00509E', '#0099CC', '#66B2FF', '#A3C1DA', '#4682B4', '#B2E0F6']


# Set up the figure size
plt.figure(figsize=(10, 6))

# Create a bar chart
sns.barplot(x='loan_intent', y='loan_amnt', data=average_loan_by_intent, palette=blue_palette)
plt.title('Average Loan Amount by Loan Intent')
plt.xlabel('Loan Intent')
plt.ylabel('Average Loan Amount')
plt.xticks(rotation=45)  # Rotate x labels for better readability

# Show the plot
plt.tight_layout()
plt.show()


# The bar chart of loan intent by loan amount reveals the distribution, central tendency, and 
# variability of loan amounts. It allows for easy identification of outliers and comparisons 
# across different loan purposes.
average_loan_amount = datafl.groupby('loan_intent')['loan_amnt'].mean().reset_index()

# Create the bar chart
plt.figure(figsize=(10, 6))
sns.barplot(data=average_loan_amount, x='loan_intent', y='loan_amnt', palette=blue_palette)
plt.title('Average Loan Amount by Loan Purpose')
plt.xlabel('Loan Purpose')
plt.ylabel('Average Loan Amount')
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()

# Calculate approval rate by home ownership status
approval_rate_by_ownership = datafl.groupby('person_home_ownership')['loan_status'].mean().sort_values()


# Bar chart of loan approval rate by home ownership status. This identifies trends and disparities.
# Provides insights for targeted marketing strategies and informed decision-making in lending practices.
plt.figure(figsize=(8, 5))
approval_rate_by_ownership.plot(kind='bar', color=blue_palette)
plt.title('Loan Approval Rate by Home Ownership Status')
plt.xlabel('Home Ownership Status')
plt.ylabel('Approval Rate')
plt.xticks(rotation=45)
plt.show()


""" 
# The bar chart of loan intent by loan amount reveals the distribution, central tendency, and 
# variability of loan amounts. It allows for easy identification of outliers and comparisons 
# across different loan purposes.
average_loan_amount = datafl.groupby('loan_intent')['loan_amnt'].mean().reset_index()

# Create the bar chart
plt.figure(figsize=(10, 6))
sns.barplot(data=average_loan_amount, x='loan_intent', y='loan_amnt', palette='viridis')
plt.title('Average Loan Amount by Loan Purpose')
plt.xlabel('Loan Purpose')
plt.ylabel('Average Loan Amount')
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()


# Sort by credit score for approved loans
approved_high_scores = datafl[datafl['loan_status'] == 1][['credit_score', 'loan_amnt', 'person_income']].sort_values(by='credit_score', ascending=False).head(10)
print("Top 10 Credit Scores with Approved Loans:")
print(approved_high_scores) 
"""