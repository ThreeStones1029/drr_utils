# CMAKE generated file: DO NOT EDIT!
<<<<<<< HEAD
# Generated by "Unix Makefiles" Generator, CMake Version 3.16
=======
# Generated by "Unix Makefiles" Generator, CMake Version 3.29
>>>>>>> e4cabe67df4300438505cc494d7a991b10bae731

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

<<<<<<< HEAD

=======
>>>>>>> e4cabe67df4300438505cc494d7a991b10bae731
#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

<<<<<<< HEAD

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

=======
# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
>>>>>>> e4cabe67df4300438505cc494d7a991b10bae731
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
<<<<<<< HEAD
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f
=======
CMAKE_COMMAND = /root/anaconda3/lib/python3.11/site-packages/cmake/data/bin/cmake

# The command to remove a file.
RM = /root/anaconda3/lib/python3.11/site-packages/cmake/data/bin/cmake -E rm -f
>>>>>>> e4cabe67df4300438505cc494d7a991b10bae731

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
<<<<<<< HEAD
CMAKE_SOURCE_DIR = /home/jjf/Desktop/drr_utils/ITK_tools/Linux_ITK_Gen_Drr

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/jjf/Desktop/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/build

# Include any dependencies generated for this target.
include CMakeFiles/itk_multi_drrs.dir/depend.make
=======
CMAKE_SOURCE_DIR = /home/drr_utils/ITK_tools/Linux_ITK_Gen_Drr

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/build

# Include any dependencies generated for this target.
include CMakeFiles/itk_multi_drrs.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/itk_multi_drrs.dir/compiler_depend.make
>>>>>>> e4cabe67df4300438505cc494d7a991b10bae731

# Include the progress variables for this target.
include CMakeFiles/itk_multi_drrs.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/itk_multi_drrs.dir/flags.make

CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.o: CMakeFiles/itk_multi_drrs.dir/flags.make
<<<<<<< HEAD
CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.o: ../gen_multidrrs.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/jjf/Desktop/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.o -c /home/jjf/Desktop/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/gen_multidrrs.cpp

CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/jjf/Desktop/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/gen_multidrrs.cpp > CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.i

CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/jjf/Desktop/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/gen_multidrrs.cpp -o CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.s
=======
CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.o: /home/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/gen_multidrrs.cpp
CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.o: CMakeFiles/itk_multi_drrs.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.o -MF CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.o.d -o CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.o -c /home/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/gen_multidrrs.cpp

CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/gen_multidrrs.cpp > CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.i

CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/gen_multidrrs.cpp -o CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.s
>>>>>>> e4cabe67df4300438505cc494d7a991b10bae731

# Object files for target itk_multi_drrs
itk_multi_drrs_OBJECTS = \
"CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.o"

# External object files for target itk_multi_drrs
itk_multi_drrs_EXTERNAL_OBJECTS =

