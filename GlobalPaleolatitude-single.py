import pygplates
import pandas as pd

# Input files and paths
input_csv = 'Global.csv'  # CSV file containing sample coordinates, plate IDs, and ages
rotation_model_path = '1000_0_rotfile_Merdith_et_al.rot'  # Rotation model from Merdith et al. (2021)
plate_boundary_file = 'shapes_continents_Merdith_et_al.gpmlz'  # Continental geometries; loaded for consistency with the original workflow

# Output file path
output_csv = 'output_latitude_reconstruction.csv'

# Load the rotation model
try:
    rotation_model = pygplates.RotationModel(rotation_model_path)
    print("Rotation model loaded successfully.")
except Exception as e:
    print(f"Failed to load the rotation model: {e}")
    exit(1)

# Load the continental geometry file
try:
    static_polygons = pygplates.FeatureCollection(plate_boundary_file)
    print("Continental geometry file loaded successfully.")
except Exception as e:
    print(f"Failed to load the continental geometry file: {e}")
    exit(1)

# Load the input CSV file
try:
    data = pd.read_csv(input_csv)
    print("Input CSV file loaded successfully.")
except Exception as e:
    print(f"Failed to load the input CSV file: {e}")
    exit(1)

# Check the required columns
required_columns = {'ID', 'Latitude', 'Longitude', 'Plate_ID', 'Age'}
if not required_columns.issubset(data.columns):
    print(f"The input CSV file is missing required columns: {required_columns - set(data.columns)}")
    exit(1)

# Prepare containers for reconstruction results and invalid records
results = []
invalid_points = []

# Process each input point
for index, row in data.iterrows():
    point_id = row['ID']
    latitude = row['Latitude']
    longitude = row['Longitude']
    plate_id = row['Plate_ID']
    age = row['Age']  # Reconstruct each point at the age specified in this column
    
    # Check the latitude and longitude ranges
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        invalid_points.append({
            'ID': point_id,
            'Latitude': latitude,
            'Longitude': longitude,
            'Age': age,
            'Error': 'Invalid Latitude or Longitude'
        })
        print(f"Validation failed for point ID {point_id}: latitude={latitude}, longitude={longitude}")
        continue
    
    # Create a PointOnSphere object
    try:
        point_geometry = pygplates.PointOnSphere(latitude, longitude)
    except Exception as e:
        invalid_points.append({
            'ID': point_id,
            'Latitude': latitude,
            'Longitude': longitude,
            'Age': age,
            'Error': f'Invalid Geometry: {e}'
        })
        print(f"Failed to create PointOnSphere for point ID {point_id}: {e}")
        continue
    
    # Create a feature and assign its reconstruction plate ID
    try:
        point_feature = pygplates.Feature()
        point_feature.set_geometry(point_geometry)
        point_feature.set_reconstruction_plate_id(int(plate_id))  # Use the plate ID supplied in the input CSV
    except Exception as e:
        invalid_points.append({
            'ID': point_id,
            'Latitude': latitude,
            'Longitude': longitude,
            'Age': age,
            'Error': f'Feature Creation Failed: {e}'
        })
        print(f"Failed to create a feature for point ID {point_id}: {e}")
        continue
    
    # Reconstruct this point at its individual age
    reconstructed_geometries = []  # Store the reconstructed feature geometries
    
    try:
        pygplates.reconstruct([point_feature], rotation_model, reconstructed_geometries, age)
        print(f"Point ID {point_id} reconstructed successfully at {age} Ma.")
    except Exception as e:
        invalid_points.append({
            'ID': point_id,
            'Latitude': latitude,
            'Longitude': longitude,
            'Age': age,
            'Error': f'Reconstruction Failed at {age} Ma: {e}'
        })
        print(f"Reconstruction failed for point ID {point_id} at {age} Ma: {e}")
        continue  # Skip this point

    # Extract coordinates if a reconstructed geometry is available
    if reconstructed_geometries:
        try:
            # Retrieve the reconstructed geometry
            reconstructed_geometry = reconstructed_geometries[0].get_reconstructed_geometry()
            reconstructed_lat, reconstructed_lon = reconstructed_geometry.to_lat_lon()
            results.append({
                'ID': point_id,
                'Original_Latitude': latitude,
                'Original_Longitude': longitude,
                'Plate_ID': plate_id,
                'Age': age,
                'Reconstructed_Latitude': reconstructed_lat,
                'Reconstructed_Longitude': reconstructed_lon,
            })
            print(f"Reconstructed latitude for point ID {point_id} at {age} Ma: {reconstructed_lat}")
        except Exception as e:
            invalid_points.append({
                'ID': point_id,
                'Latitude': latitude,
                'Longitude': longitude,
                'Age': age,
                'Error': f'Extracting Reconstructed Geometry Failed at {age} Ma: {e}'
            })
            print(f"Failed to extract the reconstructed geometry for point ID {point_id} at {age} Ma: {e}")
            continue

# Save the reconstruction results to a CSV file
try:
    output_df = pd.DataFrame(results)
    output_df.to_csv(output_csv, index=False)
    print(f"Reconstruction results saved to {output_csv}")
except Exception as e:
    print(f"Failed to save the reconstruction results: {e}")
    
    
