#!/usr/bin/env python3
import numpy as np
import numpy.linalg
import scipy
import scipy.special
import math
import cmath
import random

# apply fit coefficients to produce fitted curve
def poly_fit( x_in, coeff_vec):
    # y_out is a point created by multiplying x_in by the fit coefficients
    exponent_vec = [-2., -1., -0.5, 0, 0.5, 1., 2.]  # polynomial order
    n_ord = len(coeff_vec)
    y_fit = 0

    for ipow in range(n_ord):
        y_fit += np.multiply(coeff_vec[ipow],
                             x_in**exponent_vec[ipow])
    return y_fit
# --------------------------------------------
def embedding_prob_func(data_vector, delay_vector, dimension_vector,dim_index,
                        coefficient_matrix, suRRogate):   
    """ finds probability that data_vector can be embedded in a space with delays given by delay_vector and
    dimensions given by dimension_vector. eigenvalue_table contains precomputed limiting
    eigenvalues as a function of dimension and number of points. suRRogate==1 compares to phase
    randomized surrogate to help distinguish signal from random noise """
    info_thresh=1

    ndel=len(delay_vector)
    ndim=len(dimension_vector)
    probability_matrix=np.zeros([ndim,ndel])
    
    probability_matrix=dim_prob_func(data_vector, delay_vector, dimension_vector,dim_index,
                                     coefficient_matrix, info_thresh)

    if suRRogate==True:
        sigFFT=np.fft.rfft(data_vector)
        lFF=len(sigFFT)
        phaseVec=np.zeros(lFF,dtype='complex')
        for k in range(lFF):
            phRand=random.random()+random.random()*1.j
            phAbs=abs(phRand)
            phaseVec[k]=phRand/phAbs
 
        expV=np.vectorize(cmath.exp)
        sigFrand=expV(-1.j*phaseVec)
    
        surrogate_vector=np.fft.irfft(sigFrand)
        prob_surrogate=dim_prob_func(surrogate_vector, delay_vector, dimension_vector,coefficient_matrix, info_thresh)
        probability_matrix -= prob_surrogate
        
    return probability_matrix
