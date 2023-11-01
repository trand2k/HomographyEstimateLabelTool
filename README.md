# HomographyEstimateLabelTool
## Introduction
This tool help to label homography matrix for image pairs. The tool is based on Qt5.9.1 and OpenCV3.4.1. The tool is tested on Ubuntu 20.04.

## Task list

- [x] Label using mouse keep and move
- [x] Label using dot 4 point match
- [x] Label aerial image match map
- [x] Label map match other moment map
- [x] change map when label
- [ ] auto genarate cache label file
- [ ] choose matching algorithm option for autogenerate cache label file


## How to install
install osgeo
    ```
    conda install -c conda-forge gdal==3.6.3

install requirements
    ```
    pip install -r requirements.txt

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
    │       ├── map1.tif                            # map file
    │   └── drone_mask_segmentation                 # drone label segment png file
    └── mapbase_all
        ├── data_homography                         # folder save homography after label
        ├── map_base                                # map base tif file
            ├── map_base.tif                        # map base tif file
        ├── map_base_DSM                            # map base DSM tif file
        └── sub_map                                 # sub map tif file

## How to use
1. Open the tool
    ```
    python label_tool.py
    ```
2. Load map
    if you have more than 1 map in 1 area:

        1. setup all map same as mapbase_all folder 
        2. choose File -> Choose data all label map to map
        3. label homography between map and mapbase
    
3. Load image and label
    ```
    prev - E
    next - R
    save - Q
    delete - S
    Reset homo
    Reset homo to cache - D
    occurency slide bar
    point match - W
    save after choose point - A