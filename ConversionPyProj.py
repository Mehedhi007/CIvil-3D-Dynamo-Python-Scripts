import pyproj
import sys
import json

try:
    # Get input easting and northing lists from command-line arguments (assuming they are passed as JSON strings)
    easting_list = json.loads(sys.argv[1])
    northing_list = json.loads(sys.argv[2])
    object_id_list = json.loads(sys.argv[3])
    epsg_code = sys.argv[4]

    # Define the projection for the provided EPSG code
    proj_utm = pyproj.CRS(f'epsg:{epsg_code}')  # User-defined EPSG code

    # Define the projection for WGS84 (latitude and longitude)
    proj_latlon = pyproj.CRS('epsg:4326')  # EPSG:4326 is the code for WGS84

    # Create a transformer object to convert from the user-defined EPSG to WGS84
    transformer = pyproj.Transformer.from_crs(proj_utm, proj_latlon)

    # Check if the lists are of the same length
    if len(easting_list) != len(northing_list) or len(easting_list) != len(object_id_list):
        print("Error: The easting, northing, and object ID lists must have the same length.", file=sys.stderr)
        sys.exit(1)

    results = []

    # Iterate over the lists and transform each pair of coordinates
    for easting, northing, object_id in zip(easting_list, northing_list, object_id_list):
        latitude, longitude = transformer.transform(easting, northing)
        results.append((object_id, round(latitude, 4), round(longitude, 4)))

    # Output the results as JSON
    output_json = json.dumps(results)
    print(output_json)

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
