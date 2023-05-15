import download_gdf
import folium
import geopandas as gpd

# Download the data
download_gdf.download()

# Read the saved GeoJSON file
gdf0 = gpd.read_file('data.geojson')

fuel_colors = {
    "Hydroelectric": "#a5c732",
    "Natural Gas": "#ed7711",
    "Wind": "#00cc00",
    "Petroleum": "#663300",
    "Geothermal": "#ff6600",
    "Coal": "#ed9cf1",
    "Nuclear": "#ede411",
    "Solar": "#ffff00",
    "Other": "#999999",
    "Biomass": "#996633",
    "Pumped Storage": "#b3d9ff"
}
    
def get_map(filter_variable, selected_values, save = False):
    """
    Generate a Folium map with filtered data and customized markers.

    Parameters:
        - filter_variable (str): The name of the categorical variable used for filtering.
        - selected_values (list): The selected values of the filter_variable to include in the map.
        - save (bool): Whether to save the map as an HTML file.

    Returns:
        - m (folium.Map): The generated Folium map.
    """
    try:
        # Filter the data based on the selected filter values
        gdf = gdf0[gdf0[filter_variable].isin(selected_values)]
        
        # Sort the GeoDataFrame in ascending order based on Total_MW
        gdf = gdf.sort_values("Total_MW", ascending = False)

        # Set the CRS of the GeoDataFrame
        gdf.crs = "EPSG:4326"

        # Get the total spatial extent of the data
        bounds = gdf.total_bounds

        # Create a Folium map centered at a specific location
        m = folium.Map(location=[gdf["geometry"].centroid.y.mean(), gdf["geometry"].centroid.x.mean()],
                        zoom_start=4, min_zoom=3, max_zoom=7, 
                        max_bounds=[(bounds[3], bounds[0]), (bounds[1], bounds[2])])

        # Add the US Imagery tile layer to the map
        usgs_basemap = 'https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}'
        folium.TileLayer(usgs_basemap, name="USGS US Imagery", attr="USGS US Imagery").add_to(m)

        # Calculate the bounds of the GeoDataFrame
        bounds = gdf.total_bounds

        # Define the style function for the GeoJSON layer
        def style_function(feature):
            return {
                "fillOpacity": 0.2,
                "weight": 0,
                "radius": feature["properties"]["Total_MW"] * 0.002,  # Adjust the scaling factor to control marker size
                "fillColor": get_color(feature["properties"]["PrimSource"]),
                "color": "black",
            }

        # Add each point from the GeoDataFrame as a circle marker to the map
        for _, row in gdf.iterrows():
            folium.CircleMarker(
                location=[row["geometry"].y, row["geometry"].x],
                radius=row["Total_MW"] * 0.006,  # Adjust the scaling factor to control marker size
                fill=True,
                fill_opacity=0.8,
                fill_color=fuel_colors[row["PrimSource"]],
                color=None,
                tooltip=f'''{row["StateProv"]}:<br>{row["PrimSource"]}: {row["Total_MW"]} MW''',
            ).add_to(m)

        # Save the map if 'save' = True
        if save:
            m.save('map.html')
        # Display the map
        return m
    
    except:
        m = folium.Map(location=[gdf0["geometry"].centroid.y.mean(), gdf0["geometry"].centroid.x.mean()], zoom_start=4)
        return m