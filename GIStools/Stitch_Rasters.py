
import rasterio
from rasterio.merge import merge
import os


def stitch_rasters(raster_paths, output_raster_path):
    """
    Stitches multiple rasters into a single raster, one at a time.

    :param raster_paths: List of paths to the raster files to be stitched.
    :param output_raster_path: Path where the stitched raster will be saved.
    """
    try:
        # Open the first raster to initialize the stitched raster
        stitched_raster = rasterio.open(raster_paths[0])
        print("Stitching raster: " + raster_paths[0] + " stitching (0.00%) completed.")
        for raster_path in raster_paths[1:]:
            #print progress as a percentage
            print(f"Stitching raster: {raster_path}") 
            print(f"Stitching {raster_paths.index(raster_path) / len(raster_paths) * 100:.2f}% completed.")
            with rasterio.open(raster_path) as src:
                # Merge the current raster with the stitched raster
                mosaic, out_trans = merge([stitched_raster, src])

                # Update the metadata with new dimensions and transformation
                out_meta = stitched_raster.meta.copy()
                out_meta.update({
                    "height": mosaic.shape[1],
                    "width": mosaic.shape[2],
                    "transform": out_trans
                })

                # Close the current stitched raster
                stitched_raster.close()
                print('Stitched Raster Closed. Writing to Temporary Raster.')
                # Write the current mosaic to a temporary raster
                with rasterio.open(output_raster_path, "w", **out_meta) as temp_dest:
                    temp_dest.write(mosaic)

                # Reopen the updated stitched raster for the next iteration
                stitched_raster = rasterio.open(output_raster_path)

    finally:
        # Close the stitched raster dataset
        stitched_raster.close()
            
def find_files(directory, file_name=None):
    found_files = []
    suffix_list = []

    for root, dirs, files in os.walk(directory):
        # Code to skip over specific subfolders
        # if 'Tiled_Inputs' in dirs:
        #     dirs.remove('Tiled_Inputs')  # This will skip the 'Tiled_Inputs' directory

        for file in files:
            # Check if the file is a .tif file
            if file.lower().endswith('.tif'):
                # Do not pull from directory folder "Tiled Inputs"
                if file_name is None:
                    full_path = os.path.join(root, file)
                    found_files.append(full_path)
                    # Extract last two characters of the file name
                    suffix = file[-6:-4]
                    suffix_list.append(suffix)
                elif file == file_name:
                    full_path = os.path.join(root, file)
                    found_files.append(full_path)

    return found_files, suffix_list           

in_dir = r"Z:\ATD\Drone Data Processing\GIS Processing\Vegetation Filtering Test\Classification_Florian\Test_v1\Test 12 Grid\Results\ME_2023_Full_Run"
inputs, suffix = find_files(in_dir)
output = r"Z:\ATD\Drone Data Processing\GIS Processing\Vegetation Filtering Test\Classification_Florian\Test_v1\Test 12 Grid\Results\ME_2023_Full_Run\ME_2023__Stitched.tif"
stitch_rasters(inputs, output)
