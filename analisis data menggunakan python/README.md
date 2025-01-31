# Air Quality and Weather Conditions Dashboard - Geraldo Tan M102B4KY1598

This project is a Streamlit dashboard that visualizes air quality and weather conditions over time. It provides various analyses, such as correlation analysis, seasonal trends, peak hour analysis, and the relationship between weather features and air quality.

## Features

- **Interactive Dashboard**: Allows filtering of air quality data by date range.
- **Correlation Analysis**: Displays a heatmap of correlations between air quality and weather conditions (e.g., temperature, pressure, dew point).
- **Scatter Plots**: Visualizes relationships between pollutants (e.g., PM2.5) and weather features (e.g., temperature).
- **Seasonal Trends**: Shows the seasonal trends in pollution levels.
- **Peak Hour Analysis**: Identifies the hour of the day with the highest pollution levels.
- **Weather Conditions Impact on Air Quality**: Analyzes the correlation between weather features and air quality, predicting poor air quality days based on weather conditions.

## Setup Environment
pip install numpy pandas matplotlib seaborn jupyter streamlit babel

## Run steamlit app
streamlit run dashboard.py