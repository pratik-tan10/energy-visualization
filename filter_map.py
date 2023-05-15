import streamlit as st
import folium
import geopandas as gpd

import download_gdf
import make_map

numeric_fields = ['Total_MW',
 'Renew_MW',
 'Coal_MW',
 'NG_MW',
 'Crude_MW',
 'Other_MW',
 'Hydro_MW',
 'HydroPS_MW',
 'Nuclear_MW',
 'Solar_MW',
 'Wind_MW',
 'Geo_MW',
 'Bio_MW',
 'Tidal_MW'
 ]
 
categorical_fields = {'Country':'Country',
 'Primary Source': 'PrimSource',
 'Primary Renewable Source': 'PrimRenew'
 }
 
# Download the data
download_gdf.download()

# Load the data and create the GeoDataFrame
gdf = gpd.read_file('data.geojson')

# Create a Streamlit app
st.set_page_config(layout="wide")

# Add a custom CSS style to remove the top padding
st.markdown("""
    <style>
        .reportview-container .main .block-container {
            padding-top: 10;
        }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col2:
    
    # Create a color legend HTML string
    legend_html = """
        <div class="leaflet-control-layers-expanded" style=" z-index: 9999;
                    background-color: rgba(255, 255, 255, 0.8); border-radius: 6px;
                    border: 1px solid grey; padding: 10px; font-size: 14px;">
            <h3 style="text-align: center;">Legend</h3>
            <p style="text-align: center; margin-bottom: 5px;"><strong>Primary Fuel Source</strong></p>
            """
    for source, color in make_map.fuel_colors.items():
        legend_html += f"""
            <p style="margin-left: 10px;">
                <span style="background-color:{color}; width:10px; height:10px; display: inline-block;"></span> {source}
            </p>
            """
    legend_html += "</div>"

    # Embed the legend in a Streamlit component
    st.components.v1.html(f"""
        <div style="margin-top: 70px; width: 100%; border: 2px solid #005366;">
            {legend_html}
        </div>
    """, height = 530)
    
    # Display the dropdown for selecting the filter variable
    filter_variable = st.selectbox("Select filter variable", categorical_fields.keys())
    filter_variable =  categorical_fields[filter_variable]

    # Get the unique values for the selected filter variable
    unique_values = gdf[filter_variable].unique()

    # Display the checkboxes for the unique values
    selected_values = []
    for value in unique_values:
        if st.checkbox(value, value=True):
            selected_values.append(value)

            
with col1:
    st.title("Energy Generation Distribution Visualization")

    # Create the map
    m = make_map.get_map(filter_variable, selected_values)
    # Get the HTML representation of the map
    map_html = m._repr_html_()
    
    # Embed the map HTML in a Streamlit component
    st.components.v1.html(f"""
        <div style="width: 100%; border: 2px solid #005366;">
            {map_html}
        </div>
    """, height = 720)
    
    # Define the URLs of your LinkedIn and GitHub profiles
    linkedin_url = "https://www.linkedin.com/in/pratikdh"
    github_url = "https://github.com/pratik-tan10"

    # Add the Bootstrap Icons CSS file to the Streamlit app
    st.markdown("""
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css">
    """, unsafe_allow_html=True)

    # Display the LinkedIn and GitHub logos with links to your profiles
    st.markdown(f"""
        <style>
            .contact-icon {{
                font-size: 24px;
                margin-right: 10px;
            }}
        </style>
        <div style="display:inline; text-align:left; width:50%;"><a href="{linkedin_url}" target="_blank">
            <i class="bi bi-linkedin contact-icon"></i>
            Pratik dhungana: LinkedIn
        </a></div>
        <div style="display:inline; text-align:right; width:50%;"><a href="{github_url}" target="_blank">
            <i class="bi bi-github contact-icon"></i>
            Pratik Dhungana: GitHub
        </a></div>
    """, unsafe_allow_html=True)