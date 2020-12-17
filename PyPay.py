#! python3

import sys
import os

from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtCore import QUrl, Qt, QCoreApplication

from pypay.paycontroller import PayController

application_path = (
    os.path.dirname(sys.executable)
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)

if __name__ == '__main__':
    print("starting pypay ...")

    QCoreApplication.setApplicationName("PyPay")
    QCoreApplication.setOrganizationName("Palliums")
    QCoreApplication.setOrganizationDomain("palliums.org")
    QCoreApplication.setApplicationVersion("1.0.0")

    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QGuiApplication(sys.argv)

    file = os.path.join(application_path, "qml/icons/pypay.png")
    QGuiApplication.setWindowIcon(QIcon(file));

    payController = PayController()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("payController", payController)
    file = os.path.join(application_path, "qml/main.qml")
    engine.load(QUrl.fromLocalFile(file))
    if not engine.rootObjects():
        print("not engine.rootObjects()")
        sys.exit(-1)

    try:
        exitCode = app.exec_()

        #del engine
        #del payController
        
        sys.exit(exitCode)
    except:
        print("exiting")
