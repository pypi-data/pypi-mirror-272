# Copyright (C) 2020 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: GPL-3.0-or-later

project(everybeam_pybind11)

if(DEFINED ENV{CIBUILDWHEEL})
  # Build using `cibuildwheel`
  if(CMAKE_VERSION VERSION_LESS "3.18")
    message(
      FATAL_ERROR
        "Package `cibuildwheel` requires CMake >= 3.18, but you have ${CMAKE_VERSION}."
    )
  endif()
  find_package(
    Python
    COMPONENTS Interpreter Development.Module
    REQUIRED)
else()
  # Normal build, not using `cibuildwheel`
  find_package(PythonInterp 3 REQUIRED)
  find_package(PythonLibs 3 REQUIRED)
endif()

# Create the binding library
# pyeverybeam is a temporary alias for everybeam target
pybind11_add_module(
  pyeverybeam
  wrappers/pyelementresponse.cc
  wrappers/pyload.cc
  wrappers/pylobes.cc
  wrappers/pytelescope.cc
  wrappers/pyutils.cc
  wrappers/wrapper.cc)

target_include_directories(pyeverybeam
                           PUBLIC "$<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/cpp>")
target_link_libraries(pyeverybeam PUBLIC everybeam)
set_target_properties(pyeverybeam PROPERTIES OUTPUT_NAME everybeam)
if(SKBUILD)
  set_target_properties(pyeverybeam PROPERTIES INSTALL_RPATH
                                               "$ORIGIN/${INSTALL_LIBDIR}")
endif()

# Define where the python module will be installed. When using scikit-build,
# it must be the current directory; otherwise, use site-packages directory.
if(NOT DEFINED PYTHON_LIBRARY_DIR)
  if(DEFINED SKBUILD)
    set(PYTHON_LIBRARY_DIR .)
  else()
    execute_process(
      COMMAND ${PYTHON_EXECUTABLE} -c
              "import site; print(site.getsitepackages()[0])"
      OUTPUT_VARIABLE PYTHON_DIST_PATH
      OUTPUT_STRIP_TRAILING_WHITESPACE)

    if(PYTHON_DIST_PATH
       MATCHES
       "\\/(lib.*\\/python${PYTHON_VERSION_MAJOR}\\.${PYTHON_VERSION_MINOR}\\/.*)"
    )
      set(PYTHON_LIBRARY_DIR ${CMAKE_MATCH_1})
    else()
      message(
        FATAL_ERROR "Failed to parse PYTHON_DIST_PATH='${PYTHON_DIST_PATH}'")
    endif()
  endif()
endif()

# Install pyeverybeam in site-packages directory
install(
  TARGETS pyeverybeam
  COMPONENT libraries
  LIBRARY DESTINATION ${PYTHON_LIBRARY_DIR})
