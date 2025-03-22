# Bike Sharing Dashboard 🚲

## Project Overview

This interactive dashboard analyzes bike sharing data to answer key business questions about usage patterns, seasonal trends, and weather impacts. The analysis focuses on:

1. Comparing bike usage between 2011 and 2012 to identify growth factors beyond seasonal weather
2. Analyzing how extreme weather affects casual vs. registered users differently

## Setup Environment - Anaconda

```
conda create --name bike-dashboard python=3.9
conda activate bike-dashboard
<<<<<<< HEAD
pip install streamlit pandas matplotlib plotly
=======
pip install streamlit pandas matplotlib numpy tabulate plotly
>>>>>>> 5341f7d399a91be6eca67b16f453e9a0cbe17459
```

## Setup Environment - Shell/Terminal

```
mkdir bike_sharing_dashboard
cd bike_sharing_dashboard
pipenv install
pipenv shell
pip install streamlit pandas matplotlib numpy tabulate plotly
```

## Run Streamlit app

```
cd dashboard
streamlit run dashboard.py
```

## Dashboard Features

-   **Multi-page navigation**: Introduction, Data Overview, Analysis Q1, Analysis Q2, Conclusion
-   **Interactive visualizations**: Data exploration with Plotly charts and toggleable insights
-   **Year-over-year analysis**: Visualizing 2011 vs. 2012 rental patterns
-   **Weather impact comparison**: Analyzing how weather affects different user segments
-   **Business recommendations**: Data-driven strategies based on findings

## Key Insights

-   **Consistent growth**: The 2012 data shows higher usage across all months compared to 2011
-   **Seasonal patterns**: Both years show similar seasonal trends but with 2012 consistently outperforming
-   **Weather sensitivity**: Casual users are more affected by adverse weather than registered users
-   **User behavior**: Registered users show more consistent usage patterns across different conditions

## Data Requirements

Place these files in the same directory as dashboard.py:

-   day.csv
-   hour.csv

## Author

**aksalatdev**
