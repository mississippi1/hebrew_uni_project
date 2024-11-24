import pandas as pd
import zipfile
import os

selected_columns = ['D', 'E', 'J', 'K']
# Path to the uploaded zip file
zip_file_path = '/Users/tomerpeker/Downloads/metal_1_part_2.zip'
extracted_folder_path = '/Users/tomerpeker/Downloads/lab_b_1/Metal 1/'

# Extract the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder_path)

# List the extracted files to see what we're working with
extracted_files = os.listdir(extracted_folder_path)


# Define function to load CSV, drop unnecessary columns, and rename relevant ones
def process_csv(file_path):
    # Load only specified columns from CSV
    print(file_path)
    df = pd.read_csv(file_path)

    # Rename columns
    df = df.rename(columns={df.columns[3]: 'Time (s)',
                            df.columns[4]: 'Volt Channel 1 (V)',
                            df.columns[9]: 'Time (s) 2',
                            df.columns[10]: 'Volt Channel 2 (V)'})

    df = df[['Time (s)', 'Volt Channel 1 (V)', 'Time (s) 2', 'Volt Channel 2 (V)']]
    df.to_excel(file_path+".xlsx")

    return df


# Process each CSV file in the extracted folder
processed_data = {file_name: process_csv(os.path.join(extracted_folder_path, file_name)) for file_name in
                  extracted_files if file_name.endswith("csv")}

