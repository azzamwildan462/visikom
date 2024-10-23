import cv2
import numpy as np

# Fungsi untuk menyatukan dua gambar menggunakan homografi
def stitch_images(img1, img2):
    # Konversi gambar ke grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Inisialisasi SIFT untuk mendeteksi keypoints dan descriptor
    sift = cv2.SIFT_create()

    # Deteksi keypoints dan deskriptor
    keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

    # Inisialisasi matcher
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    # Cocokkan deskriptor antara dua gambar
    matches = bf.match(descriptors1, descriptors2)
    
    # Urutkan berdasarkan jarak
    matches = sorted(matches, key=lambda x: x.distance)

    # Ambil poin keypoints yang cocok
    src_pts = np.float32([keypoints1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # Hitung homografi
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # Ukuran gambar panorama
    width_panorama = img1.shape[1] + img2.shape[1]
    height_panorama = img1.shape[0]

    # Terapkan homografi dan gabungkan gambar
    panorama = cv2.warpPerspective(img1, H, (width_panorama, height_panorama))
    panorama[0:img2.shape[0], 0:img2.shape[1]] = img2

    return panorama

# Baca dua gambar
img1 = cv2.imread(r'C:\Users\Windows\OneDrive - Institut Teknologi Sepuluh Nopember\Semester 2\Visi Komputer\07_Pertemuan Ke-7 - Panorama\kanan.jpg')
img2 = cv2.imread(r'C:\Users\Windows\OneDrive - Institut Teknologi Sepuluh Nopember\Semester 2\Visi Komputer\07_Pertemuan Ke-7 - Panorama\kiri.jpg')


# Buat panorama
result = stitch_images(img1, img2)

# Simpan hasilnya
cv2.imwrite('panorama_result.jpg', result)

# Tampilkan gambar panorama
cv2.imshow('Panorama', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
