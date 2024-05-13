# This file is part of PyXfem, a software distributed under the MIT license.
# For any question, please contact the authors cited below.
#
# Copyright (c) 2023
# 	Shaoqi WU <shaoqiwu@outlook.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# simple postprocessor for plotting and error computation

from typing import Any
import numpy as np
import matplotlib.pyplot as plt


class BasePostProcess(object):
    def __init__(self, title, *args, **kwargs):
        self.title = title

    def set_figure(self, xaxis, yaxis):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title(self.title)
        self.ax.set_xlabel(xaxis)
        self.ax.set_ylabel(yaxis)

    def compute_error(self, sol, ana_sol, remove=None):
        # relative error

        # Compute the differences between the solutions
        differences = np.abs(ana_sol - sol)

        # Square the differences
        squared_differences = differences ** 2

        # Sum up the squared differences
        sum_squared_differences = np.sum(squared_differences)

        # Divide by the number of nodes
        num_nodes = ana_sol.size
        mean_squared_difference = sum_squared_differences / num_nodes

        # Compute analytical
        abs_analytical = np.sum(np.abs(ana_sol)**2)/num_nodes

        # Relative error
        l2_error = np.sqrt(mean_squared_difference/abs_analytical)

        return l2_error

class PostProcessField(BasePostProcess):

    def __init__(self, x_nodes, title, quantity='Pressure', unit='Pa'):
        super().__init__(title)
        self.x_nodes = x_nodes
        self.quantity = quantity
        self.unit = unit

    
    def plot_sol(self, *sols, file_name=None, save=False):
        self.set_figure('Position(m)', self.quantity+'('+self.unit+')')
        for sol in sols:
            self.ax.plot(self.x_nodes, sol[0], label=sol[1], linestyle=sol[2])
        
        self.ax.legend()
        if save:
            plt.savefig(file_name)

    def save_sol(self, *sols, file_name):
        for sol in sols:
            np.savetxt(file_name, sol[0])
        

    def display_layers(self, *layers_pos):
        for pos in layers_pos:
            self.ax.axvline(x=pos, ls='--', c='k')



    
# frequency response function postprocessor
class PostProcessFRF(BasePostProcess):  

    def __init__(self, freqs, title, acoustic_indicator='SPL'):
        super().__init__(title)
        self.freqs = freqs
        self.operator=acoustic_indicator
        self.unit = ''
        if acoustic_indicator == 'SPL':
            self.unit = 'dB'
        

    def get_operator(self):
        if self.operator == 'SPL(dB)':
            return lambda x: 20*np.log10(np.abs(x))
        elif self.operator == 'SPL(dB) - 2':
            print("Warning: SPL(dB) - 2 is not implemented yet!")


    def plot_sol(self, *sols, save=False, file_name=None):
        self.set_figure('Frequency(Hz)', self.operator+f'({self.unit})')
        for sol in sols:
            sol_r = self.get_operator()(sol[0])
            self.ax.plot(self.freqs, sol_r, label=sol[1], linestyle=sol[2])
        
        self.ax.legend()
        if save:
            plt.savefig(file_name)

    def save_sol(self, *sols, file_name):
        """
        output result as a txt file, res.txt
        {
        // header, PyacoustiX FRF result file
        // Frequency(Hz) SPL(dB)
        100 20.1
        200 30.7
        300 40.4
        400 50.1
        500 48.7
        }
        """
        with open(file_name, 'w') as file:
            # write the header
            file.write('// PyacoustiX FRF result file\n')
            file.write(f'Frequency(Hz) {self.operator}({self.unit})\n')
            for sol in sols:
                file.write(f'\n{sol[1]}')
                sol_r = self.get_operator()(sol[0])
                for i in range(len(sol_r)):
                    file.write(f'{self.freqs[i]} {sol_r[i]}\n')
