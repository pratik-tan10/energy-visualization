import os
import requests
import geopandas as gpd

# URL for the energy infrastructure data of North America
url = "https://geoappext.nrcan.gc.ca/arcgis/rest/services/NACEI/energy_infrastructure_of_north_america_en/MapServer/15/query"

# Parameters for the data query
params = {
    "where": "OBJECTID >= 0", # To obtain all the rows
    "geometryType": "esriGeometryEnvelope",
    "spatialRel": "esriSpatialRelIntersects",
    "outFields": "OBJECTID, SHAPE, Country, Facility, Owner, Operator, Latitude, Longitude, City, County, StateProv, ZipCode, Address, Total_MW, Renew_MW, PrimSource, PrimRenew, Coal_MW, NG_MW, Crude_MW, Other_MW, Hydro_MW, HydroPS_MW, Nuclear_MW, Solar_MW, Wind_MW, Geo_MW, Bio_MW, Tidal_MW, Source, Period",
    "returnGeometry": "true",
    "f": "geojson"
}

def download():
    """
    Ddownloads the energy infrastructure data of North America from the given URL and saves it as a GeoJSON file.
    """
    # Check if the data file already exists
    if not os.path.exists('data.geojson'):
        # Send a GET request to the URL with the given parameters
        response = requests.get(url, params=params)
        # Load the response data as JSON
        data = response.json()

        # Convert JSON data to GeoDataFrame
        gdf = gpd.GeoDataFrame.from_features(data["features"])

        # Save the GeoDataFrame as a GeoJSON file
        gdf.to_file('data.geojson', driver='GeoJSON')