# Import necessary libraries
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Housing Price Analysis",
    page_icon="🏠",
)

# Apply custom CSS to style your app
st.write(
    """
    <style>
    body {
        font-family: poppins;
    }
    .stApp {
        max-width: 100%;
        margin: 0 auto;
    }
    .stHeader {
        font-size: 36px;
        color: #333;
    }
    .stMarkdown {
        font-size: 18px;
        color: #555;
    }
    .stButton>button {
        background-color: #009688;
        color: white;
        border: none;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #00736c;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.title('Data Science Project')
st.subheader('Housing Price Analysis')

# =====================Introduction====================='''
st.header('Introduction')
st.write('''
The motivation behind the project is to understand the dynamics of housing prices in the current real estate market, particularly in the context of changing socio-economic factors and the impact of recent events on property values.
''')

# =====================Project Objective====================='''
st.header('Project Objective')
st.write('''
View the dataset and perform data cleaning, data analysis, and data visualization to answer the following questions:
1. How do house prices vary by the number of bedrooms?
2. How do house prices vary by the number of bathrooms?
3. How do house prices vary by the presence of a basement?
4. How do house prices vary by the presence of air conditioning?
5. How do house prices vary by the presence of a guest room?
''')

# =====================Dataset Description====================='''
st.header('Dataset Description')

st.write('''
The dataset contains various features related to housing such as price, area, number of bedrooms, number of bathrooms, stories, and more. It provides a comprehensive overview of different aspects of housing data, allowing for analysis and exploration of housing prices and the factors influencing them.
''', unsafe_allow_html=True)

st.markdown(
    """
    <style>
        .stMarkdown {
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================Load Dataset====================='''
df = pd.read_csv('./Data/Housing.csv')
st.header('Dataset')
st.write(df)

# =====================Data Cleaning====================='''
st.header('Data Cleaning')

# Keep the required columns
selected_columns = ['price', 'area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom',
                    'basement', 'hotwaterheating', 'airconditioning', 'parking', 'furnishingstatus']
df_cleaned = df[selected_columns]

# Convert 'yes' and 'no' values to 1 and 0
binary_columns = ['mainroad', 'guestroom',
                  'basement', 'hotwaterheating', 'airconditioning']
df_cleaned[binary_columns] = df_cleaned[binary_columns].applymap(
    lambda x: 1 if x == 'yes' else 0)

# Drop the 'furnishingstatus' column
df_cleaned = df_cleaned.drop(columns=['furnishingstatus'])

# Display the cleaned dataset using st.dataframe()
st.dataframe(df_cleaned)

# ================Descriptive Statistics==================``'
st.header('Descriptive Statistics')

# Display basic statistics for numeric columns rounded to 2 decimal places
st.write(df_cleaned.describe().round(2))

# Data Analysis
st.header('Data Analysis')

# Calculate mean price with and without a basement
mean_price_with_basement = df_cleaned[df_cleaned['basement'] == 1]['price'].mean()
mean_price_without_basement = df_cleaned[df_cleaned['basement'] == 0]['price'].mean()

# Display the results
st.write("Mean Price with Basement:", mean_price_with_basement.round(2))
st.write("Mean Price without Basement:", mean_price_without_basement.round(2))

# Calculate mean price with and without air conditioning
mean_price_with_ac = df_cleaned[df_cleaned['airconditioning']
                                == 1]['price'].mean()
mean_price_without_ac = df_cleaned[df_cleaned['airconditioning'] == 0]['price'].mean()

# Display the results
st.write("Mean Price with Air Conditioning:", mean_price_with_ac.round(2))
st.write("Mean Price without Air Conditioning:",
         mean_price_without_ac.round(2))

# Calculate mean price with and without a guest room
mean_price_with_guestroom = df_cleaned[df_cleaned['guestroom'] == 1]['price'].mean()
mean_price_without_guestroom = df_cleaned[df_cleaned['guestroom'] == 0]['price'].mean()

# Display the results
st.write("Mean Price with Guest Room:", mean_price_with_guestroom.round(2))
st.write("Mean Price without Guest Room:",
         mean_price_without_guestroom.round(2))

# =====================Data Visualization====================='''
st.header('Data Visualization')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Line Graph for House Prices by Number of Bedrooms
st.subheader('Line Graph of House Prices by Number of Bedrooms')

# Group the data by 'bedrooms' and calculate the mean price
bedroom_prices = df_cleaned.groupby('bedrooms')['price'].mean()

plt.figure(figsize=(10, 6))
sns.lineplot(x=bedroom_prices.index, y=bedroom_prices.values)
plt.xlabel('Number of Bedrooms')
plt.ylabel('Mean Price (in millions USD)')
plt.title('Line Graph of House Prices by Number of Bedrooms')

# Format the y-axis labels as currency values in millions of USD
plt.gca().get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, loc: "${:,.2f}M".format(x/1000000)))
st.pyplot()

# Line Graph for House Prices by Number of Bathrooms (rounded)
st.subheader('Line Graph of House Prices by Number of Bathrooms (Rounded)')

# Round the 'bathrooms' column
df_cleaned['bathrooms_rounded'] = df_cleaned['bathrooms'].round()

# Group the data by 'bathrooms_rounded' and calculate the mean price
bathroom_prices = df_cleaned.groupby('bathrooms_rounded')['price'].mean()

plt.figure(figsize=(10, 6))
sns.lineplot(x=bathroom_prices.index, y=bathroom_prices.values)
plt.xlabel('Number of Bathrooms (Rounded)')
plt.ylabel('Mean Price (in millions USD)')
plt.title('Line Graph of House Prices by Number of Bathrooms (Rounded)')

# Format the y-axis labels as currency values in millions of USD
plt.gca().get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, loc: "${:,.2f}M".format(x/1000000)))
st.pyplot()

# =====================Data Wrangling====================
st.header('Data Wrangling')
st.write('''
Handling missing values in the 'area' column by replacing them with the column's median value.
''')

# Replace missing values in 'area' with median value
df_cleaned['area'].fillna(df_cleaned['area'].median(), inplace=True)

# Display updated dataset after handling missing values
st.dataframe(df_cleaned)

# ====================Data Aggregation - Mean price based on number of stories====================
st.header('Data Aggregation')
st.write('''
Calculating the mean price based on the number of stories in the houses.
''')

mean_price_stories = df_cleaned.groupby('stories')['price'].mean()

# Display the results
st.write("Mean Price based on Number of Stories:")
st.dataframe(mean_price_stories)