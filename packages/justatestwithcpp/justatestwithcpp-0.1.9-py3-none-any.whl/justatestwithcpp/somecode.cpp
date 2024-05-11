// cppimport
#include <pybind11/pybind11.h>

namespace py = pybind11;

int square(int x) {
    return x * x;
}
// expose w/ pybind11
PYBIND11_MODULE(somecode, m) {
    m.def("square", &square); 
}
/*
<%
setup_pybind11(cfg)
%>
*/