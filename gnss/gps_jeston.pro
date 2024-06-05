QT += core serialport
QT -= gui

CONFIG += c++11

TARGET = gps_jeston
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

SOURCES += main.cpp \
    utils.cpp \
    eventonesec.cpp

HEADERS += \
    utils.h
