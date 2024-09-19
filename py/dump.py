import numpy as np
import cv2

image = None

def SetPoint(x, y):
    p = np.array([[x], [y], [1]])
    return p

def W2L(x, y):
    xl = x+300
    yl = 300-y
    return int(xl), int(yl)

def MatKali(M1, M2):
    Mo = np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                Mo[i,j] = Mo[i,j] + M1[i,k] * M2[k,j]
    return Mo

def Transformasi(M, P):
    Po = np.matmul(M,P)
    return Po

def D2R(sd):
    return sd / 180 * np.pi

def MatRotasi(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    R = np.array([[c, -s, 0],
                  [s, c, 0],
                  [0, 0, 1]])
    return R

def MatTranslasi(dx, dy):
    T = np.array([[1, 0, dx],
                  [0, 1, dy],
                  [0, 0, 1]])
    return T

def MatSkala(Sx, Sy):
    S = np.array([[Sx, 0, 0],
                  [0, Sy, 0],
                  [0, 0, 1]])
    return S

def Garis(pa, pk):
    global image
    xl1, yl1 = W2L(pa[0,0], pa[1,0])
    xl2, yl2 = W2L(pk[0,0], pk[1,0])
    
    start_point = (xl1, yl1)
    end_point = (xl2, yl2)
    cv2.line(image, start_point, end_point, (0, 0, 255), 2)

def Kubus(m, u):
    p1 = SetPoint(-u, -u)
    p2 = SetPoint(u, -u)
    p3 = SetPoint(u, u)
    p4 = SetPoint(-u, u)

    print(m)
    print("=======")
    print(p1)   
    print("aiudgsaidgasiudgasiudu")

    p1a = Transformasi(m, p1)
    p2a = Transformasi(m, p2)
    p3a = Transformasi(m, p3)
    p4a = Transformasi(m, p4)
    Garis(p1a, p2a)
    Garis(p2a, p3a)
    Garis(p3a, p4a)
    Garis(p4a, p1a)
sd = 0


while True:
    sd = sd + 0.01
    image = np.zeros((600, 600, 3), dtype=np.uint8)
    Garis(SetPoint(-300, 0), SetPoint(300, 0))
    Garis(SetPoint(0, -300), SetPoint(0, 300))
    M = MatSkala(1, 1)
    M = MatKali(M, MatRotasi(sd))
    Kubus(M, 40)
    M=MatKali(M,MatRotasi(sd))
    M=MatKali(M,MatTranslasi(150,0))
    M=MatKali(M,MatRotasi(sd))
    Kubus(M,30)
    M=MatKali(M,MatRotasi(sd))
    M=MatKali(M,MatTranslasi(105,0))
    M=MatKali(M,MatRotasi(sd))
    Kubus(M,20)
    M=MatKali(M,MatRotasi(sd))
    M=MatKali(M,MatTranslasi(60,0))
    M=MatKali(M,MatRotasi(sd))
    Kubus(M,10)
    M=MatKali(M,MatRotasi(sd))
    M=MatKali(M,MatTranslasi(40,0))
    M=MatKali(M,MatRotasi(sd))
    Kubus(M,5)
    cv2.imshow('RedLine', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()