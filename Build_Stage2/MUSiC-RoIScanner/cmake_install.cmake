# Install script for directory: /home/home1/institut_3a/karwatzki/1_stage/HDiv/MUSiC-RoIScanner

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "0")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/cvmfs/sft.cern.ch/lcg/releases/binutils/2.37-355ed/x86_64-centos7/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/createLookupTable" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/createLookupTable")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/createLookupTable"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/createLookupTable")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin" TYPE EXECUTABLE FILES "/home/home1/institut_3a/karwatzki/1_stage/HDiv/Build_Stage2/MUSiC-RoIScanner/createLookupTable")
  if(EXISTS "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/createLookupTable" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/createLookupTable")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/cvmfs/sft.cern.ch/lcg/releases/binutils/2.37-355ed/x86_64-centos7/bin/strip" "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/createLookupTable")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/scanClass" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/scanClass")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/scanClass"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/scanClass")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin" TYPE EXECUTABLE FILES "/home/home1/institut_3a/karwatzki/1_stage/HDiv/Build_Stage2/MUSiC-RoIScanner/scanClass")
  if(EXISTS "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/scanClass" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/scanClass")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/cvmfs/sft.cern.ch/lcg/releases/binutils/2.37-355ed/x86_64-centos7/bin/strip" "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/scanClass")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/pCalc" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/pCalc")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/pCalc"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/pCalc")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin" TYPE EXECUTABLE FILES "/home/home1/institut_3a/karwatzki/1_stage/HDiv/Build_Stage2/MUSiC-RoIScanner/pCalc")
  if(EXISTS "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/pCalc" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/pCalc")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/cvmfs/sft.cern.ch/lcg/releases/binutils/2.37-355ed/x86_64-centos7/bin/strip" "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/bin/pCalc")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib/libConvolutionComputer.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib/libConvolutionComputer.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib/libConvolutionComputer.so"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib/libConvolutionComputer.so")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib" TYPE SHARED_LIBRARY FILES "/home/home1/institut_3a/karwatzki/1_stage/HDiv/Build_Stage2/MUSiC-RoIScanner/libConvolutionComputer.so")
  if(EXISTS "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib/libConvolutionComputer.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib/libConvolutionComputer.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/cvmfs/sft.cern.ch/lcg/releases/binutils/2.37-355ed/x86_64-centos7/bin/strip" "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib/libConvolutionComputer.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib/libConvolutionLookup.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib/libConvolutionLookup.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib/libConvolutionLookup.so"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib/libConvolutionLookup.so")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib" TYPE SHARED_LIBRARY FILES "/home/home1/institut_3a/karwatzki/1_stage/HDiv/Build_Stage2/MUSiC-RoIScanner/libConvolutionLookup.so")
  if(EXISTS "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib/libConvolutionLookup.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib/libConvolutionLookup.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/cvmfs/sft.cern.ch/lcg/releases/binutils/2.37-355ed/x86_64-centos7/bin/strip" "$ENV{DESTDIR}/home/home1/institut_3a/karwatzki/1_stage/HDiv/lib/libConvolutionLookup.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

