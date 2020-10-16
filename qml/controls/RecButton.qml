import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: root
    property bool isSelected: false
    property bool isEnabled: true
    property string highLightColor: "#7038FDFF"
    property string commonColor: "#C2C2C2FF"
    
    signal clicked

    border.color: isSelected ? highLightColor : commonColor
    opacity: isEnabled ? 1 : 0.2

    MouseArea {
        anchors.fill: parent
        hoverEnabled: isEnabled
        onEntered: {
            root.border.color = highLightColor
        }
        onExited: {
            root.border.color = isSelected ? highLightColor : commonColor
        }
        onClicked: {
            root.clicked()
        }
    }
} 
