# Build gnss

## Installation
- `sudo apt-get install qt5-default qtcreator -y`
- `sudo apt-get install libqt5serialport5 libqt5serialport5-dev`

## Build
- Create the build directory: `$ mkdir build`
- CD to the build directory: `$ cd build`
- Call qmake referencing the .pro file: `$ qmake ../gps_jeston.pro`
- Call: `$ make`
