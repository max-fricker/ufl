#!/usr/bin/env python

__authors__ = "Martin Sandve Alnes"
__date__ = "2008-08-22 -- 2008-09-28"

from ufltestcase import UflTestCase, main

from ufl import *
from ufl.algorithms import * 

class MassTestCase(UflTestCase):
    
    def setUp(self):
        pass
    
    def test_something(self):
        element = FiniteElement("CG", "triangle", 1)
        
        v = TestFunction(element)
        u = TrialFunction(element)
        w = Coefficient(element)
        
        f = (w**2/2)*dx
        L = w*v*dx
        a = u*v*dx
        F  = derivative(f, w, v)
        J1 = derivative(L, w, u)
        J2 = derivative(F, w, u)
        
        #self.assertEqual(F, L)
        #self.assertEqual(J1, J2)
        #self.assertEqual(J1, a)
        #self.assertEqual(J2, a)
        # TODO: Apply algorithms of various kinds
        # and verify that (a, J1, J2) are equivalent,
        # as well as (L, F).


if __name__ == "__main__":
    main()