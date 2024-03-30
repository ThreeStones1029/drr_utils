<!--
 * @Description: How to install ITK in Ubuntu?
 * @version: 
 * @Author: ThreeStones1029 2320218115@qq.com
 * @Date: 2024-03-29 12:45:14
 * @LastEditors: ShuaiLei
 * @LastEditTime: 2024-03-30 02:06:41
-->
# How to install ITK in Ubuntu?
# 1.install gcc g++
if your system don't have gcc and g++,you can run this command install, Otherwise, you can skip it.
~~~bash
sudo apt install gcc
sudo apt-get install build-essential
~~~
~~~bash
gcc --version # run this command to check whether gcc install successfully
g++ --version # run this command to check whether g++ install successfully
~~~
# 2.Download cmake and install
[cmake down url](https://cmake.org/download/)
~~~bash
cd cmake-3.28.4
./bootstrap
make
sudo make install
~~~
~~~bash
cmake --version # run this command to check whether cmake install successfully
~~~
# 3.install ccmake
~~~bash
sudo apt-get install cmake-curses-gui
~~~
~~~bash
ccmake --version # run this command to check whether ccmake install successfully
~~~
# 4.Download ITK and install.
~~~bash
mkdir ITK
~~~
The decompressed installation package is stored in ITK
~~~bash
cd ITK
mkdir build
~~~
ls ITK will get
~~~bash
├── ITK
    ├── InsightToolkit-5.3.0
    ├── build
~~~
~~~bash
cd build
ccmake ../InsightToolkit-5.3.0
make
sudo make install
~~~
# 5.build gendrr.cpp
you need to modify drr_utils/ITK_tools/Linux_ITK_Gen_Drr/CMakeLists.txt, and set(ITK_DIR "/home/software/ITK") the directory to your ITK path.
Delete the files under the build folder.
~~~bash
cd build 
cmake ..
make
~~~
Then your can start using the drr_utils in your ubuntu system!!!

# 6.your may meet some problems
## 6.1.Could not find OpenSSL.
~~~bash
CMake Error at Utilities/cmcurl/CMakeLists.txt:647 (message):
  Could not find OpenSSL.  Install an OpenSSL development package or
  configure CMake with -DCMAKE_USE_OPENSSL=OFF to build without OpenSSL.
~~~

run this command can solve the problem
~~~bash
sudo apt-get install libssl-dev
~~~

## 6.2.Failed to find "GL/gl.h"
~~~bash
CMake Error at /root/anaconda3/lib/cmake/Qt5Gui/Qt5GuiConfigExtras.cmake:9 (message):
  Failed to find "GL/gl.h" in
  "/root/anaconda3/include;/croot/qt-main_1693210824277/_build_env/x86_64-conda-linux-gnu/sysroot/usr/include;/croot/qt-main_1693210824277/_build_env/x86_64-conda-linux-gnu/sysroot/usr/include/libdrm;/croot/qt-main_1693210824277/_build_env/x86_64-conda-linux-gnu/sysroot/usr/include".
Call Stack (most recent call first):
  /root/anaconda3/lib/cmake/Qt5Gui/Qt5GuiConfig.cmake:233 (include)
  /root/anaconda3/lib/cmake/Qt5Widgets/Qt5WidgetsConfig.cmake:100 (find_package)
  Tests/CMakeLists.txt:280 (find_package)
~~~
run this command can solve the problem
~~~bash
sudo apt-get install libgl1-mesa-dev
~~~
