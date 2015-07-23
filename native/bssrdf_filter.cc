#include <Python.h>
#include <numpy/arrayobject.h>

#include <cstdio>

static PyObject* bilateral_filter(PyObject* self, PyObject* args) {
    double sigma_s, sigma_c;
    PyArrayObject* npImage;

    if (!PyArg_ParseTuple(args, "Odd", &npImage, &sigma_s, &sigma_c)) {
        PyErr_SetString(PyExc_ValueError, "call with invalid arguments: bilateral_filter(image, sigma_s, sigma_c)");
        return NULL;
    }

    if (npImage->nd != 3) {
        PyErr_SetString(PyExc_ValueError, "Assertion failed: image.ndim == 3");
    }

    if (npImage->descr->type_num != PyArray_FLOAT) {
        PyErr_SetString(PyExc_ValueError, "Image must be 32-bit float");
        return NULL;
    }

    const int height = npImage->dimensions[0];
    const int width  = npImage->dimensions[1];
    const int dim    = npImage->dimensions[2];
    printf("size: (%d, %d, %d)\n", height, width, dim);

    Py_RETURN_NONE;
}

static PyMethodDef imfilter_methods[] = {
    { "bilateral_filter", bilateral_filter, METH_VARARGS, "Bilateral filtering" },
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef imfilter_module = {
    PyModuleDef_HEAD_INIT,
    "imfilter",
    "Filgering C module",
    -1,
    imfilter_methods
};

PyMODINIT_FUNC PyInit_imfilter(void) {
    return PyModule_Create(&imfilter_module);
}
