# This file is part of PyXfem, a software distributed under the MIT license.
# For any question, please contact the authors cited below.
#
# Copyright (c) 2023
# 	Shaoqi WU <shaoqiwu@outlook.com
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

# basis.py mutiple element types
# Lobatto element are recommended to use

import numpy as np
from abc import ABCMeta, abstractmethod
from functools import cached_property

from SAcouS.acxfem.precompute_matrices import Ke1D, Me1D, Ce1D

            

class Base1DElement(metaclass=ABCMeta):
    """base abstract FE elementary matrix class
    precompute the shape function and its derivative on gauss points
    parameters:
    order: int
        element order
    nodes: ndarray
        1d: [x1, x2]
        2d: [(x1, y1), (x2, y2)]
        3d: [(x1, y1, z1), (x2, y2, z2)]
    """
    def __init__(self, label, order, nodes):
        self.label = label
        self.order = order
        self.nodes = nodes
        self.is_discontinue = False

    @cached_property
    def Jacobian(self):
        """
        compute the Jacobian of the element
        returns:
        J: 
        J=dx/dxi"""

        return np.abs(self.nodes[0]-self.nodes[1])/2

    @cached_property
    def inverse_Jacobian(self):
        return 2/np.abs(self.nodes[0]-self.nodes[1])


class Lobbato1DElement(Base1DElement):
    """FE lobatto 1D basis class
    parameters:
    order: int
        element order

    returns:
    """
    def __init__(self, label, order, nodes):
        super().__init__(label, order, nodes)

    @cached_property
    def ke(self):
        """compute the elementary stiffness matrix
        returns:
        K: ndarray
            elementary stiffness matrix
        """
        Ke = 0
        if self.order == 1:
            Ke =  self.inverse_Jacobian*Ke1D[0]
        elif self.order == 2:
            Ke =  self.inverse_Jacobian*Ke1D[1]
        elif self.order == 3:
            Ke =  self.inverse_Jacobian*Ke1D[2]
        elif self.order == 4:
            Ke =  self.inverse_Jacobian*Ke1D[3]
        else:
            print("quadrtic lobatto not supported yet")
        return Ke
    
    @cached_property
    def me(self):
        """compute the elementary stiffness matrix
        returns:
        m: ndarray
            elementary stiffness matrix
        """
        if self.order == 1:
            Me =  self.Jacobian*Me1D[0]
        elif self.order == 2:
            Me =  self.Jacobian*Me1D[1]
        elif self.order == 3:
            Me =  self.Jacobian*Me1D[2]
        elif self.order == 4:
            Me =  self.Jacobian*Me1D[3]
        else:
            print("quadrtic lobatto not supported yet")
        return Me
    
    @cached_property
    def ce(self):
        """compute the elementary coupling matrix, N(x)B(x)
        returns:
        c: ndarray
            elementary coupling matrix
        """
        if self.order == 1:
            Ce =  Ce1D[0]
        elif self.order == 2:
            Ce =  Ce1D[1]
        elif self.order == 3:
            Ce =  Ce1D[2]
        elif self.order == 4:
            Ce =  Ce1D[3]
        else:
            print("quadrtic lobatto not supported yet")
        return Ce
    
    def get_order(self):
        return self.order
    
    @property
    def nb_internal_dofs(self):
        return self.order-1
    
    @property
    def local_dofs_index(self):
        return np.arange(self.order+1)
    