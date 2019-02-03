#-------------------------------------------------
#
# Project created by QtCreator 2019-02-03T12:45:05
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = TestProject
TEMPLATE = app

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

CONFIG += c++11

SOURCES += \
        main.cpp \
        widget.cpp

HEADERS += \
        widget.h

FORMS += \
        widget.ui


CUSTOMER = public
CONFIG(customer_a) {
    CUSTOMER = customer_a
}
CONFIG(customer_b) {
    CUSTOMER = customer_b
}

TRANSLATIONS += ./translation/public/en.ts \
                ./translation/public/zh_CN.ts \
                ./translation/public/zh_TW.ts \
                ./translation/public/zh_HK.ts \
                ./translation/public/de.ts \
                ./translation/public/ja.ts

TRANSLATIONS += ./translation/customer_a/en.ts \
                ./translation/customer_a/zh_CN.ts \
                ./translation/customer_a/zh_TW.ts \
                ./translation/customer_a/zh_HK.ts \
                ./translation/customer_a/de.ts \
                ./translation/customer_a/ja.ts

TRANSLATIONS += ./translation/customer_b/en.ts \
                ./translation/customer_b/zh_CN.ts \
                ./translation/customer_b/zh_TW.ts \
                ./translation/customer_b/zh_HK.ts \
                ./translation/customer_b/de.ts \
                ./translation/customer_b/ja.ts


# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
