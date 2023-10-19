import cv2
import numpy as np
class Opencv_helper:
    def __init__(self):
        self.name = "opencv_helper"
        self.point_init_in_map = None
        self.point_init_in_image = None
        self.homography_matrix = None
        self.image = None
        self.map = None
        self.visualize_image = None
        self.occurency = 0.5
        self.point_init_in_map_fix_4_corner = None
    def change_occurency(self, value):
        self.occurency = value/100
    def add_new_image(self, map, image, homography_matrix = None):
        '''
            init when next image
        :param map:
        :param image:
        :param homography_matrix:
        :return:
        '''
        self.image = image
        self.map = map
        self.init_2_image(homography_matrix)
        self.merge_2_image()

    def change_point(self, point_in_map_before, point_in_map_after):
        '''
            this function change point in map before and after
            logic:
                - define point_in_map_before in which area of image
                - change self.point_init_in_image in area of image to point_in_map_before inverse map
                - change self.point_init_in_map in area of image to point_in_map_after
        :param point_in_map_before: is the point in map before change
        :param point_in_map_after:  is the point in map after change
        :return: update self.point_init_in_image and self.point_init_in_map
        '''

        point_in_image_before = self.tranform_point(point_in_map_before, np.linalg.inv(self.homography_matrix))
        area = self.define_4_area(point_in_image_before, self.image)
        # print("+++++++++++++++++++++++++++++++++++++==============++++++++++++++++++++++++++++++++++++++++")
        # print("AREA:   ",area)
        # print("point_in_image_before: ", point_in_image_before)
        # print("point_in_map_after: ", point_in_map_after)
        # print("point_in_map_before: ", point_in_map_before)
        # print("point_init_in_image: ", self.point_init_in_image)
        # print("point_init_in_map: ", self.point_init_in_map)
        # print("homography matrix before: ", self.homography_matrix)
        if area == 1:
            self.point_init_in_image[0] = [point_in_image_before[0], point_in_image_before[1]]
            self.point_init_in_map[0] = [point_in_map_after[0], point_in_map_after[1]]
        elif area == 2:
            self.point_init_in_image[1] = [point_in_image_before[0], point_in_image_before[1]]
            self.point_init_in_map[1] = [point_in_map_after[0], point_in_map_after[1]]
        elif area == 3:
            self.point_init_in_image[2] = [point_in_image_before[0], point_in_image_before[1]]
            self.point_init_in_map[2] = [point_in_map_after[0], point_in_map_after[1]]
        else:
            self.point_init_in_image[3] = [point_in_image_before[0], point_in_image_before[1]]
            self.point_init_in_map[3] = [point_in_map_after[0], point_in_map_after[1]]
        self.homography_matrix,_ = cv2.findHomography(self.point_init_in_image, self.point_init_in_map)
        # print("homography matrix after: ", self.homography_matrix)
        # print("point_init_in_image_after: ", self.point_init_in_image)
        # print("point_init_in_map_after: ", self.point_init_in_map)
        self.merge_2_image()
    def define_4_area(self, point, image):
        '''
            this function define a click point in which area of image
        :param point: tuple (x,y), int
        :param image: image data
        :return: area: 1: top left, 2: top right, 3: bottom left, 4: bottom right
        1      |      2
               |
        -------|--------
               |
        4      |      3
        '''
        x, y = point
        height, width, _ = image.shape
        if x < width / 2 and y < height / 2:
            return 1
        elif x > width / 2 and y < height / 2:
            return 2
        elif x < width / 2 and y > height / 2:
            return 4
        else:
            return 3

    def tranform_point(self, point, homography_matrix):
        '''
            thí function find point through from point in map to point in image with homography matrix
        :param point:
        :param homography_matrix:
        :return:
        '''
        point_homogeneous = np.array([point[0], point[1], 1])

        # Apply the homography transformation
        transformed_point_homogeneous = np.dot(homography_matrix, point_homogeneous)

        # Convert back to Cartesian coordinates [x', y', w']
        transformed_point_cartesian = transformed_point_homogeneous / transformed_point_homogeneous[-1]

        # Extract the transformed (x', y') coordinates
        transformed_point = (transformed_point_cartesian[0], transformed_point_cartesian[1])

        return transformed_point



    def init_2_image(self, homography_matrix= None):
        '''
            init 4 point in map and in image
        :param map:
        :param image:
        :param homography_matrix:
        :return:
        '''
        if homography_matrix is not None:
            self.point_init_in_image = np.array(
                [[0, 0], [self.image.shape[1], 0], [self.image.shape[1], self.image.shape[0]], [0, self.image.shape[0]]],
                dtype=np.float32)
            # import pdb;pdb.set_trace()
            # print("homography_matrix: ", homography_matrix)
            # print("point_init_in_image reshape: ", self.point_init_in_image.reshape(-1, 1, 2))
            self.point_init_in_map = np.squeeze(cv2.perspectiveTransform(self.point_init_in_image.reshape(-1, 1, 2), homography_matrix))

        else:
            self.point_init_in_image = np.array(
                [[0, 0], [self.image.shape[1], 0], [self.image.shape[1], self.image.shape[0]], [0, self.image.shape[0]]],
                dtype=np.float32)
            self.point_init_in_map = np.array(
                [[0, 0], [self.image.shape[1], 0], [self.image.shape[1], self.image.shape[0]], [0, self.image.shape[0]]],
                dtype=np.float32)
        self.homography_matrix,_ = cv2.findHomography(self.point_init_in_image, self.point_init_in_map)

    def merge_2_image(self):
        '''
            show image with map
            input : 4 point in image
            image have 4 patch , topleft, topright, bottomleft, bottomright
                    4 point in map
                    homography is homography init in map 
                    output image_merge and homography matrix end
        '''


        # when i dot 1 point, this is point in map
        point_init_image = np.array(
                [[0, 0], [self.image.shape[1], 0], [self.image.shape[1], self.image.shape[0]], [0, self.image.shape[0]]],
                dtype=np.float32)
        self.point_init_in_map_fix_4_corner = np.squeeze(
            cv2.perspectiveTransform(point_init_image.reshape(-1, 1, 2), self.homography_matrix))
        map_copy = self.map.copy()
        black_image = np.zeros_like(self.map)
        # print("black_image shape: ", black_image.shape)
        # print("homography matrix: ", self.homography_matrix)

        warped_image = cv2.warpPerspective(self.image, self.homography_matrix, (black_image.shape[1], black_image.shape[0]))
        points = self.point_init_in_map.astype(np.int32)
        points_fix = self.point_init_in_map_fix_4_corner.astype(np.int32)
        cv2.polylines(map_copy, [points], True, (0, 0, 255), thickness=5)
        cv2.polylines(map_copy, [points_fix], True, (255, 0, 0), thickness=5)
        merged_image = cv2.addWeighted(map_copy, self.occurency, warped_image, 1 - self.occurency, 0)
        self.visualize_image  = merged_image