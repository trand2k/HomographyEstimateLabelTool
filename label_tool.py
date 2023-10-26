from osgeo import gdal
from PyQt5 import QtGui
from PyQt5.QtCore import QEvent
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QTransform, QPixmap, QImage
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QMenu, QAction, QFileDialog,QListWidget,QListWidgetItem
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtCore import pyqtSignal
app = QApplication(sys.argv)
import cv2
import numpy as np
import os
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget, QFileDialog,QShortcut,QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QTransform, QWheelEvent,QKeySequence
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QToolBar,QLabel,QLineEdit,QSplitter,QApplication, QMainWindow, QPushButton, QListWidget, QListWidgetItem,QSlider,QMessageBox
import sys
import cv2
import numpy as np
import os
from helper.opencv_helper import Opencv_helper
from helper.window_dot_point import MainWindow2
class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.graphics_view = CustomGraphicsView(self.central_widget)
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        self.graphics_view.mouseMoveSignal.connect(self.onGraphicsViewMouseMove)
        self.left_mouse_button_pressed = False

        self.image_item = QGraphicsPixmapItem()
        self.scene.addItem(self.image_item)
        # add opencv helper

        self.opencv_helper = Opencv_helper()
        '''
            function of opencv_helper
                + add_new_image: load_image, map and homography matrix, setup init image 
                + change_point: change point  
        '''
        self.zoom_factor = 1.0

        # create menu bar 
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        
        # Open folder action
        choose_data_all_action = QAction("Choose data all", self)
        choose_data_all_action.triggered.connect(self.choose_data_all)
        file_menu.addAction(choose_data_all_action)
        
        # Open folder action 
        open_action = QAction("Open folder image", self)
        open_action.triggered.connect(self.open_folder_image)
        file_menu.addAction(open_action)

        # Open File action 
        open_file_action = QAction("Open file map", self)
        open_file_action.triggered.connect(self.open_tiff_file)
        file_menu.addAction(open_file_action)

        # Choose Save Folder 
        choose_save_folder_action = QAction("Choose homography save folder", self)
        choose_save_folder_action.triggered.connect(self.choose_save_folder)
        file_menu.addAction(choose_save_folder_action)

        #Choose cache folder 
        choose_cache_folder_action = QAction("Choose homography cache folder", self)
        choose_cache_folder_action.triggered.connect(self.choose_cache_folder)
        file_menu.addAction(choose_cache_folder_action)

        self.zoom_in_button = QPushButton("Zoom In", self.central_widget)
        self.zoom_out_button = QPushButton("Zoom Out", self.central_widget)
        '''
            add-on function, prev, next, save, unsave
        '''
        # help me dreate button
        
        # create button
        self.prev_button = QPushButton("Prev", self.central_widget)
        self.next_button = QPushButton("Next", self.central_widget)
        self.save_button = QPushButton("Save", self.central_widget)
        self.delete_button = QPushButton("Delete", self.central_widget)
        self.reset_homo_button = QPushButton("Reset Homo", self.central_widget)
        self.reset_homo_cache_button = QPushButton("Reset Homo Cache", self.central_widget)

        self.four_point_press_button = QPushButton("Four Point Press", self.central_widget)

        
        

        # create a slider
        self.slider = QSlider(self)
        self.slider.setOrientation(1)  # 1 corresponds to vertical orientation
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.update_occurency)


        # create Shortcut
        prev_shortcut = QShortcut(QKeySequence("E"), self)
        prev_shortcut.activated.connect(self.handle_prev_button_click)
        self.prev_button.clicked.connect(self.handle_prev_button_click)
        
        next_shortcut = QShortcut(QKeySequence("R"), self)
        next_shortcut.activated.connect(self.handle_next_button_click)
        self.next_button.clicked.connect(self.handle_next_button_click)
        
        save_shortcut = QShortcut(QKeySequence("Q"), self)
        save_shortcut.activated.connect(self.handle_save_button_click)
        self.save_button.clicked.connect(self.handle_save_button_click)

        delete_shortcut = QShortcut(QKeySequence("S"), self)
        delete_shortcut.activated.connect(self.handle_delete_button_click)
        self.delete_button.clicked.connect(self.handle_delete_button_click)

        four_point_press_shortcut = QShortcut(QKeySequence("W"), self)
        four_point_press_shortcut.activated.connect(self.handle_four_point_press_button_click)
        self.four_point_press_button.clicked.connect(self.handle_four_point_press_button_click)
        


        self.reset_homo_button.clicked.connect(self.reset_homo_button_click)

        reset_homo_cache_shortcut = QShortcut(QKeySequence("D"), self)
        reset_homo_cache_shortcut.activated.connect(self.reset_homo_cache_button_click)
        self.reset_homo_cache_button.clicked.connect(self.reset_homo_cache_button_click)

        layout = QVBoxLayout(self.central_widget)






        # Add buttons to a horizontal layout
        widget_with_layout = QWidget()
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.zoom_in_button)
        button_layout.addWidget(self.zoom_out_button)
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.reset_homo_button)
        button_layout.addWidget(self.reset_homo_cache_button)
        button_layout.addWidget(self.four_point_press_button)
        
        self.plain_text_label = QLabel(self)
        self.plain_text_label.setText(" E - prev \n R - next \n Q - save \n S - delete \n W - open point choose \n D - reset homo cache \n A - save after choose point")
        button_layout.addWidget(self.plain_text_label)

        button_layout.addWidget(self.slider)
        self.list_widget = QListWidget(self.central_widget)
        button_layout.addWidget(self.list_widget)

        ############################################################
        ################# TEST TOOL BAR ############################
        ############################################################
        
        # toolbar = QToolBar(self)
        # self.addToolBar(toolbar)

        # # Add buttons and widgets to the toolbar
        # toolbar.addWidget(self.zoom_in_button)
        # toolbar.addWidget(self.zoom_out_button)
        # toolbar.addWidget(self.prev_button)
        # toolbar.addWidget(self.next_button)
        # toolbar.addWidget(self.save_button)
        # toolbar.addWidget(self.delete_button)
        # toolbar.addWidget(self.reset_homo_button)
        # toolbar.addWidget(self.reset_homo_cache_button)
        # toolbar.addWidget(self.four_point_press_button)
        # toolbar.addWidget(self.plain_text_label)
        # toolbar.addWidget(self.slider)
        # toolbar.addWidget(self.list_widget)


        #############################################################
        ############# END ###########################################
        #############################################################

        layout_group = QVBoxLayout(widget_with_layout)
        layout_group.addLayout(button_layout)
        # layout_group.addWidget(self.slider)
        # self.list_widget = QListWidget(self.central_widget)
        # layout_group.addWidget(self.list_widget)
        # Add QSpliter 
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.graphics_view)
        splitter.addWidget(widget_with_layout)  # Add the horizontal button layout
        
        layout.addWidget(splitter)
        # Add the graphics view, button layout, and slider
        # layout.addWidget(self.graphics_view)
        # layout.addLayout(button_layout)  # Add the horizontal button layout
        # layout.addWidget(self.slider)


        # #add List Widget

        # self.list_widget = QListWidget(self.central_widget)
        # layout.addWidget(self.list_widget)

        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)

        # self.image_data = cv2.imread("03_09_2023_09_27_02_geotag.jpg")
        # self.image_data = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2RGB)
        # self.display_image(self.image_data)

        self.image_data = None
        self.central_widget.installEventFilter(self)

        self.folder_image_path = ""
        self.file_images_path = []
        self.file_map_path = ""
        self.folder_homography_cache = ""
        self.folder_homography_save = ""
        # .image file folder path
        self.folder_image_raw_path = ""
        
        self.files_homography_save = []
        self.clicked_point = None
        self.map_data = None
        self.homography_matrix = None
        self.point_move = None
        self.point_move_pre = None

        self.point_in_map = None
        self.point_in_image = None

        self.window2 = MainWindow2()
        self.window2.destroyed.connect(self.handle_window2_closed)

        #todo: for debug
        # self.open_tiff_file()
        # self.choose_cache_folder()
        # self.choose_save_folder()
        # self.open_folder_image()
    
    def reset_homo_button_click(self):
        homography_matrix = np.eye(3)
        self.opencv_helper.add_new_image(self.map_data, self.image_data, homography_matrix)
        self.display_image(self.opencv_helper.visualize_image)

    def reset_homo_cache_button_click(self):
        current_index = self.file_images_path.index(self.list_widget.currentItem().text())
        homography_file_cache = self.folder_homography_cache + "/" + \
                                   os.path.basename(self.file_images_path[current_index]).split(".")[0] + ".txt"
        # print(homography_file_cache)
        homography_matrix = np.loadtxt(homography_file_cache)
        self.opencv_helper.add_new_image(self.map_data, self.image_data, homography_matrix)
        self.display_image(self.opencv_helper.visualize_image)

    def update_occurency(self, value):
        self.opencv_helper.change_occurency(value)
        homography_matrix = self.opencv_helper.homography_matrix
        self.opencv_helper.add_new_image(self.map_data, self.image_data, homography_matrix)
        self.display_image(self.opencv_helper.visualize_image)
    
    def handle_window2_closed(self):
        condition = self.check_condition(self.window2.mouse_click_point_1, self.window2.mouse_click_point_2)
        if not condition:
            # print("check condition")
            QMessageBox.warning(self, "Warning", "Point not match between 2 image")
            # self.window2.show()
            # Conditions are met, close window1
            # print("CHECK:  ", self.window2.mouse_click_point_1)
            # print("CHECK2 :  ", self.window2.mouse_click_point_2)
            
            self.window2.reset_point()
            self.window2.destroyed.connect(self.handle_window2_closed)
        else:
            points_src = np.array(self.window2.mouse_click_point_1, dtype=float)
            points_dst = np.array(self.window2.mouse_click_point_2, dtype=float)

            points_src = points_src.reshape(-1, 1, 2)
            points_dst = points_dst.reshape(-1, 1, 2)

            # Find homography matrix
            homography_matrix, _ = cv2.findHomography(points_src, points_dst, cv2.RANSAC)
            self.opencv_helper.add_new_image(self.map_data, self.image_data, homography_matrix)
            self.display_image(self.opencv_helper.visualize_image)
            print("DONE")
            # print(homography_matrix)

            self.window2.reset_point()
            self.window2.destroyed.connect(self.handle_window2_closed)
    
    @staticmethod
    def check_condition(list_point_1, list_point_2):
        try:
            points_src = np.array(list_point_1, dtype=float)
            points_dst = np.array(list_point_2, dtype=float)

            points_src = points_src.reshape(-1, 1, 2)
            points_dst = points_dst.reshape(-1, 1, 2)

            # Find homography matrix
            homography_matrix, _ = cv2.findHomography(points_src, points_dst, cv2.RANSAC)
            
            return True
        except:
            return False

    
    def handle_four_point_press_button_click(self):
        self.window2.load_image(self.image_data, self.map_data)
        self.window2.show()

    def handle_prev_button_click(self):
        if self.file_images_path:
            # Find the index of the currently displayed image
            current_index = self.file_images_path.index(self.list_widget.currentItem().text())

            # Decrement the index to move to the previous image
            prev_index = (current_index - 1) % len(self.file_images_path)

            # Load and display the previous image
            prev_image_path = self.file_images_path[prev_index]
            self.image_data = cv2.imread(prev_image_path)
            self.image_data = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2RGB)
            # for merge 2 image
            homography_matrix = self.read_homography_matrix(self.has_cache_label_file(prev_image_path)[1])
            self.opencv_helper.add_new_image(self.map_data, self.image_data, homography_matrix)
            self.display_image(self.opencv_helper.visualize_image)


            # Update the selected item in the list widget
            self.list_widget.setCurrentItem(self.list_widget.item(prev_index))


    def handle_next_button_click(self):
        if self.file_images_path:
            # Find the index of the currently displayed image
            current_index = self.file_images_path.index(self.list_widget.currentItem().text())

            # Increment the index to move to the next image
            next_index = (current_index + 1) % len(self.file_images_path)

            # Load and display the next image
            next_image_path = self.file_images_path[next_index]
            self.image_data = cv2.imread(next_image_path)
            self.image_data = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2RGB)
            # for merge 2 image
            homography_matrix = self.read_homography_matrix(self.has_cache_label_file(next_image_path)[1])
            self.opencv_helper.add_new_image(self.map_data, self.image_data, homography_matrix)
            self.display_image(self.opencv_helper.visualize_image)

            # Update the selected item in the list widget
            self.list_widget.setCurrentItem(self.list_widget.item(next_index))

    def handle_delete_button_click(self):
        if self.file_images_path:
            # Find the index of the currently displayed image
            ######################################################
            current_index = self.file_images_path.index(self.list_widget.currentItem().text())
            homography_file_save = (self.folder_homography_save + "/" +
                                    os.path.basename(self.file_images_path[current_index]).split(".")[0] + ".txt")
            if os.path.exists(homography_file_save):
                os.remove(homography_file_save)
            ##########################################################
            ###########   UPDATE TICK    #############################
            ##########################################################

            has_label, _ = self.has_label_file(self.list_widget.currentItem().text())
            self.list_widget.currentItem().setData(Qt.UserRole, has_label)
            if has_label:
                self.list_widget.currentItem().setCheckState(Qt.Checked)
            else:
                self.list_widget.currentItem().setCheckState(Qt.Unchecked)


            ##########################################################
            ############     MOVE NEXT IMAGE     #####################
            ##########################################################

            # Increment the index to move to the next image
            next_index = (current_index + 1) % len(self.file_images_path)

            # Load and display the next image
            next_image_path = self.file_images_path[next_index]
            self.image_data = cv2.imread(next_image_path)
            self.image_data = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2RGB)
            # for merge 2 image
            homography_matrix = self.read_homography_matrix(self.has_cache_label_file(next_image_path)[1])
            self.opencv_helper.add_new_image(self.map_data, self.image_data, homography_matrix)
            self.display_image(self.opencv_helper.visualize_image)

            # Update the selected item in the list widget
            self.list_widget.setCurrentItem(self.list_widget.item(next_index))


    def handle_save_button_click(self):
        if self.file_images_path:
            # Find the index of the currently displayed image
            ######################################################
            current_index = self.file_images_path.index(self.list_widget.currentItem().text())
            '''
                save homography matrix to
            '''
            homography_file_save = (self.folder_homography_save + "/" +
                                    os.path.basename(self.file_images_path[current_index]).split(".")[0] + ".txt")
            homography_file_cache = self.folder_homography_cache + "/" + \
                                   os.path.basename(self.file_images_path[current_index]).split(".")[0] + ".txt"
            print("CACHE PATH:  ", homography_file_cache)
            np.savetxt(homography_file_save, self.opencv_helper.homography_matrix)
            # np.savetxt(homography_file_cache, self.opencv_helper.homography_matrix)
            ##########################################################
            '''
                update tick for list widget
            '''
            has_label, _ = self.has_label_file(self.list_widget.currentItem().text())
            self.list_widget.currentItem().setData(Qt.UserRole, has_label)
            if has_label:
                self.list_widget.currentItem().setCheckState(Qt.Checked)
            else:
                self.list_widget.currentItem().setCheckState(Qt.Unchecked)
            ##########################################################

            # Increment the index to move to the next image
            next_index = (current_index + 1) % len(self.file_images_path)

            # Load and display the next image
            next_image_path = self.file_images_path[next_index]
            self.image_data = cv2.imread(next_image_path)
            self.image_data = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2RGB)
            # for merge 2 image
            homography_matrix = self.read_homography_matrix(self.has_cache_label_file(next_image_path)[1])
            self.opencv_helper.add_new_image(self.map_data, self.image_data, homography_matrix)
            self.display_image(self.opencv_helper.visualize_image)

            # Update the selected item in the list widget
            self.list_widget.setCurrentItem(self.list_widget.item(next_index))

    
    def read_map(self,map_path):
        # print("data path : " , map_path)
        geotiff = gdal.Open(map_path)
        red = geotiff.GetRasterBand(1).ReadAsArray()
        green = geotiff.GetRasterBand(2).ReadAsArray()
        blue = geotiff.GetRasterBand(3).ReadAsArray()
        map_rgb = np.dstack((blue, green, red))
        return map_rgb
    def update_list_widget(self):
        # Clear existing items
        self.list_widget.clear()
        self.file_images_path= sorted(self.file_images_path)
        # Add each file path to the list widget
        for file_path in sorted(self.file_images_path):
            item = QListWidgetItem(file_path)
            import random
            has_label,_ = self.has_label_file(file_path)
            item.setData(Qt.UserRole, has_label)
            if has_label:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.list_widget.addItem(item)
            item.setFlags(item.flags() & ~Qt.ItemIsUserCheckable)
        # Connect the itemClicked signal to a slot
        self.list_widget.itemClicked.connect(self.list_item_clicked)

    def has_label_file(self, file_path):
        '''
            check image have label or not
        '''
        # self.folder_image_path = ""
        # self.file_images_path = []
        # self.file_map_path = ""
        # self.folder_homography_cache = ""
        # self.folder_homography_save = ""
        # self.files_homography_save = []
        # self.clicked_points = []
        file_name = os.path.basename(file_path)
        file_name, _ = os.path.splitext(file_name)

        new_file_name = file_name + ".txt"
        
        return os.path.exists(self.folder_homography_save + "/"+ new_file_name),self.folder_homography_save + "/"+ new_file_name

    def has_cache_label_file(self, file_path):
        '''
            check image have label or not
            check in save folder 
            if have label file, load homography from save folder
            else load homography from cache folder
        '''
        # self.folder_image_path = ""
        # self.file_images_path = []
        # self.file_map_path = ""
        # self.folder_homography_cache = ""
        # self.folder_homography_save = ""
        # self.files_homography_save = []
        # self.clicked_points = []
        file_name = os.path.basename(file_path)
        file_name, _ = os.path.splitext(file_name)

        new_file_name = file_name + ".txt"

        if os.path.exists(self.folder_homography_save + "/"+ new_file_name):
            return True, self.folder_homography_save + "/"+ new_file_name
        else:
            return False, self.folder_homography_cache + "/"+ new_file_name
    def list_item_clicked(self, item):
        # Handle the event when a list item is clicked

        file_path = item.text()
        self.image_data = cv2.imread(file_path)
        self.image_data = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2RGB)
        self.display_image(self.image_data)
        homography_matrix = self.read_homography_matrix(self.has_cache_label_file(file_path)[1])
        self.opencv_helper.add_new_image(self.map_data, self.image_data, homography_matrix)
        self.display_image(self.opencv_helper.visualize_image)


    def read_homography_matrix(self, file_path):
        '''
            read homography matrix from file
        '''
        print("FILE_PATH: ", file_path)
        if not os.path.exists(file_path):
            return np.array(
                [[0, 0], [640, 0], [640, 480], [0, 480]],
                dtype=np.float32)
        homography_matrix = np.loadtxt(file_path)
        return homography_matrix
    

    #todo: comment for debug
    def choose_data_all(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, 'Open All Folder', options=options)
        self.open_tiff_file_for_all(folder_path)
        self.choose_cache_folder_for_all(folder_path)
        self.choose_save_folder_for_all(folder_path)
        self.open_folder_image_for_all(folder_path)
        # pass

    #todo: comment for debug
    def open_folder_image(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, 'Open Image Folder', options=options)
        #
        # folder_path = "/home/trand/Desktop/build_map/Data_Creater/drone1_image-20230509T081743Z-001/data_for_train/drone6_all/drone_jpg"
        # print(folder_path)     
        if folder_path:
            self.folder_image_path = folder_path
        self.file_images_path = [folder_path + "/" + str(i) for i in os.listdir(folder_path) if i.endswith((".jpg",".jpeg", ".png"))]
        # print(self.folder_image_path)
        # print(self.file_images_path)
        self.update_list_widget()
        if self.file_images_path:

            first_item = self.list_widget.item(0)
            if first_item:
                self.list_widget.setCurrentItem(first_item)
                
                # Load and display the first image
                first_image_path = first_item.text()
                self.image_data = cv2.imread(first_image_path)
                self.image_data = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2RGB)
                '''
                add new image function:
                    :param map: 
                    :param image:
                    :param homography_matrix:    
                '''
                homography_matrix = self.read_homography_matrix(self.has_cache_label_file(first_image_path)[1])
                self.opencv_helper.add_new_image(self.map_data, self.image_data, homography_matrix)
                self.display_image(self.opencv_helper.visualize_image)
    
    def open_folder_image_for_all(self, folder_path):
        folder_path = folder_path + "/drone_jpg"
        # print(folder_path)     
        if os.path.exists(folder_path):
            self.folder_image_path = folder_path
            self.file_images_path = [folder_path + "/" + str(i) for i in os.listdir(folder_path) if i.endswith((".jpg",".jpeg", ".png"))]
        # print(self.folder_image_path)
        # print(self.file_images_path)
        self.update_list_widget()
        if self.file_images_path:

            first_item = self.list_widget.item(0)
            if first_item:
                self.list_widget.setCurrentItem(first_item)
                
                # Load and display the first image
                first_image_path = first_item.text()
                self.image_data = cv2.imread(first_image_path)
                self.image_data = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2RGB)
                '''
                add new image function:
                    :param map: 
                    :param image:
                    :param homography_matrix:    
                '''
                homography_matrix = self.read_homography_matrix(self.has_cache_label_file(first_image_path)[1])
                self.opencv_helper.add_new_image(self.map_data, self.image_data, homography_matrix)
                self.display_image(self.opencv_helper.visualize_image)

    #todo: comment for debug
    def open_tiff_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Map TIFF file', '', 'Images (*.tif);;All Files (*)', options=options)
        if file_path:
            self.file_map_path = file_path
            # print(self.file_map_path)
            self.map_data = self.read_map(self.file_map_path)
            self.map_data = cv2.cvtColor(self.map_data, cv2.COLOR_BGR2RGB)
            self.display_image(self.map_data)
    
    def open_tiff_file_for_all(self, folder_path):
        # debug code


        # Split the path and get the last part
        last_part = os.path.basename(folder_path)
        # Extract the digit from the last part
        number = ''.join(filter(str.isdigit, last_part))

        self.file_map_path = folder_path + "/drone_map/map" + str(number) + ".tif"
        if os.path.exists(self.file_map_path):
            self.map_data = self.read_map(self.file_map_path)
            self.map_data = cv2.cvtColor(self.map_data, cv2.COLOR_BGR2RGB)
            self.display_image(self.map_data)


    #todo: comment for debug
    def choose_save_folder(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, 'Open Image Folder', options=options)
        # folder_path = "/home/trand/Desktop/build_map/Data_Creater/drone1_image-20230509T081743Z-001/data_for_train/drone6_all/drone_homography"
        if folder_path:
            self.folder_homography_save = folder_path
            self.files_homography_save = [folder_path + "/" + str(i) for i in os.listdir(folder_path) if i.endswith((".txt"))]
        self.update_list_widget()
        # print("save homography: ",self.folder_homography_save)    
        # print("file homography save: ", self.files_homography_save)     

    def choose_save_folder_for_all(self,folder_path):
        folder_path = folder_path + "/drone_homography"
        if os.path.exists(folder_path):
            self.folder_homography_save = folder_path
            self.files_homography_save = [folder_path + "/" + str(i) for i in os.listdir(folder_path) if i.endswith((".txt"))]
        self.update_list_widget()
        # print("save homography: ",self.folder_homography_save)    
        # print("file homography save: ", self.files_homography_save)  
    
    #todo: comment for debug
    def choose_cache_folder(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, 'Open Image Folder', options=options)
        if folder_path:
            self.folder_homography_cache = folder_path
        print("cache homography: ", self.folder_homography_cache)

        # debug code
        # self.folder_homography_cache = "/home/trand/Desktop/build_map/Data_Creater/drone1_image-20230509T081743Z-001/data_for_train/drone6_all/drone_homography_cache"
    def choose_cache_folder_for_all(self, folder_path):
        self.folder_homography_cache = folder_path+"/drone_homography_cache"

    def load_image(self, file_path):
        pixmap = QPixmap(file_path)
        self.image_item.setPixmap(pixmap)
        self.graphics_view.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.update_zoom()

    def load_image_numpy(self, image):
        image = QImage(image, image.shape[1], image.shape[0], image.shape[1] * 3, QImage.Format_RGB888)
        pix = QPixmap(image)
        pixmap = QPixmap(pix)
        self.image_item.setPixmap(pixmap)
        self.graphics_view.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.update_zoom()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.left_mouse_button_pressed = True
            self.clicked_point = (self.graphics_view.event_click[0],self.graphics_view.event_click[1])
            # Redraw the image with the added points
            self.draw_points()
        super(ImageViewer, self).mousePressEvent(event)

    def onGraphicsViewMouseMove(self, scene_pos):
        if self.left_mouse_button_pressed:
            print(f"Mouse moved in CustomMainWindow: ({scene_pos.x()}, {scene_pos.y()})")
            self.point_move = (int(scene_pos.x()), int(scene_pos.y()))
            # print("MOUSE MOVE: ", self.point_move)
            if self.point_move_pre is None:
                self.opencv_helper.change_point(self.clicked_point,self.point_move)
            else:
                self.opencv_helper.change_point(self.point_move_pre, self.point_move)
            self.point_move_pre = (int(scene_pos.x()), int(scene_pos.y()))

            self.draw_points_move()

    def mouseReleaseEvent(self, event):
        print("in orininal mouseReleaseEvent")
        if event.button() == Qt.LeftButton:
            self.left_mouse_button_pressed = False
            print(f"Mouse released in CustomMainWindow: ({self.graphics_view.event_click[0]}, {self.graphics_view.event_click[1]})")
            self.point_move = (int(self.graphics_view.event_click[0]), int(self.graphics_view.event_click[1]))
            if self.point_move_pre is None:
                self.opencv_helper.change_point(self.clicked_point,self.point_move)
            else:
                self.opencv_helper.change_point(self.point_move_pre, self.point_move)
            self.point_move_pre = None
            self.draw_points_release()
        super(ImageViewer, self).mouseReleaseEvent(event)


    def display_image(self, image_data):
        # Convert the NumPy array to a QImage
        height, width, channel = image_data.shape
        bytes_per_line = 3 * width
        q_image = QImage(image_data.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Convert the QImage to a QPixmap
        pixmap = QPixmap.fromImage(q_image)

        # Remove the previous pixmap from the scene
        if self.image_item is not None:
            self.scene.removeItem(self.image_item)
            self.image_item = None

        # Set the pixmap to the QGraphicsPixmapItem
        self.image_item = self.scene.addPixmap(pixmap)

        # Set the scene rect to the image size
        self.graphics_view.setSceneRect(0, 0, pixmap.width(), pixmap.height())

    def draw_points(self):
        # Create a copy of the original image_data
        image_with_points = np.copy(self.opencv_helper.visualize_image)
        # print(self.clicked_points)
        # Draw points on the copy
        cv2.circle(image_with_points, self.clicked_point, 5, (255, 0, 0), -1)

        # Display the image with points
        self.display_image(image_with_points)

    def draw_points_move(self):
        image_with_points = np.copy(self.opencv_helper.visualize_image)
        cv2.circle(image_with_points, self.point_move, 5, (0,255,0),-1)
        self.display_image(image_with_points)

    def draw_points_release(self):
        image_with_points = np.copy(self.opencv_helper.visualize_image)
        cv2.circle(image_with_points, self.point_move, 5, (0,0,255),-1)
        self.display_image(image_with_points)

    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.update_zoom()

    def zoom_out(self):
        self.zoom_factor /= 1.2
        self.update_zoom()

    def update_zoom(self):
        transform = QTransform()
        # print("check")
        transform.translate(self.graphics_view.viewport().width() / 2, self.graphics_view.viewport().height() / 2)
        transform.scale(self.zoom_factor, self.zoom_factor)
        transform.translate(-self.graphics_view.viewport().width() / 2, -self.graphics_view.viewport().height() / 2)
        self.graphics_view.setTransform(transform)



class CustomGraphicsView(QGraphicsView):
    mouseMoveSignal = pyqtSignal(QPointF)
    def __init__(self, parent=None):
        super(CustomGraphicsView, self).__init__(parent)
        self.setMouseTracking(True)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.zoom_factor = 1.0
        self.event_click = None
        self.move_mouse_event = None

    def mousePressEvent(self, event):
        # Get the position in image coordinates
        # print("CustomGraphicViewer: ", event.pos())

        pos_in_image = self.mapToScene(event.pos())
        pixel_x = int(pos_in_image.x())
        pixel_y = int(pos_in_image.y())
        # print(f"Clicked at pixel location: ({pixel_x}, {pixel_y})")
        self.event_click = (pixel_x, pixel_y)
        # import pdb;pdb.set_trace()
        # Continue with the default behavior
        
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.mouseMoveSignal.emit(self.mapToScene(event.pos()))
        super(CustomGraphicsView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        print("in mouseReleaseEvent")
        if event.button() == Qt.LeftButton:
            print("checkking", self)
            pos_in_image = self.mapToScene(event.pos())
            pixel_x = int(pos_in_image.x())
            pixel_y = int(pos_in_image.y())
            self.event_click = (pixel_x, pixel_y)
            self.parent().mouseReleaseEvent(event)  # Forward the event to the parent (CustomMainWindow)
        super(CustomGraphicsView, self).mouseReleaseEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        # Get the position of the wheel event in the view
        wheel_pos = event.pos()

        # Map the wheel position to the scene coordinates
        pos_in_scene_before_zoom = self.mapToScene(wheel_pos)

        # Zoom with the mouse wheel
        factor = 1.2 if event.angleDelta().y() > 0 else 1.0 / 1.2

        self.zoom_factor *= factor
        self.setTransform(QTransform.fromScale(self.zoom_factor, self.zoom_factor))

        # Map the wheel position to the scene coordinates after zoom
        pos_in_scene_after_zoom = self.mapToScene(wheel_pos)
        # pos_in_scene_after_zoom = wheel_pos
        # print(pos_in_scene_after_zoom)
        # Adjust the view center to keep the cursor position fixed
        delta = pos_in_scene_after_zoom - pos_in_scene_before_zoom
        # print(delta.x(), delta.y())
        # print("checkkking")
        self.centerOn(pos_in_scene_after_zoom)

        # Continue with the default behavior
        super().wheelEvent(event)

        

#TODO: code save button
#TODO: code unsave button
#TODO: code reset button

def main():
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
