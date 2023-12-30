# QGIS
Initially a 300m x 300m grid shapefile is created within QGIS to match the extent of the orthomosaic, delineating the study area for subsequent analyses and a roughness raster is derived from the DEM using the GDAL roughness tool. 

# Python
The Python GIStools.py script then extracts relevant features from these inputs for the random forest algorithm and tiles the raster inputs, which is necessary when working with very large raster datasets. The preprocess_function within this script executes multiple tasks including: extraction of RGB and roughness tiles, creation Excessive Green Index (EGI) and saturation rasters from RGB bands, alignment of all rasters to the smallest extent and highest resolution, and finally compilation of raster bands for Random Forest processing. In the final preprocessing step, the Raster_Matching.py script ensures the uniformity in raster dimensions necessary for random forest algorithm execution.  

The Tiled_Classification_RF.py script, based on work from Florian Beyer and Chris Holden, trains and implements a random forest algorithm on the set of preprocessed tiles (Beyer et al., 2019). This step requires a training and validation shapefile input containing numerically labeled bare earth and vegetation features and produces classified tiles as well as a log file with a confusion matrix. The performance of the algorithm can be improved by using the sieving function of the remotior-sensus Python library which filters out isolated patches less than 36 contiguous pixels of vegetation or bare earth. Each pixel in the classification raster is 1.77 cm2, so this filtration was performed on the assumption that patches of bare earth or vegetation that are less than 0.005 - 0.01 m2 are likely artifacts of the classification algorithm. This sieving step is incorporated into the Filter_rasters.py script, which extracts only bare earth values from the original DEM. The process culminates in the generation of multiple DEM tiles. These tiles can either be analyzed individually, to conserve computational resources, or combined into a single file using the Stitch_Rasters.py script.   