libitk_multi_drrs.so: CMakeFiles/itk_multi_drrs.dir/gen_multidrrs.cpp.o
libitk_multi_drrs.so: CMakeFiles/itk_multi_drrs.dir/build.make
<<<<<<< HEAD
libitk_multi_drrs.so: /usr/local/lib/libitkdouble-conversion-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitksys-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkvnl_algo-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkvnl-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkv3p_netlib-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkvcl-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKCommon-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkNetlibSlatec-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKStatistics-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKTransform-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKMesh-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkzlib-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKMetaIO-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKSpatialObjects-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKPath-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKLabelMap-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKMathematicalMorphology-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKQuadEdgeMesh-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKFastMarching-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOImageBase-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKSmoothing-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKImageFeature-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKOptimizers-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKPolynomials-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKBiasCorrection-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKColormap-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKFFT-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKConvolution-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKDICOMParser-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKDeformableMesh-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKDenoising-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKDiffusionTensorImage-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKEXPAT-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmDICT-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmMSFF-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKznz-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKniftiio-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKgiftiio-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKPDEDeformableRegistration-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkhdf5_cpp-static-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkhdf5-static-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOBMP-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOBioRad-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOBruker-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOCSV-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOGDCM-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOIPL-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOGE-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOGIPL-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOHDF5-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkjpeg-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOJPEG-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkopenjpeg-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOJPEG2000-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitktiff-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOTIFF-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOLSM-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkminc2-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMINC-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMRC-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshBase-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshBYU-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshFreeSurfer-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshGifti-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshOBJ-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshOFF-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshVTK-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeta-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIONIFTI-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKNrrdIO-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIONRRD-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkpng-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOPNG-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOSiemens-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOXML-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOSpatialObjects-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOStimulate-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKTransformFactory-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOTransformBase-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOTransformHDF5-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOTransformInsightLegacy-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOTransformMatlab-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOVTK-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKKLMRegionGrowing-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitklbfgs-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKMarkovRandomFieldsClassifiers-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKOptimizersv4-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKQuadEdgeMeshFiltering-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKRegionGrowing-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKRegistrationMethodsv4-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKTestKernel-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKVTK-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKVideoCore-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKVideoIO-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKWatersheds-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKFFT-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkopenjpeg-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkminc2-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOIPL-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOXML-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkhdf5_cpp-static-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkhdf5-static-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOTransformBase-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKTransformFactory-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKImageFeature-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKOptimizersv4-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKOptimizers-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitklbfgs-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOBMP-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOGDCM-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmMSFF-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmDICT-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmIOD-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmDSED-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmCommon-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmjpeg8-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmjpeg12-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmjpeg16-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmopenjp2-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmcharls-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmuuid-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOGIPL-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOJPEG-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOTIFF-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitktiff-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkjpeg-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshBYU-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshFreeSurfer-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshGifti-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKgiftiio-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKEXPAT-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshOBJ-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshOFF-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshVTK-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshBase-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKQuadEdgeMesh-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeta-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKMetaIO-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIONIFTI-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKniftiio-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKznz-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIONRRD-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKNrrdIO-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOPNG-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkpng-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkzlib-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOVTK-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOImageBase-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKVideoCore-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKMathematicalMorphology-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKStatistics-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkNetlibSlatec-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKSpatialObjects-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKMesh-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKTransform-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKPath-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKCommon-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkdouble-conversion-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitksys-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKVNLInstantiation-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkvnl_algo-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkvnl-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkv3p_netlib-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libitkvcl-5.2.a
libitk_multi_drrs.so: /usr/local/lib/libITKSmoothing-5.2.a
libitk_multi_drrs.so: CMakeFiles/itk_multi_drrs.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/jjf/Desktop/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared library libitk_multi_drrs.so"
=======
libitk_multi_drrs.so: /usr/local/lib/libitkdouble-conversion-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitksys-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkvnl_algo-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkvnl-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkv3p_netlib-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkvcl-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKCommon-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkNetlibSlatec-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKStatistics-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKTransform-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKMesh-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkzlib-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKMetaIO-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKSpatialObjects-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKPath-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKLabelMap-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKMathematicalMorphology-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKQuadEdgeMesh-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKFastMarching-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOImageBase-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKFFT-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKConvolution-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKSmoothing-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKImageFeature-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKOptimizers-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKPolynomials-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKBiasCorrection-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKColormap-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKDICOMParser-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKDeformableMesh-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKDenoising-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKDiffusionTensorImage-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKEXPAT-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmDICT-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmMSFF-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKznz-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKniftiio-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKgiftiio-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKPDEDeformableRegistration-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkhdf5_cpp-static-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkhdf5-static-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkhdf5_hl-static-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOBMP-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOBioRad-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOBruker-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOCSV-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOGDCM-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOIPL-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOGE-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOGIPL-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOHDF5-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkjpeg-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOJPEG-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkopenjpeg-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOJPEG2000-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitktiff-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOTIFF-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOLSM-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkminc2-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMINC-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMRC-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshBase-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshBYU-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshFreeSurfer-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshGifti-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshOBJ-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshOFF-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshVTK-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeta-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIONIFTI-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKNrrdIO-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIONRRD-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkpng-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOPNG-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOSiemens-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOXML-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOSpatialObjects-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOStimulate-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKTransformFactory-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOTransformBase-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOTransformHDF5-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOTransformInsightLegacy-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOTransformMatlab-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOVTK-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKKLMRegionGrowing-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitklbfgs-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKMarkovRandomFieldsClassifiers-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKOptimizersv4-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKQuadEdgeMeshFiltering-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKRegionGrowing-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKRegistrationMethodsv4-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKTestKernel-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKVTK-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKVideoCore-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKVideoIO-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKWatersheds-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkopenjpeg-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkminc2-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOIPL-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOXML-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkhdf5_cpp-static-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkhdf5_hl-static-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkhdf5-static-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOTransformBase-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKTransformFactory-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKImageFeature-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKOptimizersv4-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKOptimizers-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitklbfgs-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKFFT-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOBMP-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOGDCM-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmMSFF-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmDICT-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmIOD-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmDSED-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmCommon-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmjpeg8-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmjpeg12-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmjpeg16-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmopenjp2-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmcharls-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkgdcmuuid-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOGIPL-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOJPEG-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOTIFF-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitktiff-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkjpeg-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshBYU-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshFreeSurfer-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshGifti-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKgiftiio-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKEXPAT-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshOBJ-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshOFF-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshVTK-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeshBase-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKQuadEdgeMesh-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOMeta-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKMetaIO-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIONIFTI-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKniftiio-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKznz-5.3.a
libitk_multi_drrs.so: /usr/lib/x86_64-linux-gnu/libm.so
libitk_multi_drrs.so: /usr/local/lib/libITKIONRRD-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKNrrdIO-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOPNG-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkpng-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkzlib-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOVTK-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKIOImageBase-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKVideoCore-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKMathematicalMorphology-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKStatistics-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkNetlibSlatec-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKSpatialObjects-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKMesh-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKTransform-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKPath-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKCommon-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkdouble-conversion-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitksys-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKVNLInstantiation-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkvnl_algo-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkvnl-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkv3p_netlib-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libitkvcl-5.3.a
libitk_multi_drrs.so: /usr/local/lib/libITKSmoothing-5.3.a
libitk_multi_drrs.so: CMakeFiles/itk_multi_drrs.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/home/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared library libitk_multi_drrs.so"
>>>>>>> e4cabe67df4300438505cc494d7a991b10bae731
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/itk_multi_drrs.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/itk_multi_drrs.dir/build: libitk_multi_drrs.so
<<<<<<< HEAD

