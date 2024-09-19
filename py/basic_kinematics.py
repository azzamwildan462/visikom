import cv2
import numpy as np
image =None

image_width = 800
image_height = 800

def SetPoint(x ,y,z):
    p=np.array([[x],[y],[z],[1]])
    return p 

def MatKali(M1,M2):
    Mo = np.matmul(M1,M2)
    return Mo.copy() 

def Transformasi(M,P):
    Po = np.matmul(M,P)
    return Po
    
def D2R(capit_link_ar):
    return capit_link_ar/180 *np.pi 

def MatRz(Teta):
    c = np.cos(Teta)
    s = np.sin(Teta)
    m=np.array([[c,-s,0,0],
                [s,c,0,0],
                [0,0,1,0],
                [0,0,0,1]])
    return m.copy() 

def MatRy(Teta):
    c = np.cos(Teta)
    s = np.sin(Teta)
    m=np.array([[c,0,s,0],
                [0,1,0,0],
                [-s,0,c,0],
                [0,0,0,1]])
    return m.copy() 

def MatRx(Teta):
    c = np.cos(Teta)
    s = np.sin(Teta)
    m=np.array([[1,0,0,0],
                [0,c,-s,0],
                [0,s,c,0],
                [0,0,0,1]])
    return m.copy() 

def MatTranslasi(dx,dy,dz):
    m=np.array([[1,0,0,dx],
                [0,1,0,dy],
                [0,0,1,dz],
                [0,0,0,1]])
    return m 
    
def MatSkala(sx,sy,sz):
    m=np.array([[sx,0,0,0],
                [0,sy,0,0],
                [0,0,sz,0],
                [0,0,0,1]])
    return m.copy() 
    
def W2L(x,y):
    xl=x+image_width/2
    yl=image_height/2-y
    return  int(xl),int(yl)  
    
def Garis(pa,pk,  color = (0, 0, 255) ):
    global image 
    xl1,yl1 = W2L(pa[0,0],pa[1,0])
    xl2,yl2 = W2L(pk[0,0],pk[1,0]) 

    start_point = (xl1, yl1)  # Titik awal (x, y)
    end_point = (xl2, yl2)   # Titik akhir (x, y)
   # Merah (BGR)
    thickness = 2
    # print(int(xl1),int(xl2))
    cv2.line(image, start_point, end_point, color, thickness)
    
def Kubus(m,x,y,z,color = (0, 0, 255) ):
    l=[]
    p1=SetPoint(-x, -y,-z)
    p2=SetPoint(x, -y,-z)
    p3=SetPoint(x, y,-z)
    p4=SetPoint(-x, y,-z)
    l.append((p1,p2,p3,p4))

    p1=SetPoint(-x, -y,z)
    p2=SetPoint(x, -y,z)
    p3=SetPoint(x, y,z)
    p4=SetPoint(-x, y,z)
    l.append((p1,p2,p3,p4))
    
    p1=SetPoint(-x, -y,-z)
    p2=SetPoint(-x, y,-z)
    p3=SetPoint(-x, y,z)
    p4=SetPoint(-x, -y,z)
    l.append((p1,p2,p3,p4))
    
    p1=SetPoint(x, -y,-z)
    p2=SetPoint(x, y,-z)
    p3=SetPoint(x, y,z)
    p4=SetPoint(x, -y,z)
    l.append((p1,p2,p3,p4))
    
    p1=SetPoint(-x, -y,-z)
    p2=SetPoint(x, -y,-z)
    p3=SetPoint(x, -y,z)
    p4=SetPoint(-x, -y,z)
    l.append((p1,p2,p3,p4))
    
    p1=SetPoint(-x, y,-z)
    p2=SetPoint(x, y,-z)
    p3=SetPoint(x, y,z)
    p4=SetPoint(-x, y,z)
    l.append((p1,p2,p3,p4))

    for p in l:
        p1 = p[0]
        p2 = p[1]
        p3 = p[2]
        p4 = p[3]
        # print(m)
        p1a = Transformasi(m, p1)
        p2a = Transformasi(m, p2)
        p3a = Transformasi(m, p3)
        p4a = Transformasi(m, p4)
        Garis(p1a,p2a,color = color)
        Garis(p2a,p3a,color =  color)
        Garis(p3a,p4a,color =  color)
        Garis(p4a,p1a,color =  color)
    
def DrawSumbu(m, color = (0, 0, 255)):
    Garis(Transformasi(m,SetPoint(-1200,0,0)),Transformasi(m,SetPoint(1200,0,0)),color = color)
    Garis(Transformasi(m,SetPoint(0,-1200,0)),Transformasi(m,SetPoint(0,1200,0)),color = color)

def Lengan(M,pj,lb,t):
    M=MatKali(M, MatSkala(pj, lb, t))
    M=MatKali(M, MatSkala(0.5, 0.5, 0.5))
    M=MatKali(M, MatTranslasi(1, 0, 0))
    Kubus(M,1,1,1,color=(0,255,0))