#####################
def dim_prob_func(data_vector, delay_vector, dimension_vector,dim_index,
                  coefficient_matrix, info_thresh):

    import sklearn.neighbors as neighbors
    
    ndel=len(delay_vector)
    ndim=len(dim_index)
    npt=len(data_vector)
    probOut=np.zeros([ndim,ndel])
    
    
    for jd in range(ndim): # loop for embedding dimensions
        print('jd', jd)
        embDim=dimension_vector[dim_index[jd]]
        print('embDim',embDim)
        n_partition=2**embDim

        for itau in range(ndel): # loop for embedding delays
            tau=delay_vector[itau]
            print('embDim delay',embDim,tau)
            nLen=npt-(embDim-1)*tau
            embed_signal=np.zeros([nLen,embDim]) # embedded signal
            for j in range(embDim):
                embed_signal[:,j]=data_vector[j*tau:nLen+j*tau]
                
            embTree = neighbors.KDTree(embed_signal, leaf_size=40)
            total_out=0 # number of clusters for which eigenvalues are outside limits for random
            nClust=0 # total number of clusters
            used_list=np.zeros(nLen) # 0 if point not yet used in a cluster, 1 if used
            used_number=0 # total number of points used in a cluster so far
           
            while used_number < 0.8*nLen: # 95% of points should be used
        
                k=embDim+1 # min points
              # next 4 lines: pick new center from unused points  
                uList=np.where(used_list == 0)
                icp_u=random.randint(0,len(uList[0])-1)
                icpX=uList[0]
                icp=icpX[icp_u]
            
     # cluster embedded signal                
                dkfunc=0 # partition cost
                while (dkfunc < info_thresh) and (k < nLen): # increase cluster size until info_threshold exceeded
                    k+=embDim
                # find distance to k nearest points
                    dist_list=embTree.query(embed_signal[icp:icp+1][:],k,return_distance=False,sort_results='True')
                    dist_list=dist_list[0]   
        # Theiler exclusion: exclude points that are consecutive in time
                    list_diff=np.diff(dist_list,n=1)
                    zList=tuple(np.where(list_diff!=1))
                    dist_list=dist_list[zList]
                    nNear=len(dist_list)
                    
                    xMax=np.zeros([embDim])
                    xMin=np.zeros([embDim])
                    iMaxMin=1 # used in case max==min for some dimension
                    if nNear==0:
                        iMaxMin=0
                    if iMaxMin:
                        for jm in range(embDim):
                            lX1=embed_signal[:,jm]
                            lX2=lX1[dist_list]
                            xMax[jm]=max(lX2)
                            xMin[jm]=min(lX2)
                            if xMax[jm]==xMin[jm]:
                                iMaxMin=0
                   
     # proceed if max != min
                    if iMaxMin:
                     # turn point locations into box numbers
                         nBox=np.zeros([nNear])
       # points are located on a grid where point location for each dimension runs fro 0 to 1
       # nBox is embDim-dimensional grid location converted to a 1-dimensional integer
                     #    print('dist_list',dist_list)
                         for jm in range(embDim):                        
                             lDlist=dist_list[0:k]                         
                             lX1=embed_signal[:,jm]
                             lX2=embed_signal[lDlist,jm]                                                  
                             nPvec=(lX2-xMin[jm])/(xMax[jm]-xMin[jm])
                             nBox+=np.floor(nPvec)*(2**jm)

                         probVec=np.zeros([n_partition]) # will contain number of points in each partition
                         for kp in range(n_partition):
                            pList=list(np.where(nBox==kp))
                            probVec[kp]=len(pList[0])
                     
                         rho0=nNear/n_partition
                        
                         dKLff=0;
                   # compute Kullback Leibler divergence      
                         for kp in range(n_partition):
                            dKLff+=(probVec[kp]-rho0)*scipy.special.psi(probVec[kp]+0.5)- \
                            scipy.special.gammaln(probVec[kp]+0.5)+scipy.special.gammaln(rho0+0.5)
                      
                         dKLff/= math.sqrt(2) # scale to log2 units
                         lfunc=n_partition*math.log2(n_partition) # partitioning penalty function
                         dkfunc=dKLff-lfunc
                           
                         a0=1;
                    # end if iMaxMin
                   
                #  end while dkfunc < lthresh
               
                a0=1;
               # find covariance matrix        
                xMat=embed_signal[dist_list[0:k]][:]
          #      print('xMat unnorm',xMat)
                for jx in range(embDim):
                    xMean=sum(xMat[:,jx])/nNear
                    xMat[:,jx]-=xMean
                for jx in range(embDim):
                    xStd=math.sqrt((sum(xMat[:,jx]**2))/(nNear-1))
                    xMat[:,jx] /=xStd
                
                cMat=np.transpose(xMat)@xMat/nNear
            #    print('xMat',xMat)
             #   print('cMat',cMat)
                cEig=numpy.linalg.eigvals(cMat) # covariance matrix eigenvalues
         
          # precomputed eigenvalues for random processes
                eLow=poly_fit( nNear, coefficient_matrix[embDim][0][:])
                eHigh=poly_fit(nNear, coefficient_matrix[embDim][1][:])
                
                iOut=0 # 1 if at least 1 eigenvalue outside limits
                for j in range(embDim): # check to see if eigenvalues within limits for random process
                    if cEig[j] > eHigh:
                        iOut=1
                    if cEig[j] < eLow:
                        iOut=1
         
                total_out+=iOut
                nClust+=1
                used_list[dist_list[1:k]]=1 # add to list of used points
                usedNm=np.where(used_list == 1)
                used_number=len(usedNm[0])
            #    strOut=str(icp)+' '+str(nNear)+' '+str(cEig[0])+' '+str(cEig[1])+' '+str(eLow)+' '+str(eHigh)+'\n'
            #    file_out.write(strOut)
                a0=1
            # end if used_number < 0.95*nLen    
            probOut[jd,itau]=total_out/nClust # probability as a function of delay and dimension
            print('nClust',nClust)
        # end of itau loop
       
        a0=1
        # end of jd loop
     
    return probOut  
#######

    

    

     
    
    

