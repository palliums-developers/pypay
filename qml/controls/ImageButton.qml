import QtQuick 2.14
import QtQuick.Controls 2.14

Image {
    id: control
    property bool isHover: false
    signal clicked
    opacity: isHover ? 0.5 : 1
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onEntered: {
            control.isHover = true
        }
        onExited: {
            control.isHover = false
        }
        onClicked: {
            control.clicked()
        }
    }
}
