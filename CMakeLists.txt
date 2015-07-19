cmake_minimum_required(VERSION 3.0.0)
project(bssrdf_estimate)

if (MSVC)
  set(Your_Qt5_DIR "C:/Qt/5.4/msvc_2013_64_opengl/" CACHE STRING "Your_Qt5_DIR")
  set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} ${Your_Qt5_DIR})
endif()

if (MSVC)
  set(LIB_PREFIX "")
  set(LIB_PREFIX ".lib")
else()
  set(LIB_PREFIX "lib")
  set(LIB_SUFFIX ".so")
endif()

if (MSVC)
  find_package(OpenMP)
  if (OPENMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
  endif()
endif()

if (NOT MSVC)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -O2")
endif()

add_subdirectory(submodule)
