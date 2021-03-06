/*=========================================================================

  Program:   Visualization Toolkit
  Module:    vtkTestingInteractor.h

  Copyright (c) Ken Martin, Will Schroeder, Bill Lorensen
  All rights reserved.
  See Copyright.txt or http://www.kitware.com/Copyright.htm for details.

     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyrgight notice for more information.

=========================================================================*/
// .NAME vtkTestingInteractor - A RenderWindowInteractor for testing
// .SECTION Description
// Provides a Start() method that passes arguments to a test for
// regression testing and returns. This permits programs that
// run as tests to exit gracefully during the test run without needing
// interaction.
// .SECTION See Also
// vtkTestingObjectFactory

#ifndef __vtkTestingInteractor_h
#define __vtkTestingInteractor_h

#include "vtkRenderWindowInteractor.h"

//BTX
#include <string> // STL Header; Required for string
//ETX

class VTK_RENDERING_EXPORT vtkTestingInteractor : public vtkRenderWindowInteractor
{
public:
  static vtkTestingInteractor* New();
  vtkTypeMacro(vtkTestingInteractor,vtkRenderWindowInteractor);
  virtual void Start();

  static int      TestReturnStatus;  // Return status of the test
  static std::string ValidBaseline;     // Name of the Baseline image
  static std::string TempDirectory;     // Location of Testing/Temporary
  static std::string DataDirectory;     // Location of VTKData

protected:
  vtkTestingInteractor() {}

private:
  vtkTestingInteractor(const vtkTestingInteractor&); // Not implemented
  void operator=(const vtkTestingInteractor&);       // Not implemented

};

#endif
