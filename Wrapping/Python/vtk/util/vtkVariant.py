"""
Utility functions to mimic the template support functions for vtkVariant
"""

import vtk
import vtkConstants

_variant_type_map = {
    'char' : vtkConstants.VTK_CHAR,
    'unsigned char' : vtkConstants.VTK_UNSIGNED_CHAR,
    'signed char' : vtkConstants.VTK_SIGNED_CHAR,
    'short' : vtkConstants.VTK_SHORT,
    'unsigned short' : vtkConstants.VTK_UNSIGNED_SHORT,
    'int' : vtkConstants.VTK_INT,
    'unsigned int' : vtkConstants.VTK_UNSIGNED_INT,
    'long' : vtkConstants.VTK_LONG,
    'unsigned long' : vtkConstants.VTK_UNSIGNED_LONG,
    'long long' : vtkConstants.VTK_LONG_LONG,
    'unsigned long long' : vtkConstants.VTK_UNSIGNED_LONG_LONG,
    '__int64' : vtkConstants.VTK___INT64,
    'unsigned __int64' : vtkConstants.VTK_UNSIGNED___INT64,
    'float' : vtkConstants.VTK_FLOAT,
    'double' : vtkConstants.VTK_DOUBLE,
    'string' : vtkConstants.VTK_STRING,
    'unicode string' : vtkConstants.VTK_UNICODE_STRING,
    'vtkObjectBase' : vtkConstants.VTK_OBJECT,
    'vtkObject' : vtkConstants.VTK_OBJECT,
}

_variant_method_map = {
    vtk.VTK_CHAR : 'ToChar',
    vtk.VTK_UNSIGNED_CHAR : 'ToUnsignedChar',
    vtk.VTK_SIGNED_CHAR : 'ToSignedChar',
    vtk.VTK_SHORT : 'ToShort',
    vtk.VTK_UNSIGNED_SHORT : 'ToUnsignedShort',
    vtk.VTK_INT : 'ToInt',
    vtk.VTK_UNSIGNED_INT : 'ToUnsignedInt',
    vtk.VTK_LONG : 'ToLong',
    vtk.VTK_UNSIGNED_LONG : 'ToUnsignedLong',
    vtk.VTK_LONG_LONG : 'ToLongLong',
    vtk.VTK_UNSIGNED_LONG_LONG : 'ToUnsignedLongLong',
    vtk.VTK___INT64 : 'To__Int64',
    vtk.VTK_UNSIGNED___INT64 : 'ToUnsigned__Int64',
    vtk.VTK_FLOAT : 'ToFloat',
    vtk.VTK_DOUBLE : 'ToDouble',
    vtk.VTK_STRING : 'ToString',
    vtk.VTK_UNICODE_STRING : 'ToUnicodeString',
    vtk.VTK_OBJECT : 'ToVTKObject',
}

_variant_check_map = {
    vtk.VTK_CHAR : 'IsChar',
    vtk.VTK_UNSIGNED_CHAR : 'IsUnsignedChar',
    vtk.VTK_SIGNED_CHAR : 'IsSignedChar',
    vtk.VTK_SHORT : 'IsShort',
    vtk.VTK_UNSIGNED_SHORT : 'IsUnsignedShort',
    vtk.VTK_INT : 'IsInt',
    vtk.VTK_UNSIGNED_INT : 'IsUnsignedInt',
    vtk.VTK_LONG : 'IsLong',
    vtk.VTK_UNSIGNED_LONG : 'IsUnsignedLong',
    vtk.VTK_LONG_LONG : 'IsLongLong',
    vtk.VTK_UNSIGNED_LONG_LONG : 'IsUnsignedLongLong',
    vtk.VTK___INT64 : 'Is__Int64',
    vtk.VTK_UNSIGNED___INT64 : 'IsUnsigned__Int64',
    vtk.VTK_FLOAT : 'IsFloat',
    vtk.VTK_DOUBLE : 'IsDouble',
    vtk.VTK_STRING : 'IsString',
    vtk.VTK_UNICODE_STRING : 'IsUnicodeString',
    vtk.VTK_OBJECT : 'IsVTKObject',
}


def vtkVariantCreate(v, t):
    """
    Create a vtkVariant of the specified type, where the type is in the
    following format: 'int', 'unsigned int', etc. for numeric types,
    and 'string' or 'unicode string' for strings.  You can also use an
    integer VTK type constant for the type.
    """
    if not issubclass(type(t), int):
        i = _variant_type_map[t]

    return vtk.vtkVariant(v, i)


def vtkVariantExtract(v, t=None):
    """
    Extract the specified value type from the vtkVariant, where the type is
    in the following format: 'int', 'unsigned int', etc. for numeric types,
    and 'string' or 'unicode string' for strings.  You can also use an
    integer VTK type constant for the type.  Set the type to 'None" to
    extract the value in its native type.
    """
    if t == None:
        t = v.GetType()
    elif not issubclass(type(t), int):
        t = _variant_type_map[t]

    if getattr(v, _variant_check_map[t])():
        return getattr(v, _variant_method_map[t])()
    else:
        return None


def vtkVariantCast(v, t):
    """
    Cast the vtkVariant to the specified value type, where the type is
    in the following format: 'int', 'unsigned int', etc. for numeric types,
    and 'string' or 'unicode string' for strings.  You can also use an
    integer VTK type constant for the type.
    """
    if not issubclass(type(t), int):
        t = _variant_type_map[t]

    v = vtk.vtkVariant(v, i)

    if v.IsValid():
        return getattr(v, _variant_method_map[t])()
    else:
        return None


def vtkVariantStrictWeakOrder(s1, s2):
    """
    Compare variants by type first, and then by value.  The return values
    are -1, 0, 1 like the python cmp() method, for compatibility with the
    python list sort() method.  This is in contrast with the C++ version,
    which returns true or false.
    """
    t1 = s1.GetType()
    t2 = s2.GetType()

    # check based on type
    if t1 != t2:
        return cmp(t1,t2)

    v1 = s1.IsValid()
    v2 = s2.IsValid()

    # check based on validity
    if (not v1) and (not v2):
        return 0
    elif v1 != v2:
        return cmp(v1,v2)

    # extract and compare the values
    r1 = getattr(s1, _variant_method_map[t1])()
    r2 = getattr(s2, _variant_method_map[t2])()

    # compare vtk objects by classname
    if t1 == vtk.VTK_OBJECT:
        return cmp(r1.GetClassName(), r2.GetClassName())

    return cmp(r1, r2)


def vtkVariantStrictEquality(s1, s2):
    """
    Check two variants for strict equality of type and value.
    """
    t1 = s1.GetType()
    t2 = s2.GetType()

    # check based on type
    if t1 != t2:
        return False

    v1 = s1.IsValid()
    v2 = s2.IsValid()

    # check based on validity
    if (not v1) and (not v2):
        return True
    elif v1 != v2:
        return False

    # extract and compare the values
    r1 = getattr(s1, _variant_method_map[t1])()
    r2 = getattr(s2, _variant_method_map[t2])()

    return (r1 == r2)


def vtkVariantLessThan(s1, s2):
    """
    Return true if s1 < s2.  This isn't very useful in Python.
    """
    return (s1 < s2)


def vtkVariantEqual(s1, s2):
    """
    Return true if s1 == s2.  This isn't very useful in Python.
    """
    return (s1 == s2)
