import cv2
import numpy as np
import os
from osgeo import gdal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal
    
class AutogenHomographyCache:
    '''
        input is folder data, get data image from folder image jpg and data map from folder map
    '''
    def __init__(self):
        self.name = "autogen_homography_cache"

    
    def get_data_from_tiff_file(self,tiff_path):
        geotiff_map1 = gdal.Open(tiff_path)
        red = geotiff_map1.GetRasterBand(1).ReadAsArray()
        green = geotiff_map1.GetRasterBand(2).ReadAsArray()
        blue = geotiff_map1.GetRasterBand(3).ReadAsArray()
        map_rgb_1 = np.dstack((blue, green, red))
        #     map_rgb_1 = cv2.cvtColor(map_rgb_1, cv2.COLOR_BGR2GRAY)
        return map_rgb_1
    
    def feature_matching_return_image(self, image1, image):
        '''
        feature matching algorithm
        :param image1: image 1
        :param image2: image 2
        :return: return image after feature matching
        '''
        image2 = image.copy()
        MIN_MATCH_COUNT = 5
        img1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)  # queryImage
        img2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)  # trainImage
        # Initiate SIFT detector
        sift = cv2.SIFT_create()
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=2)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)
        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()
            h, w = img1.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            img2 = cv2.polylines(image2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
        else:
            print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
            matchesMask = None
        draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                        singlePointColor=None,
                        matchesMask=matchesMask,  # draw only inliers
                        flags=2)
        img3 = cv2.drawMatches(image1, kp1, image2, kp2, good, None, **draw_params)
        return img3,M
        


class WorkerThread(QThread):
    update_progress = pyqtSignal(int)
    task_completed = pyqtSignal()

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
    
    def run(self):
        Autogen_homography_cache = AutogenHomographyCache()
        # Autogen_homography_cache.create_homography_cache(self.folder_path)

        last_part = os.path.basename(self.folder_path)
        number = ''.join(filter(str.isdigit, last_part))
        tiff_file_path = self.folder_path + "/drone_map/map" + str(number) + ".tif"
        cache_folder_path = self.folder_path+"/drone_homography_cache/"
        image_folder_path = self.folder_path + "/drone_jpg/"
        map_rgb = Autogen_homography_cache.get_data_from_tiff_file(tiff_file_path)
        for index, i in enumerate(os.listdir(image_folder_path)):
            # print(len(os.listdir(image_folder_path))//100)
            print(index/(len(os.listdir(image_folder_path))/100))
            self.update_progress.emit(int(index/(len(os.listdir(image_folder_path))/100)))
            try:
                print(image_folder_path+i)
                image = cv2.imread(image_folder_path+i)
                img_match,M = Autogen_homography_cache.feature_matching_return_image(image,map_rgb)
                path_homography = cache_folder_path
                np.savetxt(path_homography + i[:-4]+'.txt', M)
            except Exception as e:
                print(f"Error matching for {i}: {e}")
                identity_matrix = np.eye(3)
                np.savetxt(path_homography + i[:-4] + '.txt', identity_matrix)

        self.task_completed.emit()