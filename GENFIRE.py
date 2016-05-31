
from __future__ import division
import numpy as np
import matplotlib
matplotlib.use("Qt4Agg")

import matplotlib.pyplot as plt
import scipy.fftpack as sfft
import os
import scipy.io
import pyfftw
import time
import GENFIRE_from_GUI_Input
import misc
import itertools
import weightValues
from multiprocessing import Pool


PI = 3.14159265359


if __name__ != "__main__":
    def GENFIRE_iterate(numIterations,initialObject,support,measuredK,constraintIndicators,constraintEnforcementDelayIndicators,R_freeInd_complex,R_freeVals_complex,displayFigure):
        """
         * GENFIRE_iterate *

         Primary GENFIRE reconstruction function


         Author: Alan (AJ) Pryor, Jr.
         Jianwei (John) Miao Coherent Imaging Group
         University of California, Los Angeles
         Copyright 2015-2016. All rights reserved.


        :param numIterations: Integer number of iterations to run
        :param initialObject: Initial guess of 3D object
        :param support: Binary matrix representing where the object is allowed to exist
        :param measuredK: Assembled 3D Fourier grid
        :param constraintIndicators: Flag value for each datapoint used to control during which iterations a given Fourier component is enforced
        :param constraintEnforcementDelayIndicators: List of cutoff values that will be divided evenly among the iterations. All Fourier grid points with constraintIndicators greater than the current cutoff are enforced
        :param R_freeInd_complex: 3 x 1 x num_shells tuple of (x,y,z) coordinate lists for withheld values for Rfree calculation
        :param R_freeVals_complex: Complex valued component at the indices given by R_freeInd_complex
        :param displayFigure: Boolean flag to display figures during the reconstruction
        :return: outputs dictionary containing the reconstruction and error metrics
        """

        NUMTHREADS = 6 #number of threads to be used for the FFTW interface
        bestErr = 1e30 #initialize error

        #initialize arrays for error metrics
        Rfree_complex = np.ones(numIterations)*-1 #
        errK = np.zeros(numIterations)

        #prefetch indices for monitoring error
        errInd = measuredK != 0

        #get dimensions of object
        dims = np.shape(support)
        if R_freeInd_complex:
            Rfree_complex = np.zeros((np.shape(R_freeInd_complex)[2], numIterations))

        if displayFigure.DisplayFigureON: #setup some indices for plotting.
            n_half_x = int(dims[0]/2) #this assumes even-sized arrays
            n_half_y = int(dims[1]/2)
            n_half_z = int(dims[2]/2)

            half_window_x = displayFigure.reconstructionDisplayWindowSize[0]//2
            half_window_y = displayFigure.reconstructionDisplayWindowSize[1]//2
            half_window_z = displayFigure.reconstructionDisplayWindowSize[2]//2

        #setup output dict
        if R_freeInd_complex:
            outputs = {'reconstruction':initialObject,'errK':errK,'R_free':Rfree_complex}
        else:
            outputs = {'reconstruction':initialObject,'errK':errK}

        #determine how to divide up the constraint enforcement cutoffs among the iterations by determining
        #which iterations will require a recalculation of the indices to enforce
        iterationNumsToChangeCutoff = np.round(np.linspace(1, numIterations, num=np.size(constraintEnforcementDelayIndicators)))
        iterationNumsToChangeCutoff, uniqueIndices = np.unique(iterationNumsToChangeCutoff, return_index=True)
        iterationNumsToChangeCutoff = np.append(iterationNumsToChangeCutoff,1e30) #add an arbitrarily high number to the end that is an iteration number that won't be reached
        constraintEnforcementDelayIndicators = constraintEnforcementDelayIndicators[uniqueIndices]
        currentCutoffNum = 0
        for iterationNum in range(1, numIterations+1): #iterations are counted started from 1

            if iterationNum == iterationNumsToChangeCutoff[currentCutoffNum]: #update current Fourier constraint if appropriate
                relevantCutoff = constraintEnforcementDelayIndicators[currentCutoffNum]
                constraintInd_complex = (constraintIndicators > relevantCutoff) * measuredK != 0

                bestErr = 1e30 #reset error
                currentCutoffNum+=1#update constraint set number


            if iterationNum%25==0:
                print ("iteration number: ", iterationNum)
            initialObject[initialObject<0] = 0 #enforce positivity
            initialObject = initialObject * support #enforce support

            #take FFT of current reconstruction
            k = pyfftw.interfaces.numpy_fft.rfftn(initialObject,overwrite_input=True,threads=NUMTHREADS)

            #compute error
            errK[iterationNum-1] = np.sum(abs(k[errInd]-measuredK[errInd]))/np.sum(abs(measuredK[errInd]))#monitor error

            #update best object if a better one has been found
            if errK[iterationNum-1] < bestErr:
                bestErr = errK[iterationNum-1]
                outputs['reconstruction'] = initialObject

            #calculate Rfree for each spatial frequency shell if necessary
            if R_freeInd_complex:
                for shellNum in range(0, np.shape(R_freeInd_complex)[2]):

                    tmpIndX = R_freeInd_complex[0][0][shellNum]
                    tmpIndY = R_freeInd_complex[1][0][shellNum]
                    tmpIndZ = R_freeInd_complex[2][0][shellNum]

                    tmpVals = R_freeVals_complex[shellNum]
                    Rfree_complex[shellNum, iterationNum-1] = np.sum(abs(k[tmpIndX, tmpIndY, tmpIndZ] - tmpVals)) / np.sum(abs(tmpVals))

            #replace Fourier components with ones from measured data from the current set of constraints
            k[constraintInd_complex] = measuredK[constraintInd_complex]
            initialObject = pyfftw.interfaces.numpy_fft.irfftn(k,overwrite_input=True,threads=NUMTHREADS)

            #update display
            if displayFigure.DisplayFigureON:
                if iterationNum % displayFigure.displayFrequency == 0:

                    plt.figure(1)
                    plt.subplot(233)
                    plt.imshow(np.squeeze(np.fft.ifftshift(initialObject)[n_half_x, n_half_y-half_window_y:n_half_y+half_window_y, n_half_z-half_window_z:n_half_z+half_window_z]))
                    plt.title("central YZ slice")

                    plt.subplot(232)
                    plt.imshow(np.squeeze(np.fft.ifftshift(initialObject)[n_half_x-half_window_x:n_half_x+half_window_x, n_half_y, n_half_z-half_window_z:n_half_z+half_window_z]))
                    plt.title("central XZ slice")

                    plt.subplot(231)
                    plt.title("central XY slice")
                    plt.imshow(np.squeeze(np.fft.ifftshift(initialObject)[n_half_x-half_window_x:n_half_x+half_window_x, n_half_y-half_window_y:n_half_y+half_window_y, n_half_z]))

                    plt.subplot(236)
                    plt.title("YZ projection")
                    plt.imshow(np.squeeze(np.sum(np.fft.ifftshift(initialObject)[n_half_x-half_window_x:n_half_x+half_window_x, n_half_y-half_window_y:n_half_y+half_window_y, n_half_z-half_window_z:n_half_z+half_window_z], axis=0)))

                    plt.subplot(235)
                    plt.title("XZ projection")
                    plt.imshow(np.squeeze(np.sum(np.fft.ifftshift(initialObject)[n_half_x-half_window_x:n_half_x+half_window_x, n_half_y-half_window_y:n_half_y+half_window_y, n_half_z-half_window_z:n_half_z+half_window_z], axis=1)))

                    plt.subplot(234)
                    plt.title("XY projection")
                    plt.imshow(np.squeeze(np.sum(np.fft.ifftshift(initialObject)[n_half_x-half_window_x:n_half_x+half_window_x, n_half_y-half_window_y:n_half_y+half_window_y, n_half_z-half_window_z:n_half_z+half_window_z], axis=2)))
                    plt.get_current_fig_manager().window.setGeometry(25,25,400, 400)
                    plt.draw()

                    plt.figure(2)
                    plt.get_current_fig_manager().window.setGeometry(25,450,400, 400)
                    plt.hold(False)
                    plt.plot(range(0,numIterations),errK)
                    plt.title("K-space Error vs Iteration Number")
                    plt.xlabel("Spatial Frequency (% of Nyquist)")
                    plt.ylabel('Reciprocal Space Error')
                    plt.draw()

                    if R_freeInd_complex:
                        plt.figure(3)
                        mngr = plt.get_current_fig_manager()
                        mngr.window.setGeometry(450,25,400, 400)
                        plt.plot(range(0,numIterations),np.mean(Rfree_complex,axis=0))
                        plt.title("Mean R-free Value vs Iteration Number")
                        plt.xlabel("Iteration Num")
                        plt.ylabel('Mean R-free')
                        plt.draw()

                        plt.figure(4)
                        mngr = plt.get_current_fig_manager()
                        mngr.window.setGeometry(450,450,400, 400)
                        plt.hold(False)
                        X = np.linspace(0,1,np.shape(Rfree_complex)[0])
                        plt.plot(X, Rfree_complex[:,iterationNum-1])
                        plt.hold(False)
                        plt.title("Current Rfree Value vs Spatial Frequency")
                        plt.xlabel("Spatial Frequency (% of Nyquist)")
                        plt.ylabel('Rfree')
                        plt.draw()


                    plt.pause(1e-30) #forces display to update

        outputs['errK'] = errK
        if R_freeInd_complex:
            outputs['R_free'] = Rfree_complex
        outputs['reconstruction'] = np.fft.fftshift(outputs['reconstruction'])
        return outputs

    def generateKspaceIndices(obj):
        """
        * generateKspaceIndices *

        Maps the radial coordinate indices in the matrix obj

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.


        :param obj: Matrix of size to be mapped
        :return: 3D indices for each voxel in the volume
        """

        dims = np.shape(obj)
        if len(dims) < 3:
            dims = dims + (0,)

        if dims[0] % 2 == 0:
            ncK0 = dims[0]/2
            vec0 = np.arange(-ncK0, ncK0, 1)/ncK0
        elif dims[0] == 1:
            vec0 = 0
            ncK0 = 1

        else:
            ncK0 = ((dims[0]+1)/2)-1
            vec0 = np.arange(-ncK0, ncK0+1)/ncK0


        if dims[1] % 2 == 0:
            ncK1 = dims[1]/2
            vec1 = np.arange(-ncK1, ncK1, 1)/ncK1
        elif dims[1] == 1:
            vec1 = 0
            ncK1 = 1

        else:
            ncK1 = ((dims[1]+1)/2)-1
            vec1 = np.arange(-ncK1, ncK1+1)/ncK1


        if dims[2] % 2 == 0:
            ncK2 = dims[2]/2
            vec2 = np.arange(-ncK2, ncK2, 1)/ncK2
        elif dims[2] == 1:
            vec2 = 0
            ncK2 = 1

        else:
            ncK2 = ((dims[2]+1)/2)-1
            vec2 = np.arange(-ncK2, ncK2+1)/ncK2

        kx, ky, kz = np.meshgrid(vec1,vec0,vec2)
        Kindices = np.sqrt(kx**2 + ky**2 + kz**2)
        return Kindices






    def fillInFourierGrid(projections,angles,interpolationCutoffDistance):
        """
        * fillInFourierGrid *

        Primary function for converting a set of 2D projection images into a 3D Fourier grid

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.

        :param projections: N x N x num_projections NumPy array containing the projections
        :param angles: 3 x num_projections NumPy array of Euler angles phi,theta, psi
        :param interpolationCutoffDistance: Radius of interpolation kernel. Only values within this radius of a grid point are considered
        :return: the assembled Fourier grid

        """
        tic = time.time()
        dim1 = np.shape(projections)[0]
        dim2 = np.shape(projections)[1]
        if len(np.shape(projections))>2:
            numProjections = np.shape(projections)[2]
        else:
            numProjections = 1
        nc = np.round(dim1/2)
        n2 = nc
        measuredX = np.zeros([dim1*dim2,numProjections])
        measuredY = np.zeros([dim1*dim2,numProjections])
        measuredZ = np.zeros([dim1*dim2,numProjections])
        kMeasured = np.zeros([dim1,dim1,numProjections], dtype=complex)
        confidenceWeights = np.zeros([dim1,dim1,numProjections]) #do I need this??
        ky,kx = np.meshgrid(np.arange(-n2,n2,1),np.arange(-n2,n2,1))
        Q = np.sqrt(ky**2+kx**2)/n2
        kx = np.reshape(kx, [1, dim1*dim2], 'F')
        ky = np.reshape(ky, [1, dim1*dim2], 'F')
        kz = np.zeros([1, dim1*dim1])
        for projNum in range(0, numProjections):
            phi = angles[0, projNum] * PI/180
            theta = angles[1, projNum] * PI/180
            psi = angles[2, projNum] * PI/180
            R = np.array([[np.cos(psi)*np.cos(theta)*np.cos(phi)-np.sin(psi)*np.sin(phi) ,np.cos(psi)*np.cos(theta)*np.sin(phi)+np.sin(psi)*np.cos(phi)   ,    -np.cos(psi)*np.sin(theta)],
            [-np.sin(psi)*np.cos(theta)*np.cos(phi)-np.cos(psi)*np.sin(phi), -np.sin(psi)*np.cos(theta)*np.sin(phi)+np.cos(psi)*np.cos(phi) ,   np.sin(psi)*np.sin(theta) ],
            [np.sin(theta)*np.cos(phi)                               , np.sin(theta)*np.sin(phi)                                ,              np.cos(theta)]])
            R = R.T

            Kcoordinates = np.zeros([3, dim1*dim2])
            Kcoordinates[0, :] = kx
            Kcoordinates[1, :] = ky
            Kcoordinates[2, :] = kz


            rotkCoords = np.dot(R, Kcoordinates)
            confidenceWeights[:, :, projNum] = np.ones_like(Q) #this implementation does not support individual projection weighting, so just set all weights to 1
            measuredX[:, projNum] = rotkCoords[0, :]
            measuredY[:, projNum] = rotkCoords[1, :]
            measuredZ[:, projNum] = rotkCoords[2, :]
            kMeasured[:, :, projNum] = np.fft.fftshift(np.fft.fftn(np.fft.ifftshift(projections[:, :, projNum])))

        measuredX = np.reshape(measuredX,[1, np.size(kMeasured)], 'F')
        measuredY = np.reshape(measuredY,[1, np.size(kMeasured)], 'F')
        measuredZ = np.reshape(measuredZ,[1, np.size(kMeasured)], 'F')
        kMeasured = np.reshape(kMeasured,[1, np.size(kMeasured)], 'F')
        confidenceWeights = np.reshape(confidenceWeights,[1, np.size(kMeasured)], 'F')
        notFlaggedIndices = kMeasured != -999
        measuredX = measuredX[notFlaggedIndices]
        measuredY = measuredY[notFlaggedIndices]
        measuredZ = measuredZ[notFlaggedIndices]
        kMeasured = kMeasured[notFlaggedIndices]
        confidenceWeights = confidenceWeights[notFlaggedIndices]

        masterInd = []
        masterVals = []
        masterDistances = []
        masterConfidenceWeights = []
        shiftMax = 0

        for Yshift in range(-shiftMax, shiftMax+1):
            for Xshift in range(-shiftMax, shiftMax+1):
                for Zshift in range(-shiftMax, shiftMax+1):

                    tmpX = np.round(measuredX) + Xshift
                    tmpY = np.round(measuredY) + Yshift
                    tmpZ = np.round(measuredZ) + Zshift


                    tmpVals = kMeasured
                    tmpConfidenceWeights = confidenceWeights
                    distances = np.sqrt(abs(measuredX-tmpX)**2 + abs(measuredY-tmpY)**2 + abs(measuredZ-tmpZ)**2)
                    tmpX+=nc
                    tmpY+=nc
                    tmpZ+=nc

                    goodInd = (np.logical_not((tmpX > (dim1-1)) | (tmpX < 0) | (tmpY > (dim1-1)) | (tmpY < 0) | (tmpZ > (dim1-1)) | (tmpZ < 0))) & (distances <= interpolationCutoffDistance)

                    masterInd=np.append(masterInd, np.ravel_multi_index((tmpX[goodInd].astype(np.int64), tmpY[goodInd].astype(np.int64), tmpZ[goodInd].astype(np.int64)),[dim1, dim1, dim1], order='F'))
                    masterVals=np.append(masterVals, tmpVals[goodInd])
                    masterDistances=np.append(masterDistances, distances[goodInd])
                    masterConfidenceWeights=np.append(masterConfidenceWeights, tmpConfidenceWeights[goodInd])


                    t = 0;

        masterInd = np.array(masterInd).astype(np.int64)
        masterVals = np.array(masterVals)
        masterDistances = np.array(masterDistances)
        masterConfidenceWeights = np.array(masterConfidenceWeights)



        sortIndices = np.argsort(masterInd)
        masterInd = masterInd[sortIndices]
        masterVals = masterVals[sortIndices]
        masterDistances = masterDistances[sortIndices]
        masterConfidenceWeights = masterConfidenceWeights[sortIndices]


        halfwayCutoff = ((dim1+1)**3)//2+1


        masterVals = masterVals[masterInd <= halfwayCutoff]
        masterDistances = masterDistances[masterInd <= halfwayCutoff]
        masterConfidenceWeights = masterConfidenceWeights[masterInd <= halfwayCutoff]
        masterInd = masterInd[masterInd <= halfwayCutoff]


        uniqueVals, uniqueInd = np.unique(masterInd, return_index=True)

        uniqueInd = np.append(uniqueInd, 0)

        diffVec = np.diff(uniqueInd)
        singleInd = diffVec == 1
        multiInd = np.where(diffVec != 1)
        measuredK = np.zeros([dim1**3], dtype=complex)

        measuredK[uniqueVals[singleInd]] = masterVals[uniqueInd[0:-1][singleInd]]

        vals = weightValues.weightValue(np.array(multiInd[0][:],dtype=int), uniqueInd, masterDistances, masterVals)

        measuredK[uniqueVals[multiInd[0][:]]] = vals
        measuredK = np.reshape(measuredK,[dim1,dim1,dim1],order='F')

        # print ("time3 " , time.time()-tic3)
        measuredK[np.isnan(measuredK)] = 0
        measuredK = misc.hermitianSymmetrize(measuredK)

        print ("GENFIRE: Fourier grid assembled in %d seconds" % (time.time()-tic))
        return measuredK




    def loadProjections(filename):
        """
        * loadProjections *

        Wrapper function for loading in projections of arbitrary (supported) extension

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.

        :param filename: Filename of project images to load
        :return: NumPy array containing projections
        """

        filename, file_extension = os.path.splitext(filename)
        if file_extension == ".mat":
            print ("GENFIRE: reading projections from MATLAB file.\n")
            return readMAT(filename + file_extension)
        elif file_extension == ".tif":
            print ("GENFIRE: reading projections from .tif file.\n")
            return readTIFF(filename + file_extension)
        elif file_extension == ".mrc":
            print ("GENFIRE: reading projections from .mrc file.\n")
            return readMRC(filename + file_extension)
        else:
            raise Exception('GENFIRE: File format %s not supported.', file_extension)

    def readMAT(filename):
        """
        * readMAT *

        Read projections from a .mat file

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.

        :param filename: MATLAB file (.mat) containing projections
        :return: NumPy array containing projections
        """

        try: #try to open the projections as a stack
            projections = scipy.io.loadmat(filename)
            projections = np.array(projections[projections.keys()[0]])
        except: ## -- figure out where error is thrown
             #check if the projections are in individual files
            flag = True
            filename_base, file_extension = os.path.splitext(filename)
            projectionCount = 1
            while flag: #first count the number of projections so the array can be initialized
                projectionCount = projectionCount
                nextFile = filename_base + str(projectionCount) + file_extension
                if os.path.isfile(nextFile):
                    projectionCount += 1
                else:
                    flag = False


            ## open first projection to get dimensions
            pj = scipy.io.loadmat(filename_base + str(1) + file_extension)
            pj = pj[projections.keys()[0]]
            dims = np.shape(pj)
            #initialize projection array
            projections = np.zeros((dims[0], dims[1], projectionCount),dtype=int)

            #now actually load in the tiff images
            for projNum in range(projectionCount):
                nextFile = filename_base + str(projNum) + file_extension
                pj = scipy.io.loadmat(filename_base + str(projNum) + file_extension)
                pj = pj[pj.keys()[0]]
                projections[:, :, projNum] = np.array(pj)

        return projections


    def readTIFF(filename):
        """
        * readTIFF *

        Read (possibly multiple) TIFF images into a NumPy array

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.

        :param filename: Name of TIFF file or TIFF file basename to read. If the filename is a base then
        #       the images must begin with the string contained in filename followed by consecutive integers with
        #       no zero padding, i.e. foo1.tiff, foo2.tiff,..., foo275.tiff
        :return: NumPy array containing projections
        """
        import functools
        from PIL import Image
        import os
        try:
            projections = np.array(Image.open(filename))
        except:
            flag = True
            filename_base, file_extension = os.path.splitext(filename)
            projectionCount = 1
            while flag: #first count the number of projections so the array can be initialized
                projectionCount = projectionCount
                nextFile = filename_base + str(projectionCount) + file_extension
                if os.path.isfile(nextFile):
                    projectionCount += 1
                else:
                    flag = False

            ## open first projection to get dimensions
            dims = np.shape(Image.open(filename_base + str(1) + file_extension))

            #initialize projection array
            projections = np.zeros((dims[0], dims[1], projectionCount),dtype=int)

            pool = Pool(4)
            func = functools.partial(readInTiffProjection, filename_base)
            pj = pool.map(func, range(projectionCount))
            for j  in range(projectionCount):
                projections[:, :, j] = pj[j]
            return projections

    def readInTiffProjection(filename_base, fileNumber):
        """
        * readInTiffProjection *

        Reads and returns a single TIFF image as a NumPy array

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.

        :param filename_base: Base filename of TIFF
        :param fileNumber: Image number
        :return: Image in a 2D NumPy array
        """
        from PIL import Image
        nextFile = filename_base + str(fileNumber) + '.tif'
        return np.array(Image.open(nextFile))

    def readMRC(filename, dtype=float,order="C"):
        """
        * readMRC *

        Read in a volume in .mrc file format. See http://bio3d.colorado.edu/imod/doc/mrc_format.txt

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.

        :param filename: Filename of .mrc
        :return: NumPy array containing the .mrc data
        """
        import struct
        headerIntNumber = 56
        sizeof_int = 4
        headerCharNumber = 800
        sizeof_char = 1
        with open(filename,'rb') as fid:
            int_header = struct.unpack('=' + 'i'*headerIntNumber, fid.read(headerIntNumber * sizeof_int))
            char_header = struct.unpack('=' + 'c'*headerCharNumber, fid.read(headerCharNumber * sizeof_char))
            dimx, dimy, dimz, data_flag= int_header[:4]
            print "reading, ", dimx,dimy,dimz
            if (data_flag == 0):
                datatype='u1'
            elif (data_flag ==1):
                datatype='i1'
            elif (data_flag ==2):
                datatype='f4'
            elif (data_flag ==3):
                datatype='c'
            elif (data_flag ==4):
                datatype='f4'
            elif (data_flag ==6):
                datatype='u2'
            else:
                raise ValueError("No supported datatype found!\n")
            print dimx,dimy,dimz
            print datatype
            return np.fromfile(file=fid, dtype=datatype,count=dimx*dimy*dimz).reshape((dimx,dimy,dimz),order=order).astype(dtype)

    def writeMRC(filename, arr, datatype='f4'):
        """
        * writeMRC *

        Write a volume to .mrc file format. See http://bio3d.colorado.edu/imod/doc/mrc_format.txt

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved

        :param filename: Filename of .mrc file to write
        :param arr: NumPy volume of data to write
        :param dtype: Type of data to write
        """
        dimx, dimy, dimz = np.shape(arr)
        if datatype != arr.dtype:
            arr = arr.astype(datatype)
        int_header = np.zeros(56,dtype='int32')

        if (datatype == 'u1'):
            data_flag = 0
        elif (datatype =='i1'):
            data_flag = 1
        elif (datatype =='f4'):
            data_flag = 2
        elif (datatype =='c'):
            data_flag = 3
        elif (datatype =='f4'):
            data_flag = 4
        elif (datatype =='u2'):
            data_flag = 6
        else:
            raise ValueError("No supported datatype found!\n")

        int_header[:4] = (dimx,dimy,dimz,data_flag)
        char_header = str(' '*800)
        with open(filename,'wb') as fid:
            fid.write(int_header.tobytes())
            fid.write(char_header)
            fid.write(arr.tobytes())

    def saveResults(reconstruction_outputs, filename):
        """
        * saveResults *

        Helper function to save results of GENFIRE reconstruction

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved

        :param reconstruction_outputs: dictionary containing reconstruction, reciprocal error (errK), and possible R_free
        :param filename: Output filename
        """
        import os
        fn, ext = os.path.splitext(filename)
        writeMRC(filename, reconstruction_outputs['reconstruction'])
        np.savetxt(fn+'_errK.txt',reconstruction_outputs['errK'])
        if 'R_free' in reconstruction_outputs.keys():
            np.savetxt(fn+'_Rfree.txt',reconstruction_outputs['R_free'])


    class DisplayFigure:
        """
        * DisplayFigure *

        Helper class for displaying figures during reconstruction process

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.
        """
        def __init__(self):
            self.DisplayFigureON = False
            self.DisplayErrorFigureON = False
            self.displayFrequency = 5
            self.reconstructionDisplayWindowSize = 0

    def loadAngles(filename):
        """
        * loadAngles *

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.

        :param filename:
        :return:
        """
        import os
        base,ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext == ".txt":
            return np.loadtxt(filename,dtype=float)
        elif ext== ".npy":
            return np.load(filename)
        elif ext==".mat":
            import scipy.io as io
            data = io.loadmat(filename)
            if "angles" not in data.keys():
                raise LookupError("No variable called 'angles' found in \"{}\"!".format(filename))
            return np.array(data['angles'],dtype=float)
        else:
            raise IOError("Unsupported file extension \"{}\" for Euler angles".format(ext))

    def loadInitialObject(filename):
        """
        * loadInitialObject *

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.

        :param filename:
        :return:
        """
        import os
        base,ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext == ".npy":
            return np.load(filename)
        elif ext==".mat":
            import scipy.io as io
            data = io.loadmat(filename)
            if "initial_object" not in data.keys():
                raise LookupError("No variable called 'initial_object' found in \"{}\"!".format(filename))
            return np.array(data['initial_object'],dtype=float)
        elif ext==".mrc":
            raise NotImplementedError("mrc file format not yet supported")
        else:
            raise IOError("Unsupported file extension \"{}\" for initial object".format(ext))

