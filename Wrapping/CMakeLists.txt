# Allow the user to customize their build with some local options
#
INCLUDE (${VTK_SOURCE_DIR}/Wrapping/LocalUserOptions.cmake OPTIONAL)

# vtkParse.tab.c has #line markers that break #include with double quotes.
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})

IF(NOT CMAKE_CROSSCOMPILING)
  IF(NOT VTK_INSTALL_NO_DEVELOPMENT)
    INSTALL(FILES vtkParse.h vtkParseType.h
      DESTINATION ${VTK_INSTALL_INCLUDE_DIR_CM24}
      COMPONENT Development
      )
  ENDIF(NOT VTK_INSTALL_NO_DEVELOPMENT)

  IF(VTK_IGNORE_BTX)
    ADD_DEFINITIONS(-DVTK_IGNORE_BTX)
  ENDIF(VTK_IGNORE_BTX)

  IF (VTK_WRAP_TCL OR VTK_WRAP_PYTHON OR VTK_WRAP_JAVA)
    ADD_EXECUTABLE(vtkWrapHierarchy vtkParse.tab.c vtkWrapHierarchy.c)
  ENDIF (VTK_WRAP_TCL OR VTK_WRAP_PYTHON OR VTK_WRAP_JAVA)

  IF (VTK_WRAP_TCL)
    ADD_EXECUTABLE(vtkWrapTcl vtkWrapTcl.c vtkParseMain.c vtkParse.tab.c
                   vtkParseHierarchy.c)
    ADD_EXECUTABLE(vtkWrapTclInit vtkWrapTclInit.c)
    EXPORT(TARGETS vtkWrapTcl vtkWrapTclInit FILE ${EXPORT_EXECUTABLES_FILE} NAMESPACE "${EXPORT_EXECUTABLES_NAMESPACE}" APPEND)
    IF(COMPILE_TOOLS_TARGET)
      ADD_DEPENDENCIES(${COMPILE_TOOLS_TARGET} vtkWrapTcl vtkWrapTclInit)
   ENDIF(COMPILE_TOOLS_TARGET)
    IF(NOT VTK_INSTALL_NO_DEVELOPMENT)
      INSTALL(TARGETS vtkWrapTcl vtkWrapTclInit
        RUNTIME DESTINATION ${VTK_INSTALL_BIN_DIR_CM24} COMPONENT Development # .exe, .dll
        )
    ENDIF(NOT VTK_INSTALL_NO_DEVELOPMENT)
  ENDIF (VTK_WRAP_TCL)

  IF (VTK_WRAP_PYTHON)
    ADD_EXECUTABLE(vtkWrapPython vtkWrapPython.c vtkParseMain.c vtkParse.tab.c
                   vtkParseHierarchy.c)
    ADD_EXECUTABLE(vtkWrapPythonInit vtkWrapPythonInit.c)
    TARGET_LINK_LIBRARIES(vtkWrapPython ${VTK_PYTHON_LIBRARIES})
    EXPORT(TARGETS vtkWrapPython vtkWrapPythonInit FILE ${EXPORT_EXECUTABLES_FILE} NAMESPACE "${EXPORT_EXECUTABLES_NAMESPACE}" APPEND)
    IF(COMPILE_TOOLS_TARGET)
      ADD_DEPENDENCIES(${COMPILE_TOOLS_TARGET} vtkWrapPython vtkWrapPythonInit)
    ENDIF(COMPILE_TOOLS_TARGET)
    IF(NOT VTK_INSTALL_NO_DEVELOPMENT)
      INSTALL(TARGETS vtkWrapPython vtkWrapPythonInit
        RUNTIME DESTINATION ${VTK_INSTALL_BIN_DIR_CM24} COMPONENT Development # .exe, .dll
        )
    ENDIF(NOT VTK_INSTALL_NO_DEVELOPMENT)
  ENDIF (VTK_WRAP_PYTHON)

  IF (VTK_WRAP_JAVA)
    ADD_EXECUTABLE(vtkParseJava vtkParseJava.c vtkParseMain.c vtkParse.tab.c
                   vtkParseHierarchy.c)
    ADD_EXECUTABLE(vtkWrapJava vtkWrapJava.c vtkParseMain.c vtkParse.tab.c
                   vtkParseHierarchy.c)
    EXPORT(TARGETS vtkParseJava vtkWrapJava FILE ${EXPORT_EXECUTABLES_FILE} NAMESPACE "${EXPORT_EXECUTABLES_NAMESPACE}" APPEND)
    IF(COMPILE_TOOLS_TARGET)
      ADD_DEPENDENCIES(${COMPILE_TOOLS_TARGET} vtkParseJava vtkWrapJava)
    ENDIF(COMPILE_TOOLS_TARGET)
    IF(NOT VTK_INSTALL_NO_DEVELOPMENT)
      INSTALL(TARGETS vtkParseJava vtkWrapJava
        RUNTIME DESTINATION ${VTK_INSTALL_BIN_DIR_CM24} COMPONENT Development # .exe, .dll
        )
    ENDIF(NOT VTK_INSTALL_NO_DEVELOPMENT)
  ENDIF (VTK_WRAP_JAVA)

ENDIF(NOT CMAKE_CROSSCOMPILING)