=======
>>>>>>> e4cabe67df4300438505cc494d7a991b10bae731
.PHONY : CMakeFiles/itk_multi_drrs.dir/build

CMakeFiles/itk_multi_drrs.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/itk_multi_drrs.dir/cmake_clean.cmake
.PHONY : CMakeFiles/itk_multi_drrs.dir/clean

CMakeFiles/itk_multi_drrs.dir/depend:
<<<<<<< HEAD
	cd /home/jjf/Desktop/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/jjf/Desktop/drr_utils/ITK_tools/Linux_ITK_Gen_Drr /home/jjf/Desktop/drr_utils/ITK_tools/Linux_ITK_Gen_Drr /home/jjf/Desktop/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/build /home/jjf/Desktop/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/build /home/jjf/Desktop/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/build/CMakeFiles/itk_multi_drrs.dir/DependInfo.cmake --color=$(COLOR)
=======
	cd /home/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/drr_utils/ITK_tools/Linux_ITK_Gen_Drr /home/drr_utils/ITK_tools/Linux_ITK_Gen_Drr /home/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/build /home/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/build /home/drr_utils/ITK_tools/Linux_ITK_Gen_Drr/build/CMakeFiles/itk_multi_drrs.dir/DependInfo.cmake "--color=$(COLOR)"
>>>>>>> e4cabe67df4300438505cc494d7a991b10bae731
.PHONY : CMakeFiles/itk_multi_drrs.dir/depend

