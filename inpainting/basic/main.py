import cv2 as cv
import numpy as np
import scipy
import matplotlib.image as mpimg

from ttictoc import tic,toc

### Create image and mask
def create_image_and_mask(imagefilename,maskfilename):

    # import a clean input to be corrupted with the mask 
    input = mpimg.imread(imagefilename)
    
    if input.ndim==3:
        M,N,C = input.shape
    else:
        M,N = input.shape
        C = 1
    
    # import the mask of the inpainting domain
    # mask = 1 intact part
    # mask = 0 missing domain
    mask  = scipy.float64((mpimg.imread(maskfilename) == 1));
    
    if (input.ndim==3) & (mask.ndim<3):
        mask = np.repeat(mask[:, :, np.newaxis], C, axis=2)
    
    if C==1:
        input = scipy.expand_dims(input, axis=2)
        mask  = scipy.expand_dims(mask, axis=2)
        
    # create the image with the missin domain:
    noise = scipy.random.rand(M,N,C)      
    u     = mask*input + (1-mask)*noise;
    u = np.clip(u, 0, 1)
    return (u,mask)


### Harmonic Inpainting
def harmonic(input,mask,fidelity,tol,maxiter,dt):

    if input.ndim==3:
        M,N,C = input.shape
    else:
        M,N = input.shape
        C = 1

    u = input.copy()

    for c in range(0,C):
    
        for iter in range(0,maxiter):
    
            # COMPUTE NEW SOLUTION
            laplacian = cv.Laplacian(u[:,:,c],cv.CV_64F)
            unew = u[:,:,c] + dt*( laplacian + fidelity * mask[:,:,c] * (input[:,:,c]-u[:,:,c]) )
    
            # exit condition
            diff_u = np.linalg.norm(unew.reshape(M*N,1)-u[:,:,c].reshape(M*N,1),2)/np.linalg.norm(unew.reshape(M*N,1),2); 

            # update
            u[:,:,c] = unew
     
            # test exit condition
            if diff_u<tol:
                break
    
    u = np.clip(u, 0, 1)
    print(u)
    mpimg.imsave("harmonic_output.png", u)
    
    return u




### Harmonic Inpainting

# create the corrupted image with the mask
cleanfilename = './data/nature_corrupted.png';
maskfilename  = './data/nature_mask.png';
input,mask    = create_image_and_mask(cleanfilename,maskfilename);
mpimg.imsave("./data/nature_input.png", input)

# parameters
fidelity      = 10;
tol           = 1e-5;
maxiter       = 500;
dt            = 0.1;

# inpainting
tic()
u = harmonic(input,mask,fidelity,tol,maxiter,dt)
print('Elasped time is:',toc())