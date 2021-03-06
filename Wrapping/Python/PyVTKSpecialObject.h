/*=========================================================================

  Program:   Visualization Toolkit
  Module:    PyVTKSpecialObject.h

  Copyright (c) Ken Martin, Will Schroeder, Bill Lorensen
  All rights reserved.
  See Copyright.txt or http://www.kitware.com/Copyright.htm for details.

     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notice for more information.

=========================================================================*/
/*-----------------------------------------------------------------------
  The PyVTKSpecialObject was created in Feb 2001 by David Gobbi.
  The PyVTKSpecialType class was created in April 2010 by David Gobbi.
-----------------------------------------------------------------------*/

#ifndef __PyVTKSpecialObject_h
#define __PyVTKSpecialObject_h

#include "vtkPython.h"
#include "vtkSystemIncludes.h"

// This for objects not derived from vtkObjectBase

// Prototypes for per-type copy, delete, and print funcs

// copy the object and return the copy
typedef void *(*PyVTKSpecialCopyFunc)(const void *);
// delete the object
typedef void (*PyVTKSpecialDeleteFunc)(void *);
// print the object to the stream
typedef void (*PyVTKSpecialPrintFunc)(ostream& os, const void *);
// compare objects, final arg is on of the following:
// Py_LT, Py_LE, Py_EQ, Py_NE, Py_GT, Py_GE
// return "-1" if the comparison is impossible
typedef int (*PyVTKSpecialCompareFunc)(const void *, const void *, int);
// return a hash from the value of the object, or -1 if error,
// set second arg to '1' if the object is immutable
typedef long (*PyVTKSpecialHashFunc)(const void *, int *);

// Struct to hold special methods, the first three are mandatory
// and the rest are optional.
struct PyVTKSpecialMethods
{
  PyVTKSpecialCopyFunc copy_func;
  PyVTKSpecialDeleteFunc delete_func;
  PyVTKSpecialPrintFunc print_func;
  PyVTKSpecialCompareFunc compare_func;
  PyVTKSpecialHashFunc hash_func;
};

// Unlike PyVTKObject, there is no "meta-type" like PyVTKClass.
// Instead, there is just the following class that contains info
// about each special type.
class VTK_PYTHON_EXPORT PyVTKSpecialType
{
public:
  PyVTKSpecialType() :
    classname(0), docstring(0), methods(0), constructors(0),
    copy_func(0), delete_func(0), print_func(0) {};

  PyVTKSpecialType(
    const char *cname, const char *cdocs[],
    PyMethodDef *cmethods, PyMethodDef *ccons,
    PyVTKSpecialMethods *smethods);

  // general information
  PyObject *classname;
  PyObject *docstring;
  PyMethodDef *methods;
  PyMethodDef *constructors;
  // mandatory functions
  PyVTKSpecialCopyFunc copy_func;
  PyVTKSpecialDeleteFunc delete_func;
  PyVTKSpecialPrintFunc print_func;
  // optional functions
  PyVTKSpecialCompareFunc compare_func;
  PyVTKSpecialHashFunc hash_func;
};

// The PyVTKSpecialObject is very lightweight.
struct PyVTKSpecialObject {
  PyObject_HEAD
  void *vtk_ptr;
  long vtk_hash;
  PyVTKSpecialType *vtk_info;
};

extern "C"
{
VTK_PYTHON_EXPORT
PyObject *PyVTKSpecialType_New(
  PyMethodDef *newmethod, PyMethodDef *methods, PyMethodDef *constructors,
  const char *classname, const char *docstring[],
  PyVTKSpecialMethods *smethods);

VTK_PYTHON_EXPORT
int PyVTKSpecialObject_Check(PyObject *obj);

VTK_PYTHON_EXPORT
PyObject *PyVTKSpecialObject_New(const char *classname, void *ptr);

VTK_PYTHON_EXPORT
PyObject *PyVTKSpecialObject_CopyNew(const char *classname, const void *ptr);
}

#endif
