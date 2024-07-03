/* compile like 
 * gcc -g -O3 -march=native -mtune=native -ffast-math -fopenmp --std=gnu11 -lpython3.5m -I/usr/include/python3.5m/ -I/usr/lib/python3.5/site-packages/numpy/core/include/ -fPIC --shared -o mmm_ops.so mmm_ops.c
 */

/* 
* To compile on Mac with python 3.7
* /usr/local/bin/gcc-8 -g -O3 -march=native -mtune=native -ffast-math -fopenmp --std=gnu11 -lpython3.7m -I/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/include/python3.7m -I/usr/local/lib/python3.7/site-packages/numpy/core/include -L/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib -fPIC --shared -o mmm_ops.so mmm_ops.c 
*/

#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/noprefix.h>

#ifdef MMM_OP_NAME
static PyObject *
MMM_OP_NAME(PyObject *dummy, PyObject *args)
{
    PyObject *arg1=NULL, *arg2=NULL, *aout=NULL;
    PyArrayObject *arr1=NULL, *arr2=NULL, *oarr=NULL;

    if (!PyArg_ParseTuple(args, "OOO!", &arg1, &arg2,
        &PyArray_Type, &aout)) return NULL;

    arr1 = (PyArrayObject*) PyArray_FROM_OTF(arg1, NPY_TYPE, NPY_ARRAY_IN_ARRAY);
    if (arr1 == NULL) return NULL;
    arr2 = (PyArrayObject*) PyArray_FROM_OTF(arg2, NPY_TYPE, NPY_ARRAY_IN_ARRAY);
    if (arr2 == NULL) goto fail;
    oarr = (PyArrayObject*) PyArray_FROM_OTF(aout, NPY_TYPE, NPY_ARRAY_INOUT_ARRAY);
    if (oarr == NULL) goto fail;
    
    if (PyArray_NDIM(arr1) != 2 || PyArray_NDIM(arr2) != 2 || PyArray_NDIM(oarr) != 2)
        goto fail;
    
    int n = PyArray_DIM(oarr, 0);
    if (PyArray_DIM(oarr, 0) != n || PyArray_DIM(oarr, 1) != n
     || PyArray_DIM(arr1, 0) != n || PyArray_DIM(arr1, 1) != n
     || PyArray_DIM(arr2, 0) != n || PyArray_DIM(arr2, 1) != n)
        goto fail;
        
    CTYPE* a = (CTYPE*) PyArray_DATA(arr1);
    CTYPE* b = (CTYPE*) PyArray_DATA(arr2);
    CTYPE* out = (CTYPE*) PyArray_DATA(oarr);
    
    for (int i = 0; i < n*n; i++) {
        out[i] = 0;
    }
            
    int BS = 128;
    
    #pragma omp parallel for
    for (int by = 0; by < n+BS-1; by += BS) {
        for (int bx = 0; bx < n+BS-1; bx += BS) {
            for (int bk = 0; bk < n+BS-1; bk += BS) {
                for (int y = by; y < by+BS && y < n; y++) {
                    for (int x = bx; x < bx+BS && x < n; x++) {
                        CTYPE acc = 0;
                        for(int k = bk; k < bk+BS && k < n; k++) {
                            acc += OP(a[k + n*y], b[x + n*k]);
                        }
                        out[x + n*y] += acc;
                    }
                }
            }
        }
    }

    Py_DECREF(arr1);
    Py_DECREF(arr2);
    Py_DECREF(oarr);
    Py_INCREF(aout);
    return aout;

 fail:
    Py_XDECREF(arr1);
    Py_XDECREF(arr2);
    PyArray_XDECREF_ERR(oarr);
    return NULL;
}

#else

#define NPY_TYPE NPY_FLOAT64
#define CTYPE double

#define MMM_OP_NAME mmm_op_mult
#define OP(a, b)  ((a) * (b))
#include "mmm_ops.c"
#undef OP
#undef MMM_OP_NAME

#define MMM_OP_NAME mmm_op_min
#define OP(a, b)  (((a) < (b)) ? (a) : (b))
#include "mmm_ops.c"
#undef OP
#undef MMM_OP_NAME

static PyMethodDef mmm_ops_Methods[] = {
    {"mmm_mult",  mmm_op_mult, METH_VARARGS,
     "Normal Matrix-Matrix Multiplication with multiplication"},
    {"mmm_min",  mmm_op_min, METH_VARARGS,
     "Matrix-Matrix Multiplication with min(x,y) instead of x*y"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef mmm_ops_module = {
   PyModuleDef_HEAD_INIT,
   "mmm_ops",   /* name of module */
   NULL, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   mmm_ops_Methods
};

PyMODINIT_FUNC
PyInit_mmm_ops(void)
{
    PyObject *m;
    
    import_array();

    m = PyModule_Create(&mmm_ops_module);
    if (m == NULL)
        return NULL;

    return m;
}

#endif
