#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:23:33 2024

@author: carroll
Estimate the probability that a time series signal can be embedded in D
dimensions with an embedding delay of Tau. The probability is calculated by
the number of local regions on the embedded signal whose covariance eigenvalues
lie outside the limits for a random process. The limits for a random process
are computed from the coefficients for a polynomial fit to a plot of the
largest and smallest possible eigenvalues as a function of number of points N
for each embedding dimension D. The coefficients may be read in from a file or
the default coefficients may be used.
"""

import numpy as np
import array as arr
# import embedding_prob_func as epp
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import default_coeff
from embedding_prob_func_coeff import embedding_prob_func
import matplotlib.pyplot as plt
import csv

root = tk.Tk()
# root window title and dimension
root.title("Estimate probability signal can be embedded")
# Set geometry (widthxheight)
root.geometry('700x400')

# load coefficients from file
def load_coeff():
    mb.showinfo(root, 'Next window opens coefficient file')
    fil_in = fd.askopenfile(mode='r', title='coefficient_file', parent=root)
    eval_dat = np.load(fil_in.name)

    dimension_vector = eval_dat['dim_vec']
    coefficient_matrix = eval_dat['coeff_mat']
    return dimension_vector, coefficient_matrix
    # ----------------------------------


def load_signal():
    mb.showinfo(root, 'Choose time series in next window')
    fil_in = fd.askopenfile(mode='r', title='Time series file', parent=root)
    time_series = np.loadtxt(fil_in.name, dtype=float)
    return time_series
# ---------------------------------------------
 # button is clicked


def clicked_run():
    global prob_out
    use_coeff = choose_coeff.get()
    if use_coeff == 'n':
        dim_vec, coeff_mat = load_coeff()
    else:
        dim_vec, coeff_mat = default_coeff.use_default_coeff()
    coeff_mat = np.array(coeff_mat)
# use surrogate?
    use_surr=choose_surr.get()
        
    lbl_run = tk.Label(text='Running', fg='red')
    lbl_run.pack()

    min_dim = min_entry.get()
    max_dim = max_entry.get()
    if (min_dim == ''):
        min_dim = 1
    min_dim = int(min_dim)
    if max_dim == '':
        max_dim = 1
    max_dim = int(max_dim)
    dv_max = max(dim_vec)
    if (max_dim > dv_max):
        max_dim = dv_max
    dv_min = min(dim_vec)
    if (min_dim < dv_min):
        min_dim = dv_min
# choose elements from dim_vec
    di0=list(dim_vec).index(min_dim)
    di1=list(dim_vec).index(max_dim)
    dim_index = np.arange(di0,di1+1)

    # read delays
    min_del = min_delay_w.get()
    max_del = max_delay_w.get()
    if (min_del == ''):
        min_del = 1
    min_del = int(min_del)
    if (max_del == ''):
        max_del = 1
    max_del = int(max_del)
    delay_vector = np.arange(min_del, max_del+1)
    ndel=len(delay_vector)
# load 1-d time series signal
    time_series = load_signal()
 # choose output file   
    mb.showinfo(root, 'Choose output file in next window')
    file_out = fd.asksaveasfile(mode='w')
    
 # run probability estimates
    prob_out = embedding_prob_func(
        time_series, delay_vector, dim_vec, dim_index,coeff_mat, use_surr)

#  probOut=np.zeros([ndim,ndel])

# write output
    ndim=len(dim_index)
    r_out=np.zeros(ndim+1)
    head_out=[0]*(ndim+1)
    head_out[0]='delay'
    for idx in range(ndim):
        head_out[idx+1]=f'dim={dim_vec[dim_index[idx]]}'
    with open(file_out.name,'w', newline='') as out_file:
        write_out=csv.writer(out_file)
        write_out.writerow(head_out)
        for irr in range(ndel):
            r_out[0]=delay_vector[irr]
            r_out[1:ndim+1]=prob_out[:,irr]
            write_out.writerow(r_out)
    file_out.name.close()    
    plt.close()
    for iplt in range(ndim):
        plt.plot(delay_vector,prob_out[iplt,:])
    
    plt.legend(dim_vec[dim_index])
    plt.xlabel('delay')
    plt.ylabel('probability')
    plt.show()

    root.destroy()
# -------------------------------------

global prob_out
# minimum and maximum dimensions
lbl_dim1 = tk.Label(root, text="minimum dimension?")
lbl_dim1.pack(side=tk.TOP)
# adding Entry Field
min_entry = tk.Entry(root, width=6)
min_entry.pack(side=tk.TOP)
lbl_dim2 = tk.Label(root, text="maximum dimension?")
lbl_dim2.pack(side=tk.TOP)
# adding Entry Field
max_entry = tk.Entry(root, width=6)
max_entry.pack(side=tk.TOP)
# min and max delays -------------------------
lbl_delay1 = tk.Label(root, text='minimum delay?')
lbl_delay1.pack(side=tk.TOP)
min_delay_w = tk.Entry(root, width=6)
min_delay_w.pack(side=tk.TOP)

lbl_delay2 = tk.Label(root, text='maximum delay?')
lbl_delay2.pack(side=tk.TOP)
max_delay_w = tk.Entry(root, width=6)
max_delay_w.pack(side=tk.TOP)

# choose whether to use default coefficients or load from file
choose_coeff = tk.StringVar()
choices = (('Yes', 'y'),
           ('No', 'n'),
           )
label_coeff = ttk.Label(text="Use default coefficients?")
label_coeff.pack(fill='x', padx=5, pady=5)

# radio buttons
choose_coeff.set(0)
for choice in choices:
    r = ttk.Radiobutton(
        root,
        text=choice[0],
        value=choice[1],
        variable=choose_coeff
    )
    r.pack(fill='x', padx=5, pady=5)

# choose whether compare probabilities to surrogate probabilities
choose_surr = tk.StringVar()
choices_surr = (('Yes', 'True'),
           ('No', 'False'),
           )
label_surr = ttk.Label(text="Compare with surrogate?")
label_surr.pack(fill='x', padx=5, pady=5)

# radio buttons
choose_surr.set(1)
for choice in choices_surr:
    r_cf = ttk.Radiobutton(
        root,
        text=choice[0],
        value=choice[1],
        variable=choose_surr
    )
    r_cf.pack(fill='x', padx=5, pady=5)


button = ttk.Button(
    root,
    text="Run",
    command=clicked_run)

button.pack(fill='x', padx=5, pady=5)


root.mainloop()