# LINK 
# INI ABSOLUTE TERHADAP WORLD MODEL
# ===============
capit_link_ar = 0

body_link_px = 0
body_link_py = 0
body_link_pz = 0

body_link_ar = 0
body_link_ap = 0
body_link_ay = 0

map_link_ap = -60
map_link_ay = 45

lengan_1_link_ap = 0
lengan_2_link_ap = 0
lengan_3_link_ap = 0

px_local_robot = 0
py_local_robot = 0

while True:

    key = cv2.waitKey(1) & 0xFF

    if key != 255: # Ketika keyboard ditekan
        if key == 113: # Tombol 'q'
            capit_link_ar += 5
            if capit_link_ar > 30:
                capit_link_ar = 30
            elif capit_link_ar < -30:
                capit_link_ar = -30
        elif key == 119: # Tombol 'w'
            capit_link_ar -= 5
            if capit_link_ar > 30:
                capit_link_ar = 30
            elif capit_link_ar < -30:
                capit_link_ar = -30
        elif key == 97: # Tombol 'a'
            body_link_px += 5
        elif key == 115: # Tombol 's'
            body_link_py += 5
        elif key == 100: # Tombol 'd'
            body_link_pz += 5
        elif key == 122: # Tombol 'z'
            body_link_px -= 5
        elif key == 120: # Tombol 'x'
            body_link_py -= 5
        elif key == 99: # Tombol 'c'
            body_link_pz -= 5

        elif key == 102:
            body_link_ar += 5
        elif key == 103:
            body_link_ap += 5
        elif key == 104:
            body_link_ay += 5
        elif key == 118:
            body_link_ar -= 5
        elif key == 98:
            body_link_ap -= 5
        elif key == 110:
            body_link_ay -= 5
        
        # j, m
        elif key == 106:
            lengan_3_link_ap += 5
        elif key == 109:
            lengan_3_link_ap -= 5

        # i, k
        elif key == 105:
            lengan_2_link_ap += 5
        elif key == 107:
            lengan_2_link_ap -= 5

        # o, l
        elif key == 111:
            # lengan_1_link_ap += 5
            body_link_px -= 5 * np.cos(D2R(body_link_ay))
            body_link_py -= 5 * np.sin(D2R(body_link_ay))
        elif key == 108:
            # lengan_1_link_ap -= 5
            body_link_px += 5 * np.cos(D2R(body_link_ay))
            body_link_py += 5 * np.sin(D2R(body_link_ay))
        
    image = np.zeros((image_width, image_height, 3), dtype=np.uint8)
    M = MatSkala(1, 1, 1)
    M = MatKali(M, MatRx(D2R(map_link_ap)))
    M = MatKali(M, MatRz(D2R(map_link_ay)))

    # Gambar sumbu
    # ===============
    if body_link_pz >= 0:
        DrawSumbu(M, color=(0, 0, 100))

    # Draw objek
    # ===============
    M = MatKali(M, MatTranslasi(body_link_px, body_link_py, body_link_pz))   # Movement base link
    M = MatKali(M, MatTranslasi(50, 0, 25))   # Pindah center rotasi ke tengah body
    M = MatKali(M, MatRy(D2R(body_link_ar)))
    M = MatKali(M, MatRx(D2R(body_link_ap)))
    M = MatKali(M, MatRz(D2R(body_link_ay)))
    M = MatKali(M, MatTranslasi(-50, 0, -25))   # Pindah center rotasi ke tengah body

    Lengan(M, 100, 50, 50)
    M = MatKali(M, MatRy(D2R(-135 + lengan_1_link_ap)))

    # Lengan kedua
    # ===============
    Lengan(M, 100, 10, 10)
    M = MatKali(M, MatTranslasi(100, 0, 0))

    # # Lengan ketiga
    # ===============
    M = MatKali(M, MatRy(D2R(-45 + lengan_2_link_ap)))
    Lengan(M, 100, 10, 10)

    # Untuk capit
    # ===============
    M = MatKali(M, MatTranslasi(100, 0, 0))
    M = MatKali(M, MatRy(D2R(lengan_3_link_ap)))

    # # Lengan 4 untuk capit atas
    # ===========================
    M_capitA = MatKali(M, MatRy(D2R(-45 + capit_link_ar)))  
    Lengan(M_capitA, 50, 10, 10)    

    # # Lengan 5 untuk capit bawah
    # ============================
    M_capitB = MatKali(M, MatRy(D2R(45 - capit_link_ar)))  
    Lengan(M_capitB, 50, 10, 10)

    if body_link_pz < 0:
        M = MatSkala(1, 1, 1)
        M = MatKali(M, MatRx(D2R(-60)))
        M = MatKali(M, MatRz(D2R(45)))
        DrawSumbu(M)

    # Tampilkan gambar
    cv2.imshow('Capit', image)

cv2.destroyAllWindows()