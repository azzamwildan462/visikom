import numpy as np 
import cv2

p=np.array([[36,44,1],
            [364,83,1],
            [25,277,1],
            [374,259,1]])

pa=np.array([[0,0,1],
            [400,0,1],
            [0,200,1],
            [400,200,1]])
M=np.zeros((8,9))
gj =[0,2,4,6]

M[gj,0]=p[:,0]
M[gj,1]=p[:,1]
M[gj,2]=1
M[gj,6]=-p[:,0]*pa[:,0]
M[gj,7]=-p[:,1]*pa[:,0]
M[gj,8]=-pa[:,0]

gn =[1,3,5,7]


M[gn,3]=p[:,0]
M[gn,4]=p[:,1]
M[gn,5]=1
M[gn,6]=-p[:,0]*pa[:,1]
M[gn,7]=-p[:,1]*pa[:,1]
M[gn,8]=-pa[:,1]

U, S, VT = np.linalg.svd(M)
V= VT.transpose() 

H= V[:,8].reshape(3, 3)
Hi = np.linalg.inv(H)
paa = np.matmul(H,p.transpose() )

paa = paa.transpose() 
paa[0,:]=paa[0,:]/paa[0,2]
paa[1,:]=paa[1,:]/paa[1,2]
paa[2,:]=paa[2,:]/paa[2,2]
paa[3,:]=paa[3,:]/paa[3,2]


pj=([0,0,1],[431,0,1],[431,323,1],[0,323,1])
pj= np.array(pj).transpose() 

pja= np.matmul(H,pj) 

for i  in range(4):
    pja[:,i]=pja[:,i]/pja[2,i]
    
xmin = pja[0,:].min() 
xmax = pja[0,:].max()
ymin = pja[1,:].min() 
ymax = pja[1,:].max()
w = np.int32(xmax -xmin )+1
h = np.int32(ymax - ymin) +1


ImA = np.zeros((h,w))


# Read the image and convert it to grayscale
image =np.double( cv2.imread('gb.png', cv2.IMREAD_GRAYSCALE))/255




for i  in range(h):
    for j in range(w):
        pa =np.array([[j+xmin,i+ymin,1]] )
        pa =pa.transpose() 
        p= np.matmul(Hi,pa)
        
        
        p =np.int32( p[:,0]/p[2,0])
        if p[0]>=0 and p[0]<image.shape[1] and p[1]>0 and p[1]<image.shape[0] : 
            ImA[i,j]=image[p[1],p[0]]
        
        

        
        print(p)
        
    




# Display the original and labeled images
cv2.imshow('Original', image)
cv2.imshow('ImA', ImA)
cv2.waitKey(0)
cv2.destroyAllWindows()




