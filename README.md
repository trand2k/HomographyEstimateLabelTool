# HomographyEstimateLabelTool
## Introduction
This tool help to label homography matrix for image pairs. The tool is based on Qt5.9.1 and OpenCV3.4.1. The tool is tested on Ubuntu 20.04.
## How to install
install osgeo

    conda install -c conda-forge gdal==3.6.3

## Dictionary data set-up
set up data folder like this 


    ├── map1_all
    │   ├── drone_homography                        # folder save homography after label
    │   ├── drone_homography_cache                  # folder save homography before label
    │   ├── drone_homography_checking 
    │   ├── drone_image
    │   ├── drone_jpg                               # drone image 
    │   ├── drone_jpg_json                          # drone label segment json file
    │   ├── drone_map                               # drone map tif file
    │   └── drone_mask_segmentation                 # drone label segment png file
    └── mapbase_all
        ├── data_homography                         # folder save homography after label
        ├── map_base                                # map base tif file
        ├── map_base_DSM                            # map base DSM tif file
        └── sub_map                                 # sub map tif file

## How to use
1. Open the tool
    ```
    ./HomographyEstimateLabelTool
    ```
2. Load image pair
    ```
    zoom-in
    zoom-out
    prev - E
    next - R
    save - Q
    Reset homo
    Reset homo to cache
    occurency slide bar
    four point conner - W
    save point and out - A


    
