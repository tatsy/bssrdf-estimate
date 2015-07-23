#include <Python.h>
#include <numpy/arrayobject.h>

#include <cmath>
#include <cstdio>

const double EPS = 1.0e-12;

static bool importArray() {
    import_array1(-1);
}

static PyObject* bilateral_filter(PyObject* self, PyObject* args) {
    double sigma_s, sigma_c;
    int winsize;
    PyArrayObject* npImage;
    PyArrayObject* npOutput;

    if (!PyArg_ParseTuple(args, "Oddi", &npImage, &sigma_s, &sigma_c, &winsize)) {
        PyErr_SetString(PyExc_ValueError, "call with invalid arguments: bilateral_filter(image, sigma_s, sigma_c)");
        return NULL;
    }

    if (npImage->nd != 2 && npImage->nd != 3) {
        PyErr_SetString(PyExc_ValueError, "Assertion failed: image.ndim must be 2 or 3");
        return NULL;
    }

    if (npImage->descr->type_num != PyArray_FLOAT) {
        PyErr_SetString(PyExc_ValueError, "Image must be 32-bit float");
        return NULL;
    }

    const int height = (int)npImage->dimensions[0];
    const int width  = (int)npImage->dimensions[1];
    const int dim    = npImage->nd == 2 ? 1 : (int)npImage->dimensions[2];

    // !! This is very important line
    // !! You need this line when you use factory method PyArray_xxxx
    importArray();

    // Make output
    int dims[3] = { height, width, dim };
    npOutput = (PyArrayObject*)PyArray_FromDims(npImage->nd, dims, NPY_FLOAT);

    const int dd = (winsize + 1) / 2;
    const double ss2 = 2.0 * sigma_s * sigma_s;
    const double sc2 = 2.0 * sigma_c * sigma_c;

    float* imdata = (float*)npImage->data;
    float* outdata = (float*)npOutput->data;
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            double sumCol[3] = {0};
            double sumWgt = 0.0;
            for (int dy = -dd; dy <= dd; dy++) {
                for (int dx = -dd; dx <= dd; dx++) {
                    const int nx = x + dx;
                    const int ny = y + dy;
                    if (nx >= 0 && ny >= 0 && nx < width && ny < height) {
                        const double wgt_s = exp(- (dx * dx + dy * dy) / ss2);
                        double wgt_c = 0.0;
                        for (int d = 0; d < dim; d++) {
                            double diff = imdata[(y * width + x) * dim + d] - imdata[(ny * width + nx) * dim + d];
                            wgt_c += diff * diff;
                        }
                        wgt_c = exp(- wgt_c / sc2);

                        const double wgt = wgt_s * wgt_c;
                        for (int d = 0; d < dim; d++) {
                            sumCol[d] += wgt * imdata[(ny * width + nx) * dim + d];
                        }
                        sumWgt += wgt;
                    }
                }
            }

            for (int d = 0; d < dim; d++) {
                outdata[(y * width + x) * dim + d] = (float)(sumCol[d] / (sumWgt + EPS));
            }
        }
    }
    return Py_BuildValue("O", npOutput);
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
