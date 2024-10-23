import cv2
import numpy as np
import time

# Fungsi untuk menyatukan dua gambar menggunakan homografi
def stitch_images(img1, img2):
    # Konversi gambar ke grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()

    kp1, dc1 = sift.detectAndCompute(gray1, None)
    kp2, dc2 = sift.detectAndCompute(gray2, None)

    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    matches = bf.match(dc1, dc2)
    matches = sorted(matches, key=lambda x: x.distance)

    # Korespondensi satu satu
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    h, w, _ = img2.shape
    pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, H)


    h1, w1, _ = img1.shape
    # Define the corners of img1 and transform them using the homography matrix
    pts1 = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]]).reshape(-1, 1, 2)
    pts1_transformed = cv2.perspectiveTransform(pts1, H)

    # Calculate the overlap area width (slice area width)
    overlap_x = max(0, np.min(pts1_transformed[:, 0, 0]))  # Minimum x-coordinate of transformed img1

    slice_width = w1 - overlap_x

    print(slice_width)

    # Ukuran gambar panorama
    width_panorama = img1.shape[1] + img2.shape[1]
    height_panorama = img1.shape[0]

    # Terapkan homografi dan gabungkan gambar
    panorama = cv2.warpPerspective(img1, H, (width_panorama, height_panorama))
    # panorama = cv2.warpPerspective(img2, H, (width_panorama, height_panorama))
    panorama[0:img2.shape[0], 0:img2.shape[1]] = img2

    # panorama = cv2.polylines(panorama, [np.int32(dst)], True, (0, 255, 0), 3, cv2.LINE_AA)
    # panorama = cv2.polylines(panorama, [np.int32(dst1)], True, (255, 0, 255), 3, cv2.LINE_AA)


    return panorama

# Baca dua gambar
img1 = cv2.imread("./gb_n2.jpeg")
img2 = cv2.imread("./gb_n1.jpeg")


# Get time now 
start = time.time()

# Calc
result = stitch_images(img1, img2)

# Get time after panorama
end = time.time()

# Print time elapsed in seconds
print("Time elapsed: ", end - start)

# Tampilkan gambar panorama


while(True):
    cv2.imshow('img1', img1)
    cv2.imshow('img2', img2)
    cv2.imshow('Panorama', result)
    cv2.waitKey(20)
cv2.destroyAllWindows()
