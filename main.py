import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display
    
#process the raw pd calls for service file
servfile_path = r"C:\\Users\\elifp\\OneDrive\\Documents\\CSIT179\\Final Project\\Data Files\\pd_calls_for_service_2023_datasd_edited.csv"
df1 = pd.read_csv(servfile_path, usecols=['incident_num', 'Date', 'Time', 'call_type', 'disposition', 'beat','priority'])
df1.head(10)
    
#process calls,
callsfile_path = r"C:\\Users\\elifp\\OneDrive\\Documents\\CSIT179\\Final Project\\Data Files\\pd_cfs_calltypes_datasd.csv"
df2 = pd.read_csv(callsfile_path, usecols=['call_type', 'description'])
df2.head(10)
    
#Process beats to neighborhoods,
beatsfile_path = r"C:\\Users\\elifp\\OneDrive\\Documents\\CSIT179\\Final Project\\Data Files\\pd_beat_codes_list_Datasd.csv"
df3 = pd.read_csv(beatsfile_path, usecols=['beat', 'neighborhood'])
df3.head(10)

#process disposition
dispo_path = r"C:\\Users\\elifp\\OneDrive\\Documents\\CSIT179\\Final Project\\Data Files\\pd_dispo_codes_datasd.csv"
df4 = pd.read_csv(dispo_path)
df4.head(10)

  
#combine
df5 = df1.merge(df2, how = 'left', on='call_type') #merge raw pd with processed call codes
df6 = df5.merge(df3, how='left', on='beat') #merge the new merged raw pd file with call codes to beats file

#rename the description column since we are pulling in another file that also has a column called 'description'
df6.rename(columns={'description': 'call_description'}, inplace=True)

df7 = df6.merge(df4, how = 'left', left_on = 'disposition', right_on = 'dispo_code')


#rename the description column again
df7.rename(columns={'description': 'disposition_description'}, inplace=True)

#Drop Nulls
df7.dropna(subset=['neighborhood'], inplace=True)

df7 = df7.drop(labels=['call_type', 'disposition', 'dispo_code'], axis=1)


# if you want to save your newly merged file remove the '#'
#df7.to_csv('C:\\Users\\elifp\\OneDrive\\Documents\\CSIT179\\Final Project\\Data Files\\merged_servicecalls.csv')
pass

#narrow down data to arrests only; remove duplicates
df8 = arrest_made_data = df7[df7['disposition_description'] == 'ARREST MADE'].dropna()
df8 = arrest_made_data.drop_duplicates()
display (df8)

# Create a list of neighborhoods and the number of calls they had in total
df9 = neighborhood_totalcalls = arrest_made_data['neighborhood'].value_counts().reset_index()
df9.columns = ['neighborhood', 'total_calls']
df9 = df9.sort_values('total_calls', ascending=False)
df10 = df9.head(10)


# Plot the data: total calls by neighborhood in 2023
plt.figure(figsize=(10, 5))
plt.bar(df10['neighborhood'], df10['total_calls'])
plt.grid(linestyle='--')
plt.xlabel('Neighborhood', fontsize='12')
plt.ylabel('Total Calls', fontsize='12')
plt.title('Total Calls by Neighborhood in 2023')
plt.xticks(rotation=90)
plt.show()

# Define the list of neighborhoods
neighborhoods = ['East Village', 'Pacific Beach', 'Gaslamp', 'Midway District', 'Core-Columbia', 'San Ysidro', 'Mission Valley East', 
                 'Hillcrest', 'Ocean Beach', 'North Park']
                 
# Filter the data for the specified neighborhoods
filtered_data = df8[df8['neighborhood'].isin(neighborhoods)]

# Group the filtered data by call_description and calculate the count
grouped_data = filtered_data.groupby('call_description').size().reset_index(name='count')

# Sort the grouped data by count in descending order
grouped_data = grouped_data.sort_values('count', ascending=False)

# Take the top 10 highest number of calls per call_description
top_10_calls = grouped_data.head(10)

# Plot a pie chart for each neighborhood
for neighborhood in neighborhoods:
    filtered_data_neighborhood = filtered_data[filtered_data['neighborhood'] == neighborhood]
    grouped_data_neighborhood = filtered_data_neighborhood.groupby('call_description').size().reset_index(name='count')
    grouped_data_neighborhood = grouped_data_neighborhood.sort_values('count', ascending=False)
    top_10_calls_neighborhood = grouped_data_neighborhood.head(10)
    
plt.figure(figsize=(8, 8))
plt.pie(top_10_calls_neighborhood['count'], labels=top_10_calls_neighborhood['call_description'], autopct='%1.1f%%')
plt.title(f'Top 10 Call Descriptions in {neighborhood}',fontweight='bold')
plt.show()
    

