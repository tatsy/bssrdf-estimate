#include <Python.h>
#include <numpy/arrayobject.h>

#include <cstdio>
#include <iostream>
#include <vector>

#include "spica.h"

static PyObject* render(PyObject* self, PyObject* args) {
    int width, height, samplePerPixel, numPhotons;
    PyArrayObject* npDistances;
    PyArrayObject* npColors;
    if (!PyArg_ParseTuple(args, "iiiiOO", &width, &height, &samplePerPixel, &numPhotons, &npDistances, &npColors)) {
        PyErr_SetString(PyExc_ValueError, "call with invalid arguments: render(width, height, spp, n_photons, distances, colors)");
        return NULL;
    }

    if (npDistances->descr->type_num != PyArray_FLOAT) {
        PyErr_SetString(PyExc_ValueError, "Distances must be 32-bit float");
        return NULL;
    }

    if (npColors->descr->type_num != PyArray_FLOAT) {
        PyErr_SetString(PyExc_ValueError, "Colors must be 32-bit float");
        return NULL;
    }

    const int numIntervals = npDistances->dimensions[0];
    printf("# of intervals: %d\n", numIntervals);

    std::vector<double> distances(numIntervals);
    std::vector<spica::Color> colors(numIntervals);

    float* distData = (float*)npDistances->data;
    float* colorData = (float*)npColors->data;
    for (int i = 0; i < numIntervals; i++) {
        distances[i] = distData[i];
        const double r = colorData[i * 3 + 0];
        const double g = colorData[i * 3 + 1];
        const double b = colorData[i * 3 + 2];
        colors[i] = spica::Color(r, g, b);
    }

    spica::Scene scene;
    spica::Camera camera;
    spica::kittenEnvmap(&scene, &camera, width, height);

    spica::BSSRDF bssrdf = spica::DiscreteBSSRDF::factory(1.3, distances, colors);

    spica::SubsurfaceSPPMRenderer renderer;
    renderer.render(scene, camera, bssrdf, samplePerPixel, numPhotons, spica::PSEUDO_RANDOM_TWISTER);

    Py_RETURN_NONE;
}

static PyMethodDef render_methods[] = {
    { "render", render, METH_VARARGS, "Rendring kitten with BSSRDF" },
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef render_module = {
    PyModuleDef_HEAD_INIT,
    "render",
    "BSSRDF rendering C module",
    -1,
    render_methods
};

PyMODINIT_FUNC PyInit_render(void) {
    return PyModule_Create(&render_module);
}
