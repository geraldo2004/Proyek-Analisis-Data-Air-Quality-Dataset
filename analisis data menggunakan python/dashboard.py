import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set style for seaborn
sns.set(style='darkgrid')

# Load dataset from local file
LOCAL_DATA_PATH = "all_data.csv"  # Replace with your local file path

@st.cache
def load_data():
    # Load dataset
    data = pd.read_csv(LOCAL_DATA_PATH)
    
    # Create a datetime column
    data['date'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])
    
    # Drop unnecessary columns (but keep year, month, and day if needed later)
    data.drop(['hour', 'No'], axis=1, inplace=True)
    
    return data

data_df = load_data()

# Sidebar
st.sidebar.header("Air Quality Dashboard")
st.sidebar.subheader("Filter Data")
start_date = st.sidebar.date_input("Start Date", value=data_df['date'].min().date())
end_date = st.sidebar.date_input("End Date", value=data_df['date'].max().date())

# Filter data based on the selected date range
filtered_data = data_df[(data_df['date'] >= pd.Timestamp(start_date)) & (data_df['date'] <= pd.Timestamp(end_date))]

# Main Content
st.title("Air Quality and Weather Conditions Analysis")

# Display data
st.subheader("Dataset Overview")
st.dataframe(filtered_data.head())

# Correlation Analysis
st.subheader("Correlation Analysis")
weather_columns = ['TEMP', 'PRES', 'DEWP']
pollutants_columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

# Calculate correlation
correlation_matrix = filtered_data[weather_columns + pollutants_columns].corr()

st.write("Correlation Matrix")
st.dataframe(correlation_matrix)

# Heatmap
st.write("Heatmap of Correlation")
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
plt.title('Correlation between Air Quality and Weather Conditions')
st.pyplot(fig)

# Scatterplots
st.subheader("Scatterplots")
col1, col2, col3 = st.columns(3)

with col1:
    st.write("PM2.5 vs TEMP")
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_data, x='TEMP', y='PM2.5', ax=ax)
    ax.set_title("PM2.5 vs TEMP")
    st.pyplot(fig)

with col2:
    st.write("PM2.5 vs PRES")
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_data, x='PRES', y='PM2.5', ax=ax)
    ax.set_title("PM2.5 vs PRES")
    st.pyplot(fig)

with col3:
    st.write("PM2.5 vs DEWP")
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_data, x='DEWP', y='PM2.5', ax=ax)
    ax.set_title("PM2.5 vs DEWP")
    st.pyplot(fig)

# Seasonal Trends Analysis
# Ensure 'date' is the index
filtered_data.set_index('date', inplace=True)

# Resample the data by month and calculate the mean for each month
monthly_avg = filtered_data[['PM2.5', 'PM10', 'SO2', 'NO2', 'O3', 'CO']].resample('M').mean()

# Plot the seasonal trends of pollutants
st.subheader("Seasonal Trends Analysis")
fig, ax = plt.subplots(figsize=(12, 6))
monthly_avg.plot(ax=ax)
ax.set_title('Seasonal Trends in Pollution Levels (PM2.5, PM10, NO2, O3, SO2, CO)', fontsize=14)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Average Concentration', fontsize=12)
ax.legend(loc='upper right', fontsize=10)
st.pyplot(fig)

# Peak Hour Analysis
st.subheader("Peak Hour Analysis")

# Calculate the average pollution level for each hour across all pollutants
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
filtered_data['hour'] = filtered_data.index.hour  # Extract hour from datetime index
hourly_pollution = filtered_data.groupby('hour')[pollutants].mean().sum(axis=1)

# Find the peak hour
peak_hour = hourly_pollution.idxmax()

# Plot the hourly pollution data
fig, ax = plt.subplots(figsize=(12, 6))
hourly_pollution.plot(ax=ax)
ax.scatter(peak_hour, hourly_pollution.max(), color='red', label=f'Peak Hour: {peak_hour}')
ax.set_title('Peak Pollution Levels by Hour of Day', fontsize=14)
ax.set_xlabel('Hour of Day', fontsize=12)
ax.set_ylabel('Sum of Pollution Levels', fontsize=12)
ax.legend(loc='upper right', fontsize=10)

# Display plot in Streamlit
st.pyplot(fig)

# Display the peak hour and its pollution level
st.write(f"The peak hour for pollution is: {peak_hour}")
st.write(f"The pollution level at this time is: {hourly_pollution.max()}")

# Weather Conditions Impact on Air Quality (Predicting Poor Days)
st.subheader("Weather Conditions and Air Quality Prediction")

# Define weather-related features and the target 'Air_Quality'
features = ['TEMP', 'PRES', 'DEWP', 'WSPM']
# Target: 'Air_Quality' is mapped to 1 for Poor and 0 for Good
target = data_df['Air Quality'].apply(lambda x: 1 if x == 'Poor' else 0)

# Calculate correlation between weather features and air quality
correlations = data_df[features].corrwith(target)

# Display the correlations
st.write("Correlation between Weather Features and Air Quality:")
st.write(correlations)

# Plot the correlations
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=correlations.index, y=correlations.values, ax=ax, palette='coolwarm')
ax.set_title('Correlation between Weather Features and Air Quality', fontsize=14)
ax.set_xlabel('Weather Features', fontsize=12)
ax.set_ylabel('Correlation with Air Quality (Poor=1)', fontsize=12)
st.pyplot(fig)

# Interpretation of Weather Impact on Air Quality
st.write("""
### Interpretation of Weather Conditions Impact on Air Quality:
- **Temperature (TEMP)**: If the correlation is high, this means that temperature fluctuations are associated with changes in air quality.
- **Pressure (PRES)**: Similarly, pressure can play a role in atmospheric stability, impacting pollution dispersion.
- **Dew Point (DEWP)**: Dew point indicates moisture in the air, and high moisture can affect pollution accumulation.
- **Wind Speed (WSPM)**: Wind speed influences the dispersion of pollutants. High wind speeds tend to disperse pollutants, while low wind speeds can result in poor air quality.
""")
