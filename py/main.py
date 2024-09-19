# Menggunakan OpenCV untuk menampilkan gambar
# Menggunakan semi-oop untuk mempermudah

import numpy as np
import cv2

# I'm falling in love with my RMS timer 
import threading
import time
import pandas as pd

from loguru import logger

CENTER_X = 300
CENTER_Y = 300
RAD2DEG = 57.29577951308232
DEG2RAD = 0.017453292519943295

class Main:
    def __init__(self):
        logger.info("Main class initialized")
        self.image_buffer = np.zeros((600, 600, 3), np.uint8)

        # Initialize objects
        self.init_objs()

        # Thread
        # ------
        self.routine = threading.Thread(target=self.callback_RMSroutine50hz, daemon=True)
        self.routine.start()

    # ============================================================================================

    def set_point(self, x, y):
        return np.array([[x], [y], [1]])
    
    def set_point_polar(self, r, theta):
        theta = theta * DEG2RAD
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return np.array([[x], [y], [1]])

    def transform(self, m, p):
        return np.matmul(m, p)
    
    def rotate(self, theta):
        theta = theta * DEG2RAD
        c = np.cos(theta)
        s = np.sin(theta)
        return np.array([[c, -s, 0],
                         [s, c, 0],
                         [0, 0, 1]])
    
    def rotate_with_center(self, theta, center):
        theta = theta * DEG2RAD
        c = np.cos(theta)
        s = np.sin(theta)

        # Translation matrix to move to the origin
        translation_to_origin = np.array([[1, 0, -center[0]],
                                        [0, 1, -center[1]],
                                        [0, 0, 1]])
        
        # Rotation matrix
        rotation_matrix = np.array([[c, -s, 0],
                                    [s, c, 0],
                                    [0, 0, 1]])
        
        # Translation matrix to move back to the original position
        translation_back = np.array([[1, 0, center[0]],
                                    [0, 1, center[1]],
                                    [0, 0, 1]])
        
        # Combine the transformations: translate -> rotate -> translate back
        transformation_matrix = np.matmul(translation_back, np.matmul(rotation_matrix, translation_to_origin))
        
        return transformation_matrix

    def translate(self, dx, dy):
        return np.array([[1, 0, dx],
                         [0, 1, dy],
                         [0, 0, 1]])
    
    def scale(self, sx, sy):
        return np.array([[sx, 0, 0],
                         [0, sy, 0],
                         [0, 0, 1]])
    
    def line(self, pa, pk):
        xl1, yl1 = self.world_to_local(pa[0,0], pa[1,0])
        xl2, yl2 = self.world_to_local(pk[0,0], pk[1,0])

        start_point = (xl1, yl1)
        end_point = (xl2, yl2)
        cv2.line(self.image_buffer, start_point, end_point, (0, 0, 255), 2)
    
    def world_to_local(self, x, y):
        xl = x + CENTER_X
        yl = CENTER_Y - y
        return int(xl), int(yl)
    
    def create_polygon(self, n_corners, r):
        points = np.zeros((n_corners,3,1))
        for i in range(n_corners):
            theta = (360 / n_corners) * i
            x = r * np.cos(theta * DEG2RAD)
            y = r * np.sin(theta * DEG2RAD)
            points[i] = self.set_point(x, y)
        
        return points
    
    def process_polygon(self, obj, n_corners, r):
        o_corners = self.create_polygon(n_corners, r)
        ret_buffer = np.zeros((n_corners,3,1))
        for i in range(n_corners):
            ret_buffer[i] = self.transform(obj, o_corners[i])

        return ret_buffer

    
    def init_objs(self):
        self.obj1 = self.scale(1, 1)
        self.obj1 = self.set_point(100, 90)

        self.obj2 = self.scale(1, 1)
        self.obj2 = self.set_point_polar(200, 45)

        self.o3_x = 100
        self.o3_y = 90

        self.obj3 = self.scale(1,1)
        self.obj3 = self.set_point(self.o3_x,self.o3_y)
        self.arah_gerak_o3_kanan = True

        self.obj4 = self.scale(1, 1)
        self.obj4 = self.transform(self.translate(100,-20), self.obj4)
        self.o4_n = 3
        self.o4_r = 45
        self.o4_corner = self.create_polygon(self.o4_n, self.o4_r)
        self.obj4_trans = np.zeros((self.o4_n,3,1))
        for i in range(self.o4_n):
            self.obj4_trans[i] = self.transform(self.obj4, self.o4_corner[i])
        self.o4_diperbesar = True
        self.o4_real_r = self.o4_r
        self.o4_acc = 0
        self.o4_vel_theta = 0

        self.obj5 = self.scale(1, 1)
        self.obj5 = self.transform(self.translate(-200,-200), self.obj5)
        self.obj5_trans = self.process_polygon(self.obj5, 4, 45)
        self.o5_vel_trans = 0
        self.o5_acc = 0
        self.o5_jerk = 0
        self.o5_status_naik = True


    # ============================================================================================

    def callback_RMSroutine50hz(self):
        # RMS routine
        # -----------
        period = 19 # ms                                         # 50 hz control rate

        while(1):
            t1 = pd.Timestamp.now()
            self.callback_routine()
            t2 = pd.Timestamp.now()
            elapsed_time = (t2 - t1).total_seconds() * 1000

            if elapsed_time < period:
                time.sleep((period - elapsed_time) / 1000)
            else:
                # logger.warning("RMS routine 50hz took too long: {} ms".format(elapsed_time))
                time.sleep(period / 1000)
    
    def callback_routine(self):
        # Clear image buffer
        self.image_buffer = np.zeros((600, 600, 3), np.uint8)

        # Draw axis
        cv2.line(self.image_buffer, (0, CENTER_Y), (600, CENTER_Y), (255, 255, 255), 1)
        cv2.line(self.image_buffer, (CENTER_X, 0), (CENTER_X, 600), (255, 255, 255), 1)


        # Move objects
        self.obj1 = self.transform(self.rotate(1), self.obj1)
        self.obj2 = self.transform(self.rotate_with_center(20,(self.obj1[0][0],self.obj1[1][0])), self.obj2)

        # Move o3
        if self.o3_x > 200:
            self.arah_gerak_o3_kanan = False
        elif self.o3_x < -200:
            self.arah_gerak_o3_kanan = True

        if self.arah_gerak_o3_kanan:
            self.obj3 = self.transform(self.translate(10,0), self.obj3)
        else:
            self.obj3 = self.transform(self.translate(-10,0), self.obj3)
        
        self.o3_x = self.obj3[0][0]
        self.o3_y = self.obj3[1][0]

        # Move o4
        if self.o4_real_r > 250:
            self.o4_diperbesar = False
            self.o4_n += 1
        elif self.o4_real_r < 100:
            self.o4_diperbesar = True
            self.o4_n += 1

        if self.o4_diperbesar:
            self.obj4 = self.transform(self.scale(1.01,1.01), self.obj4)
            self.o4_acc = 0.2
        if not self.o4_diperbesar:
            self.obj4 = self.transform(self.scale(0.99,0.99), self.obj4)
            self.o4_acc = -0.156
        
        self.o4_vel_theta += self.o4_acc

        self.obj4 = self.transform(self.rotate(self.o4_vel_theta), self.obj4)
        self.obj4_trans = self.process_polygon(self.obj4, self.o4_n, self.o4_r)

        # Mencari radius terbesar
        max_r = 0
        for i in range(self.o4_n):
            r_now = np.sqrt(self.obj4_trans[i][0][0] ** 2 + self.obj4_trans[i][1][0] ** 2)
            if r_now > max_r:
                max_r = r_now
        
        self.o4_real_r = max_r

        # Move o5

        # print(self.obj5_trans[0][1][0])
        if self.obj5_trans[0][1][0] > -100:
            self.o5_status_naik = False
        elif self.obj5_trans[0][1][0] < 100:
            self.o5_status_naik = True

        # print(self.o5_status_naik)
        if self.o5_status_naik:
            self.o5_jerk = 0.234
        else:
            self.o5_jerk = -0.234

        self.o5_acc += self.o5_jerk

        if self.o5_vel_trans > 2:
            self.o5_vel_trans = 2
        if self.o5_vel_trans < -2:
            self.o5_vel_trans = -2

        self.o5_vel_trans += self.o5_acc

        if self.o5_vel_trans > 10:
            self.o5_vel_trans = 10
        if self.o5_vel_trans < -10:
            self.o5_vel_trans = -10
        
        # print(self.o5_vel_trans)
        self.obj5 = self.transform(self.translate(0,self.o5_vel_trans), self.obj5)
        self.obj5_trans = self.process_polygon(self.obj5, 4, 45)

        # Draw objects 
        cv2.circle(self.image_buffer, self.world_to_local(self.obj1[0][0],self.obj1[1][0]), 5, (0, 255, 0), -1)
        cv2.circle(self.image_buffer, self.world_to_local(self.obj2[0][0],self.obj2[1][0]), 5, (255, 0, 0), -1)
        cv2.circle(self.image_buffer, self.world_to_local(self.obj3[0][0],self.obj3[1][0]), 5, (0, 0, 255), -1)

        # Draw o4 
        for i in range(self.o4_n):
            start_point = self.world_to_local(self.obj4_trans[i][0],self.obj4_trans[i][1])
            end_point = self.world_to_local(self.obj4_trans[(i+1) % self.o4_n][0], self.obj4_trans[(i+1)% self.o4_n][1])
            cv2.line(self.image_buffer, start_point, end_point, (255, 0, int(self.o4_real_r)), 2)
        
        # Draw o5
        for i in range(4):
            start_point = self.world_to_local(self.obj5_trans[i][0],self.obj5_trans[i][1])
            end_point = self.world_to_local(self.obj5_trans[(i+1) % 4][0], self.obj5_trans[(i+1)% 4][1])
            cv2.line(self.image_buffer, start_point, end_point, (0, 255, 0), 3)


        # Show image 
        cv2.imshow("Image", self.image_buffer)
        cv2.waitKey(1)
    
    # ============================================================================================


if __name__ == "__main__":
    main = Main()
    while True:
        pass


