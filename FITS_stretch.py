import matplotlib.pyplot as plt
from astropy.io import fits
import astropy.visualization as viz
import numpy as np

output=[]
#logrithmic stretch and normalization
def log(image_name):
    trial=1
    while(trial!=0):  
        try:
            try:
                hdul=fits.open(image_name)
            except(ValueError,FileNotFoundError):
                image_name=input("\nfile missing or empty file name !!! \nPlease re-enter file name : ")
                hdul=fits.open(image_name)
            hdul.info()
            header_number=int(input("Enter Header number whose data  you want view : "))
            image=hdul[header_number].data
            hdul.close()
            #printing stats about the data
            print("\n"," Minimum Value = ",np.min(image),"\t Maximum Value = ",np.max(image),"\t Meadian Value = ",np.median(image))
            flag=1
            total_count=1
            previous_parameter=0
            while(flag!= 0):
                ##stretching and normalizing using LogStretch() and MinMaxInterval() like in DS9
                log_param=float(input("Enter base value for logrithmic stretch : "))
                norm=viz.ImageNormalize(image,vmin=((np.median(image))**2-abs(np.min(image))),vmax=50,stretch=viz.LogStretch(log_param))
                if total_count>1:
                    plt.subplot(1,2,1)
                    norm=viz.ImageNormalize(image,vmin=((np.median(image))**2-abs(np.min(image))),vmax=50,stretch=viz.LogStretch(log_param))
                    plt.imshow(image,cmap='gray',norm=norm)
                    plt.title('a='+str(log_param))
                    plt.grid(True)
                    plt.subplot(1,2,2)
                    log_param=previous_parameter
                    norm=viz.ImageNormalize(image,vmin=((np.median(image))**2-abs(np.min(image))),vmax=50,stretch=viz.LogStretch(log_param))
                    plt.imshow(image,cmap='gray',norm=norm)
                    plt.title('a='+str(previous_parameter))
                    plt.grid(True)
                else:
                    plt.imshow(image,cmap='gray',norm=norm)
                plt.show()
                ch=input("Are you happy with your choice of log_parameters(Y/N) : ")
                if ch=='Y' or ch=='y':
                    flag=0
                    print("Stretched Image stored temporarily!!! \n")
                    output=norm(image)
                   
                else:
                    flag=1 
                    total_count+=1
                    previous_parameter=log_param 
            trial=0
            return output
        except(TypeError):
            print("INCORRECT header chosen for viewing the data !!!! ")
            print("Please enter correct header number!!!\n")
        except(IndexError):
            print("HEADER UNIT not found!!!\nPlease recheck!!!\n")
        
