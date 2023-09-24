import streamlit as st
import pandas as pd
import plotly.express as px

# Read the data
file_path = '/Users/karen/Desktop/world-data-2023.csv'
data = pd.read_csv(file_path)
st.title('Global Data Explorer: Visualizing Population, Forested Area, and CO2 Emissions by Country')

# Remove the percentage sign and convert to float for "Forested Area" and "CO2 Emissions"
data["Forested Area (%)"] = data["Forested Area (%)"].str.replace('%', '', regex=True).astype(float)
data["Co2-Emissions"] = data["Co2-Emissions"].str.replace(',', '', regex=True).astype(float)
# Remove commas from the "Population" column and convert it to float
data["Population"] = data["Population"].str.replace(',', '', regex=True).astype(float)
# Remove commas from the "Urban_population" column and convert it to float
data["Urban_population"] = data["Urban_population"].str.replace(',', '', regex=True).astype(float)

# Rename the "Co2-Emissions" column to remove hyphen
data.rename(columns={"Co2-Emissions": "Co2Emissions"}, inplace=True)

# Create a sidebar for customization
st.sidebar.header('Customization')

# Add a dropdown to select the metric
selected_metric = st.sidebar.selectbox(
    'Select a Metric to Visualize',
    ['Population', 'Forested Area (%)', 'CO2 Emissions']  # "Population" is the first option
)

# Add text areas for additional customization
if selected_metric == 'Population':
    st.sidebar.text_area('App Features:', 'On this page, you can explore population data by country and tailor the map to your preferences by filtering based on population size. Below the map, you will find a convenient dropdown menu that allows you to select a specific country. This feature enables you to visualize the geographical location of the selected country on the world map and access a wealth of diverse information about it. At the bottom of the page, a bar chart is shown which allows you to quickly compare the urban populations of the top 15 countries, with additional information about their total populations displayed in the hover box when you interact with the chart.')
elif selected_metric == 'Forested Area (%)':
    st.sidebar.text_area('App Features:', 'On this page, you can explore the forested area percentages by country and fine-tune the map by applying various percentage filters. Beneath the map, you will discover a dropdown menu that enables you to pick a country, allowing you to visualize its geographical location on the world map and access a wealth of diverse information about it.')
elif selected_metric == 'CO2 Emissions':
    st.sidebar.text_area('App Features:', 'On this page, you can explore the CO2 emission percentages by country and refine the map display by adjusting percentage filters. Below the map, you will find a dropdown menu that allows you to select a country, enabling you to visualize its geographical location on the world map and access various informative details about it')

# Create the choropleth map based on the selected metric
if selected_metric == 'Population':
    title = 'Population by Country'
    color_column = 'Population'
    color_scale = ["lightblue", "purple"]
elif selected_metric == 'Forested Area (%)':
    title = 'Forested Area Percentage by Country'
    color_column = 'Forested Area (%)'
    color_scale = ["yellow", "green"]
elif selected_metric == 'CO2 Emissions':
    title = 'CO2 Emissions by Country'
    color_column = 'Co2Emissions'
    color_scale = ["lightblue", "pink"]

# Filter data based on the selected metric
filtered_data = data.copy()
if selected_metric == 'Population':
    min_population = min(data["Population"])
    max_population = max(data["Population"])
    filter_threshold = st.sidebar.slider(
        "Filter by Population:",
        min_value=min_population,
        max_value=max_population,
    )
    filtered_data = data[data["Population"] >= filter_threshold]
elif selected_metric == 'Forested Area (%)':
    min_percentage = min(data["Forested Area (%)"])
    max_percentage = max(data["Forested Area (%)"])
    filter_threshold = st.sidebar.slider(
        "Filter by Forested Area Percentage:",
        min_value=min_percentage,
        max_value=max_percentage,
    )
    filtered_data = data[data["Forested Area (%)"] >= filter_threshold]
elif selected_metric == 'CO2 Emissions':
    min_co2 = min(data["Co2Emissions"])
    max_co2 = max(data["Co2Emissions"])
    filter_threshold = st.sidebar.slider(
        "Filter by CO2 Emissions:",
        min_value=min_co2,
        max_value=max_co2,
    )
    filtered_data = data[data["Co2Emissions"] >= filter_threshold]

# Create the choropleth map
fig = px.choropleth(
    filtered_data,
    locations="Country",
    locationmode="country names",
    color=color_column,
    color_continuous_scale=color_scale,
    hover_name="Country",
    title=title,
)

# Set the color bar title
fig.update_coloraxes(colorbar_title=selected_metric)


# Display the choropleth map
st.plotly_chart(fig)


# Add a dropdown to select a country
selected_country = st.selectbox("Select a country to highlight", data["Country"])

# Filter the data for the selected country
highlighted_data = data[data["Country"] == selected_country]

# Create a scatter plot to highlight the selected country
fig_highlight = px.scatter_geo(
    highlighted_data,
    locations="Country",
    locationmode="country names",
    title=f"Highlighted Country: {selected_country}",
    color_discrete_sequence=["red"],
)

# Set marker size and opacity
fig_highlight.update_traces(marker=dict(size=10, opacity=0.7))

# Display the scatter plot to highlight the selected country
st.plotly_chart(fig_highlight)

country_data = highlighted_data if not highlighted_data.empty else data[data['Country'] == selected_country]

if country_data.empty:
    st.write('No data available for the selected country.')
else:
    st.write('Data for Selected Country:', selected_country)
    st.table(country_data)

# Create a bar chart for "Population" at the bottom of the page
if selected_metric == 'Population':
    # Sort the DataFrame by 'Urban_population' in descending order
    top_15_df = data.sort_values(by='Urban_population', ascending=False).head(15)

    # Round the 'Population' column to millions and format it with "M" at the end
    top_15_df['Population'] = top_15_df['Population'] / 1000000
    top_15_df['Population'] = top_15_df['Population'].apply(lambda x: f'{x:.2f}M')

    # Create the bar chart
    fig_bar = px.bar(top_15_df,
                     x='Country',
                     y='Urban_population',
                     title='Top 15 Countries with Urban Population',
                     labels={'Urban_population': 'Urban Population'},
                     hover_data={'Population': True},
                     height=600)

    # Customize the layout
    fig_bar.update_xaxes(title='Country')
    fig_bar.update_yaxes(title='Urban Population')
    fig_bar.update_traces(marker_color='blue')  # Change the bar color

    # Display the bar chart at the bottom of the page
    st.plotly_chart(fig_bar)



