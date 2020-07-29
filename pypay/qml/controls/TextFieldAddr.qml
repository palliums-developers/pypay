import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

Rectangle {
    id: control
    width: 642
    height: 110
    border.color: textField.activeFocus ? "#FD6565" : "#979797"

    property string placeholderText: ""
    property alias text: textField.text
    signal addrClicked

    TextField {
        id: textField
        anchors.top: parent.top
        anchors.topMargin: 5
        anchors.left: parent.left
        anchors.leftMargin: 5
        anchors.right: parent.right
        anchors.rightMargin: addrText.width + 5
        placeholderText: control.placeholderText
        background: Rectangle {
            border.color: "#FFFFFF"
        }
        selectByMouse: true
    }

    Text {
        id: addrText
        anchors.right: parent.right
        anchors.rightMargin: 5
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 5
        text: qsTr("地址簿")
        color: "#7038FD"
        property bool isHovered: false
        opacity: addrText.isHovered ? 1 : 0.8
        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: {
                addrText.isHovered = true
            }
            onExited: {
                addrText.isHovered = false
            }
            onClicked: {
                addrClicked()
                console.log("addr")
            }
        }
    }
}
