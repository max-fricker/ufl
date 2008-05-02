"""UFL provides an extensive list of predefined finite element
families. Users (or more likely form compilers) may register new
elements by calling the function register_element."""

__authors__ = "Martin Sandve Alnes and Anders Logg"
__date__ = "2008-03-03 -- 2008-05-02"

from output import *

# List of valid elements
ufl_elements = {}

# Function for registering new elements
def register_element(family, short_name, value_rank, degree_range, domains):
    "Register new finite element family"
    ufl_assert(family not in ufl_elements, 'Finite element \"%s\" has already been registered.' % family)
    ufl_elements[family] = (family, short_name, value_rank, degree_range, domains)
    ufl_elements[short_name] = (family, short_name, value_rank, degree_range, domains)

# Register valid elements
register_element("Lagrange", "CG", 0, (1, None),
                 ("interval", "triangle", "tetrahedron", "quadrilateral", "hexahedron"))

register_element("Discontinuous Lagrange", "DG", 0, (0, None),
                 ("interval", "triangle", "tetrahedron", "quadrilateral", "hexahedron"))

register_element("Crouzeix-Raviart", "CR", 0, (1, 1),
                 ("triangle", "tetrahedron"))

register_element("Brezzi-Douglas-Marini", "BDM", 1, (1, None),
                 ("triangle", "tetrahedron"))

register_element("Brezzi-Douglas-Fortin-Marini", "BDFM", 1, (1, None),
                 ("triangle", "tetrahedron"))

register_element("Raviart-Thomas", "RT", 1, (0, None),
                 ("triangle", "tetrahedron"))

register_element("Nedelec 1st kind H(div)", "N1div", 1, (0, None),
                 ("triangle", "tetrahedron"))

register_element("Nedelec 2nd kind H(div)", "N2div", 1, (1, None),
                 ("triangle", "tetrahedron"))

register_element("Nedelec 1st kind H(curl)", "N1curl", 1, (0, None),
                 ("triangle", "tetrahedron"))

register_element("Nedelec 2nd kind H(curl)", "N2curl", 1, (1, None),
                 ("triangle", "tetrahedron"))

register_element("Quadrature", "Q", 0, (None, None),
                 ("interval", "triangle", "tetrahedron", "quadrilateral", "hexahedron"))

register_element("Boundary Quadrature", "BQ", 0, (None, None),
                 ("interval", "triangle", "tetrahedron", "quadrilateral", "hexahedron"))
