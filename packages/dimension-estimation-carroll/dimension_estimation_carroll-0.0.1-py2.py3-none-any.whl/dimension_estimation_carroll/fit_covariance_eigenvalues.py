#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:19:41 2024

@author: carroll
"""
#! /usr/local/bin/python3
""" draw samples from a Wishart distribution for different numbers of 
dimensions and points. Use these matrices to find eigenvalues for the
covariance matrices of random processes in D dimensions with N points.
Do multiple draws for each N and D to estimate the maximum and minimum
values of the eigenvalue distribution. For each D fit the max and min curves
'max_iterationss a function of N using a polynomial model and save the fit coefficients """


import scipy.stats as stats
import numpy as np
from scipy.linalg import lstsq
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import tkinter as tk
root = tk.Tk()
# root window title and dimension
root.title("Estimate limiting eigenvalues for random process")
# Set geometry (widthxheight)
root.geometry('700x400')


class EigenvalueFit:

    def __init__(self, exponent_vec, max_iterations, min_dim, max_dim, max_points):
        self.exponent_vec = exponent_vec
        self.max_iterations = max_iterations
        self.min_dim = min_dim
        self.max_dim = max_dim
        self.max_points = max_points

# define fit matrix for least squares fit
    def poly_mat(self, x_in):
        n_pts = len(x_in)
        n_ord = len(self.exponent_vec)
        y_out = np.zeros((n_pts, n_ord))

        for ipow in range(n_ord):
            y_out[:, ipow] = x_in**self.exponent_vec[ipow]

        return y_out

# apply fit coefficients to produce fitted curve
    def poly_fit(self, x_in, coeff_vec):
        # y_out is a vector created by multiplying x_in by the fit coefficients
        n_ord = len(coeff_vec)
        npt = len(x_in)
        y_fit = np.zeros(npt)

        for ipow in range(n_ord):
            y_fit += np.multiply(coeff_vec[ipow],
                                 x_in**self.exponent_vec[ipow])
        return y_fit
# -----------------------------
    # for each dimension

    def dimension_fit(self, i_dim):
        num_dimension = i_dim+self.min_dim
        ev_max = np.zeros((self.max_points))
        ev_min = np.zeros((self.max_points))
    # create an identity matrix with num_dimensions
        i_matrix = np.identity(num_dimension)
        # generate a random matrix drawn from a Wishart distribution with a covariance
        # consisting of an identity matrix
        for num_points in range(num_dimension+1, self.max_points):
            ev_upper_vec = np.zeros(self.max_iterations)
            ev_lower_vec = np.zeros(self.max_iterations)
            for i_num in range(self.max_iterations):
                # multiple random trials
                # normalize by the number of points
                ws_matrix = stats.wishart.rvs(num_points, i_matrix)/num_points
                # covariance matrix
                cmat = ws_matrix*np.transpose(ws_matrix)
                # eigenvalues are the singular values
                sing_vec = np.linalg.svd(cmat, compute_uv=False)
              # upper and lower bounds on the eigenvalues for a random (isotropic) matrix
                ev_upper_vec[i_num] = max(sing_vec)
                ev_lower_vec[i_num] = min(sing_vec)
            # max and min for all max_iterations trials
            ev_max[num_points] = max(ev_upper_vec)
            ev_min[num_points] = min(ev_lower_vec)
        # least squares fits to eigenvalue vs num_points curves
        x_vec = np.arange(num_dimension+1, self.max_points)

        y_mat = EigenvalueFit.poly_mat(self, x_vec)
        # y_mat is a matrix of basis functions
        # least squares solution to y_mat*coeff_vec_max=ev_max
        coeff_vec_max, rres, r_rank, ss_val = lstsq(
            y_mat, ev_max[num_dimension+1:self.max_points])
        # least squares solution to y_mat*coeff_vec_max=ev_max
        coeff_vec_min, rres, r_rank, ss_val = lstsq(
            y_mat, ev_min[num_dimension+1:self.max_points])
     # store in matrix

        return coeff_vec_min, coeff_vec_max

    def run_estimate(self):
        # matrix to store coefficients
        n_order=len(self.exponent_vec)
        coefficient_matrix = np.zeros([self.max_dim-self.min_dim+1, 2, n_order])
        dimension_vector = np.arange(self.min_dim, self.max_dim+1)
        mb.showinfo(message='choose output file in next window')
        file_out = fd.asksaveasfile(mode='w')
        
        for i_dim in range(self.max_dim-self.min_dim+1):
            print(i_dim+self.min_dim)
            coeff_vec_min, coeff_vec_max = EigenvalueFit.dimension_fit(self,i_dim)
            coefficient_matrix[i_dim, 0, :] = coeff_vec_min
            coefficient_matrix[i_dim, 1, :] = coeff_vec_max
  
# save fit coefficients
        np.savez(file_out.name, dim_vec=dimension_vector,
                 coeff_mat=coefficient_matrix)
        root.destroy()
 # button is clicked
def clicked_run():
    lbl_run.configure(fg='red', text="running")
   
    min_dim = min_entry.get()
    max_dim = max_entry.get()
    max_points = points_entry.get()
    max_iterations = iter_entry.get()
    if len(min_dim) == 0:
        min_dim = 2
    else:
        min_dim=int(min_dim)        
    if len(max_dim) == 0:
        max_dim = 10
    else:
        max_dim=int(max_dim) 
    if len(max_points)==0:
        max_points=200
    else:
        max_points=int(max_points)
    if len(max_iterations) == 0:
        max_iterations = 300
    else:
        max_iterations=int(max_iterations)

    exponent_vec = [-2., -1., -0.5, 0, 0.5, 1., 2.]  # polynomial order
    ee_fit = EigenvalueFit(exponent_vec, max_iterations,
                           min_dim, max_dim, max_points)

    ee_fit.run_estimate()

    lbl_run.configure(fg='blue', text="finished")


    # ----------------------------------
# minimum and maximum dimensions
lbl_dim1 = tk.Label(root, text="minimum dimension? (default=2)")
lbl_dim1.pack(side=tk.TOP)
# adding Entry Field
min_entry = tk.Entry(root, width=6)
min_entry.pack(side=tk.TOP)

lbl_dim2 = tk.Label(root, text="maximum dimension? (default=10)" )
lbl_dim2.pack(side=tk.TOP)
# adding Entry Field
max_entry = tk.Entry(root, width=6)
max_entry.pack(side=tk.TOP)
# max number of points
lbl_dim2 = tk.Label(root, text="maximum number of points? (default=200)")
lbl_dim2.pack(side=tk.TOP)
# adding Entry Field
points_entry = tk.Entry(root, width=6)
points_entry.pack(side=tk.TOP)
# number of iterations
label_iter = tk.Label(root, text='number of iterations (default=300)')
label_iter.pack(side=tk.TOP)
iter_entry = tk.Entry(root, width=8)
iter_entry.pack(side=tk.TOP)

lbl_run = tk.Label(root,fg='blue',text='click button to run')
lbl_run.pack(side=tk.TOP)
    
# button widget
run_btn=tk.Button(root, text = 'Start',
                 fg="blue", command=clicked_run)

run_btn.pack(side=tk.TOP)

# Execute Tkinter
root.mainloop()
