import auxil.auxil as auxil
import numpy as np 
from osgeo import gdal   
from osgeo.gdalconst import GA_ReadOnly,GDT_Float32
import matplotlib.pyplot as plt
from pylab import *
import gc
import os


# Open a pre-classified image
in_path = auxil.select_infile(title="Choosing the input file directory")
gdal.AllRegister()
raw_image = gdal.Open(in_path,GA_ReadOnly)
try:
    cols = raw_image.RasterXSize
    rows = raw_image.RasterYSize
    bands = raw_image.RasterCount
except StandardError, e:
    print "Error: It is not an image"



# Get the spatial reference of the input image
projInfo = raw_image.GetProjection()
transInfo = raw_image.GetGeoTransform()


# Read the image as an array
pre_classified = raw_image.ReadAsArray(0, 0, cols, rows)



# Starting from the 2nd row and 2nd col
i = 1
j = 1
M = 1
while M <= 10:   # run 10 iterations
    while i < rows - 1:
        while j < cols - 1:
            if pre_classified[i,j] == 1:
            # If the center pixel is water
              
                # define variables to record the nearest pixel value
                W1 = 0  # water
                G1 = 0  # grass
                T1 = 0  # tree
                B1 = 0  # bare soil
                U1 = 0  # urban

                # check the pixel above the center pixel
                if pre_classified[i - 1,j] == 1:
                        W1 = W1 + 1
                if pre_classified[i - 1,j] == 2:
                        G1 = G1 + 1
                if pre_classified[i - 1,j] == 3:
                        T1 = T1 + 1
                if pre_classified[i - 1,j] == 4:
                        B1 = B1 + 1
                if pre_classified[i - 1,j] == 5:
                        U1 = U1 + 1

                # check the pixel below the center pixel
                if pre_classified[i + 1,j] == 1:
                        W1 = W1 + 1
                if pre_classified[i + 1,j] == 2:
                        G1 = G1 + 1
                if pre_classified[i + 1,j] == 3:
                        T1 = T1 + 1
                if pre_classified[i + 1,j] == 4:
                        B1 = B1 + 1
                if pre_classified[i + 1,j] == 5:
                        U1 = U1 + 1


                # check the pixel left to the center pixel
                if pre_classified[i ,j - 1] == 1:
                        W1 = W1 + 1
                if pre_classified[i ,j - 1] == 2:
                        G1 = G1 + 1
                if pre_classified[i ,j - 1] == 3:
                        T1 = T1 + 1
                if pre_classified[i ,j - 1] == 4:
                        B1 = B1 + 1
                if pre_classified[i ,j - 1] == 5:
                        U1 = U1 + 1


                # check the pixel left to the center pixel
                if pre_classified[i ,j + 1] == 1:
                        W1 = W1 + 1
                if pre_classified[i ,j + 1] == 2:
                        G1 = G1 + 1
                if pre_classified[i ,j + 1] == 3:
                        T1 = T1 + 1
                if pre_classified[i ,j + 1] == 4:
                        B1 = B1 + 1
                if pre_classified[i ,j + 1] == 5:
                        U1 = U1 + 1


                # Find the maximum value and its corresponding state
                List = [W1,G1,T1,B1,U1]
                #print List
                Maximum1 = max(List)
                index = List.index(max(List))
                #print index
                if Maximum1 < 4:    # only when the nearest pixel are the same type, will the center pixel change
                        pre_classified[i,j] = pre_classified[i,j]
                if Maximum1 == 4:  
                        if index == 0:   # the nearest pixels are all water, remain water
                                pre_classified[i,j] = 1
                        if index == 1:   # the nearest pixels are all grass, make the center pixel grass
                                pre_classified[i,j] = 2
                        if index == 2:   # the nearest pixels are all tree, make the center pixel tree
                                pre_classified[i,j] = 3
                        if index == 3:   # the nearest pixels are all bare soil, make the center pixel bare soil
                                pre_classified[i,j] = 4
                        if index == 4:   # the nearest pixels are all urban, make the center pixel urban
                                pre_classified[i,j] = 5

                                
            # If the center pixel is grass
            if pre_classified[i,j] == 2:

                # define variables to record the nearest pixel value
                W1 = 0  # water
                G1 = 0  # grass
                T1 = 0  # tree
                B1 = 0  # bare soil
                U1 = 0  # urban

                # check the pixel above the center pixel
                if pre_classified[i - 1,j] == 1:
                    W1 = W1 + 1
                if pre_classified[i - 1,j] == 2:
                    G1 = G1 + 1
                if pre_classified[i - 1,j] == 3:
                    T1 = T1 + 1
                if pre_classified[i - 1,j] == 4:
                    B1 = B1 + 1
                if pre_classified[i - 1,j] == 5:
                    U1 = U1 + 1

                # check the pixel below the center pixel
                if pre_classified[i + 1,j] == 1:
                    W1 = W1 + 1
                if pre_classified[i + 1,j] == 2:
                    G1 = G1 + 1
                if pre_classified[i + 1,j] == 3:
                    T1 = T1 + 1
                if pre_classified[i + 1,j] == 4:
                    B1 = B1 + 1
                if pre_classified[i + 1,j] == 5:
                    U1 = U1 + 1


                # check the pixel left to the center pixel
                if pre_classified[i ,j - 1] == 1:
                    W1 = W1 + 1
                if pre_classified[i ,j - 1] == 2:
                    G1 = G1 + 1
                if pre_classified[i ,j - 1] == 3:
                    T1 = T1 + 1
                if pre_classified[i ,j - 1] == 4:
                    B1 = B1 + 1
                if pre_classified[i ,j - 1] == 5:
                    U1 = U1 + 1


                # check the pixel left to the center pixel
                if pre_classified[i ,j + 1] == 1:
                    W1 = W1 + 1
                if pre_classified[i ,j + 1] == 2:
                    G1 = G1 + 1
                if pre_classified[i ,j + 1] == 3:
                    T1 = T1 + 1
                if pre_classified[i ,j + 1] == 4:
                    B1 = B1 + 1
                if pre_classified[i ,j + 1] == 5:
                    U1 = U1 + 1


                # Find the maximum value and its corresponding state
                List = [W1,G1,T1,B1,U1]
                Maximum1 = max(List)
                index = List.index(max(List))
                if Maximum1 < 3:    # only when 3 nearest pixel are the same type, will the center pixel change
                    pre_classified[i,j] = pre_classified[i,j]
                else:  
                    if index == 0:   # the nearest pixels are all water, be water
                        pre_classified[i,j] = 1
                    if index == 1:   # the nearest pixels are all grass, make the center pixel grass
                        pre_classified[i,j] = 2
                    if index == 2:   # the nearest pixels are all tree, make the center pixel tree
                        pre_classified[i,j] = 3
                    if index == 3:   # the nearest pixels are all bare soil, make the center pixel bare soil
                        pre_classified[i,j] = 4
                    if index == 4:   # the nearest pixels are all urban, make the center pixel urban
                        pre_classified[i,j] = 5

                        
            # If the center pixel is tree
            if pre_classified[i,j] == 3:
                
                # define variables to record the nearest pixel value
                W1 = 0  # water
                G1 = 0  # grass
                T1 = 0  # tree
                B1 = 0  # bare soil
                U1 = 0  # urban

                # check the pixel above the center pixel
                if pre_classified[i - 1,j] == 1:
                    W1 = W1 + 1
                if pre_classified[i - 1,j] == 2:
                    G1 = G1 + 1
                if pre_classified[i - 1,j] == 3:
                    T1 = T1 + 1
                if pre_classified[i - 1,j] == 4:
                    B1 = B1 + 1
                if pre_classified[i - 1,j] == 5:
                    U1 = U1 + 1

                # check the pixel below the center pixel
                if pre_classified[i + 1,j] == 1:
                    W1 = W1 + 1
                if pre_classified[i + 1,j] == 2:
                    G1 = G1 + 1
                if pre_classified[i + 1,j] == 3:
                    T1 = T1 + 1
                if pre_classified[i + 1,j] == 4:
                    B1 = B1 + 1
                if pre_classified[i + 1,j] == 5:
                    U1 = U1 + 1


                # check the pixel left to the center pixel
                if pre_classified[i ,j - 1] == 1:
                    W1 = W1 + 1
                if pre_classified[i ,j - 1] == 2:
                    G1 = G1 + 1
                if pre_classified[i ,j - 1] == 3:
                    T1 = T1 + 1
                if pre_classified[i ,j - 1] == 4:
                    B1 = B1 + 1
                if pre_classified[i ,j - 1] == 5:
                    U1 = U1 + 1


                # check the pixel right to the center pixel
                if pre_classified[i ,j + 1] == 1:
                    W1 = W1 + 1
                if pre_classified[i ,j + 1] == 2:
                    G1 = G1 + 1
                if pre_classified[i ,j + 1] == 3:
                    T1 = T1 + 1
                if pre_classified[i ,j + 1] == 4:
                    B1 = B1 + 1
                if pre_classified[i ,j + 1] == 5:
                    U1 = U1 + 1


                # Find the maximum value and its corresponding state
                List = [W1,G1,T1,B1,U1]
                Maximum1 = max(List)
                index = List.index(max(List))
                if Maximum1 < 3:    # only when at least 3 nearest pixels are the same type, will the center pixel change
                    pre_classified[i,j] = pre_classified[i,j]
                if Maximum1 == 3:
                    if G1 == 3:
                        pre_classified[i,j] = 2  # when 2 nearest pixels are grass, make it grass
                if Maximum1 == 4:
                    if index == 0:   # the nearest pixels are all water, be water
                        pre_classified[i,j] = 1
                    if index == 1:   # the nearest pixels are all grass, make the center pixel grass
                        pre_classified[i,j] = 2
                    if index == 2:   # the nearest pixels are all tree, make the center pixel tree
                        pre_classified[i,j] = 3
                    if index == 3:   # the nearest pixels are all bare soil, make the center pixel bare soil
                        pre_classified[i,j] = 4
                    if index == 4:   # the nearest pixels are all urban, make the center pixel urban
                        pre_classified[i,j] = 5


            # If the center pixel is bare soil           
            if pre_classified[i,j] == 4:


                # define variables to record the nearest pixel value
                W1 = 0  # water
                G1 = 0  # grass
                T1 = 0  # tree
                B1 = 0  # bare soil
                U1 = 0  # urban

                # check the pixel above the center pixel
                if pre_classified[i - 1,j] == 1:
                    W1 = W1 + 1
                if pre_classified[i - 1,j] == 2:
                    G1 = G1 + 1
                if pre_classified[i - 1,j] == 3:
                    T1 = T1 + 1
                if pre_classified[i - 1,j] == 4:
                    B1 = B1 + 1
                if pre_classified[i - 1,j] == 5:
                    U1 = U1 + 1

                # check the pixel below the center pixel
                if pre_classified[i + 1,j] == 1:
                    W1 = W1 + 1
                if pre_classified[i + 1,j] == 2:
                    G1 = G1 + 1
                if pre_classified[i + 1,j] == 3:
                    T1 = T1 + 1
                if pre_classified[i + 1,j] == 4:
                    B1 = B1 + 1
                if pre_classified[i + 1,j] == 5:
                    U1 = U1 + 1


                # check the pixel left to the center pixel
                if pre_classified[i ,j - 1] == 1:
                    W1 = W1 + 1
                if pre_classified[i ,j - 1] == 2:
                    G1 = G1 + 1
                if pre_classified[i ,j - 1] == 3:
                    T1 = T1 + 1
                if pre_classified[i ,j - 1] == 4:
                    B1 = B1 + 1
                if pre_classified[i ,j - 1] == 5:
                    U1 = U1 + 1


                # check the pixel left to the center pixel
                if pre_classified[i ,j + 1] == 1:
                    W1 = W1 + 1
                if pre_classified[i ,j + 1] == 2:
                    G1 = G1 + 1
                if pre_classified[i ,j + 1] == 3:
                    T1 = T1 + 1
                if pre_classified[i ,j + 1] == 4:
                    B1 = B1 + 1
                if pre_classified[i ,j + 1] == 5:
                    U1 = U1 + 1


                # Find the maximum value and its corresponding state
                List = [W1,G1,T1,B1,U1]
                Maximum1 = max(List)
                index = List.index(max(List))
                if Maximum1 < 3:    # only when the nearest pixel are the same type, will the center pixel 
                    pre_classified[i,j] = pre_classified[i,j]
                if Maximum1 == 3:
                    if U1 == 3:   # when 3 nearest pixels are urban, make it urban
                        pre_classified[i,j] = 5
                if Maximum1 == 4:
                    if index == 0:   # the nearest pixels are all water, be water
                        pre_classified[i,j] = 1
                    if index == 1:   # the nearest pixels are all grass, make the center pixel grass
                        pre_classified[i,j] = 2
                    if index == 2:   # the nearest pixels are all tree, make the center pixel tree
                        pre_classified[i,j] = 3
                    if index == 3:   # the nearest pixels are all bare soil, make the center pixel bare soil
                        pre_classified[i,j] = 4
                    if index == 4:   # the nearest pixels are all urban, make the center pixel urban
                        pre_classified[i,j] = 5

                        
            # If the center pixel is urban
            if pre_classified[i,j] == 5:

                # define variables to record the nearest pixel value
                W1 = 0  # water
                G1 = 0  # grass
                T1 = 0  # tree
                B1 = 0  # bare soil
                U1 = 0  # urban

                # check the pixel above the center pixel
                if pre_classified[i - 1,j] == 1:
                    W1 = W1 + 1
                if pre_classified[i - 1,j] == 2:
                    G1 = G1 + 1
                if pre_classified[i - 1,j] == 3:
                    T1 = T1 + 1
                if pre_classified[i - 1,j] == 4:
                    B1 = B1 + 1
                if pre_classified[i - 1,j] == 5:
                    U1 = U1 + 1

                # check the pixel below the center pixel
                if pre_classified[i + 1,j] == 1:
                    W1 = W1 + 1
                if pre_classified[i + 1,j] == 2:
                    G1 = G1 + 1
                if pre_classified[i + 1,j] == 3:
                    T1 = T1 + 1
                if pre_classified[i + 1,j] == 4:
                    B1 = B1 + 1
                if pre_classified[i + 1,j] == 5:
                    U1 = U1 + 1


                # check the pixel left to the center pixel
                if pre_classified[i ,j - 1] == 1:
                    W1 = W1 + 1
                if pre_classified[i ,j - 1] == 2:
                    G1 = G1 + 1
                if pre_classified[i ,j - 1] == 3:
                    T1 = T1 + 1
                if pre_classified[i ,j - 1] == 4:
                    B1 = B1 + 1
                if pre_classified[i ,j - 1] == 5:
                    U1 = U1 + 1


                # check the pixel left to the center pixel
                if pre_classified[i ,j + 1] == 1:
                    W1 = W1 + 1
                if pre_classified[i ,j + 1] == 2:
                    G1 = G1 + 1
                if pre_classified[i ,j + 1] == 3:
                    T1 = T1 + 1
                if pre_classified[i ,j + 1] == 4:
                    B1 = B1 + 1
                if pre_classified[i ,j + 1] == 5:
                    U1 = U1 + 1


                # Find the maximum value and its corresponding state
                List = [W1,G1,T1,B1,U1]
                Maximum1 = max(List)
                index = List.index(max(List))
                if Maximum1 < 3:    # only when the nearest pixel are the same type, will the center pixel 
                    pre_classified[i,j] = pre_classified[i,j]
                if Maximum1 == 3:
                    if B1 == 3:   # when 3 nearest pixels are bare soil, make it bare soil
                        pre_classified[i,j] = 4
                if Maximum1 == 4:
                    if index == 0:   # the nearest pixels are all water, be water
                        pre_classified[i,j] = 1
                    if index == 1:   # the nearest pixels are all grass, make the center pixel grass
                        pre_classified[i,j] = 2
                    if index == 2:   # the nearest pixels are all tree, make the center pixel tree
                        pre_classified[i,j] = 3
                    if index == 3:   # the nearest pixels are all bare soil, make the center pixel bare soil
                        pre_classified[i,j] = 4
                    if index == 4:   # the nearest pixels are all urban, make the center pixel urban
                        pre_classified[i,j] = 5
                    
            j = j + 1
        j = 1
        i = i + 1
    print M, "iteration(s) finished"
    i = 1
    j = 1
    M = M + 1


#   write result to disk
driver = gdal.GetDriverByName("GTiff")
outDataset = driver.Create("M:/808/Mini2/CA.tif",
                    cols,rows,bands,GDT_Float32)
outDataset.SetProjection(projInfo)
outDataset.SetGeoTransform(transInfo)
CA = outDataset.GetRasterBand(1)
CA.WriteArray(pre_classified[:,:])
CA.FlushCache()
CA = None
outDataset = None
