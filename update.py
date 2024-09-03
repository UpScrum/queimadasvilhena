import json
import requests
import geopandas as gpd
from shapely.geometry import shape

URL = "https://dataserver-coids.inpe.br/queimadas/queimadas/focos/kml/estados-48h/focos_frentes_RO.kml"
FILENAME = "focos_frentes_RO.kml"
VILHENA_POLYGON = "vilhena.geojson"

def download_file(url, filename):
    # Download the file
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully and saved as {filename}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

def main():
    download_file(URL, FILENAME)
    # Load the GeoJSON file
    with open(VILHENA_POLYGON, 'r') as f:
        geojson_data = json.load(f)
        # Convert the GeoJSON geometry to a shapely geometry object
        vilhena_polygon = shape(geojson_data['features'][0]['geometry'])
    gdf = gpd.read_file(FILENAME, driver='KML')
    points_inside_vilhena = gdf[gdf.geometry.apply(lambda x: vilhena_polygon.contains(x))]
    points_inside_vilhena.to_file('points.kml', driver='KML')


if __name__ == "__main__":
    main()
