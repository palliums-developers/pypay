import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Text {
    id: root
    color: "#7038FD"
    font.pointSize: 16
    opacity: isHovered ? 0.5 : 1
    signal clicked
    property bool isHovered: false
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
            root.clicked()
        }
        onEntered: {
            isHovered = true
        }
        onExited: {
            isHovered = false
        }
    }
}
