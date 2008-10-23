"""Utility algorithms for inspection of and information extraction from UFL objects in various ways."""

from __future__ import absolute_import

__authors__ = "Martin Sandve Alnes"
__date__ = "2008-03-14 -- 2008-10-21"

# Modified by Anders Logg, 2008

from itertools import chain

from ..output import ufl_assert, ufl_error
from ..common import lstr
from ..base import UFLObject
from ..algebra import Sum, Product
from ..basisfunction import BasisFunction
from ..function import Function
from ..indexing import DefaultDimType
from ..form import Form
from ..integral import Integral
from .traversal import iter_expressions, post_traversal

# FIXME: Many of these need to traverse Variable objects as well!
#        (Split Variable into two classes? One for the user for diff etc, and one for internal usage? (f.ex. Token))

#--- Utilities to extract information from an expression ---

def extract_type(a, ufl_type):
    """Build a set of all objects of class ufl_type found in a.
    The argument a can be a Form, Integral or UFLObject."""
    iter = (o for e in iter_expressions(a) \
              for (o, stack) in post_traversal(e) \
              if isinstance(o, ufl_type) )
    return set(iter)

def extract_classes(a):
    """Build a set of all unique UFLObject subclasses used in a.
    The argument a can be a Form, Integral or UFLObject."""
    c = set()
    for e in iter_expressions(a):
        for (o, stack) in post_traversal(e):
            c.add(type(o))
    return c

def extract_domain(a):
    "Find the polygonal domain of Form a."
    element = extract_elements(a)
    domain = element[0].domain()
    return domain

def extract_value_shape(expression, dimension):
    "Evaluate the value shape of expression with given implicit dimension."
    ufl_assert(isinstance(expression, UFLObject), "Expecting UFL expression.")
    ufl_assert(isinstance(dimension, int), "Expecting int dimension.")
    s = expression.shape()
    shape = []
    for i in s:
        if isinstance(i, DefaultDimType):
            shape.append(dimension)
        else:
            shape.append(i)
    return tuple(shape)

def extract_basisfunctions(a):
    """Build a sorted list of all basisfunctions in a,
    which can be a Form, Integral or UFLObject."""
    # build set of all unique basisfunctions
    s = extract_type(a, BasisFunction)
    # sort by count
    l = sorted(s, cmp=lambda x,y: cmp(x._count, y._count))
    return l

def extract_coefficients(a):
    """Build a sorted list of all coefficients in a,
    which can be a Form, Integral or UFLObject."""
    # build set of all unique coefficients
    s = extract_type(a, Function)
    # sort by count
    l = sorted(s, cmp=lambda x,y: cmp(x._count, y._count))
    return l

# alternative implementation, kept as an example:
def _coefficients(a):
    """Build a sorted list of all coefficients in a,
    which can be a Form, Integral or UFLObject."""
    # build set of all unique coefficients
    s = set()
    def func(o):
        if isinstance(o, Function):
            s.add(o)
    walk(a, func)
    # sort by count
    l = sorted(s, cmp=lambda x,y: cmp(x._count, y._count))
    return l

def extract_elements(a):
    "Build a sorted list of all elements used in a."
    return [f._element for f in chain(extract_basisfunctions(a), extract_coefficients(a))]

def extract_unique_elements(a):
    "Build a set of all unique elements used in a."
    return set(extract_elements(a))

def extract_variables(a):
    """Build a set of all Variable objects in a,
    which can be a Form, Integral or UFLObject."""
    return extract_type(a, Variable)

def extract_indices(expression):
    "Build a set of all Index objects used in expression."
    multi_indices = extract_type(expression, MultiIndex)
    indices = set()
    for mi in multi_indices:
        indices.update(i for i in mi if isinstance(i, Index))
    return indices

def extract_duplications(expression):
    "Build a set of all repeated expressions in expression."
    ufl_assert(isinstance(expression, UFLObject), "Expecting UFL expression.")
    handled = set()
    duplicated = set()
    for (o, stack) in post_traversal(expression):
        if o in handled:
            duplicated.add(o)
        handled.add(o)
    return duplicated

def extract_monomials(expression, indent=""):
    "Extract monomial representation of expression (if possible)."

    # FIXME: Not yet working, need to include derivatives, integrals etc

    ufl_assert(isinstance(expression, Form) or isinstance(expression, UFLObject), "Expecting UFL form or expression.")

    # Iterate over expressions
    m = []

    print ""
    print "Extracting monomials"

    #cell_integrals = expression.cell_integrals()
    #print cell_integrals
    #print dir(cell_integrals[0].)
    #integrals

    for e in iter_expressions(expression):

        # Check for linearity
        if not e.is_linear():
            ufl_error("Operator is nonlinear, unable to extract monomials: " + str(e))
            
        print indent + "e =", e, str(type(e))
        operands = e.operands()
        if isinstance(e, Sum):
            ufl_assert(len(operands) == 2, "Strange, expecting two terms.")
            m += extract_monomials(operands[0], indent + "  ")
            m += extract_monomials(operands[1], indent + "  ")
        elif isinstance(e, Product):
            ufl_assert(len(operands) == 2, "Strange, expecting two factors.")
            for m0 in extract_monomials(operands[0], indent + "  "):
                for m1 in extract_monomials(operands[1], indent + "  "):
                    m.append(m0 + m1)
        elif isinstance(e, BasisFunction):
            m.append((e,))
        elif isinstance(e, Function):
            m.append((e,))
        else:
            print type(e)
            print e.as_basic()
            print "free indices =", e.free_indices()
            ufl_error("Don't know how to handle expression: %s", str(e))

    return m
