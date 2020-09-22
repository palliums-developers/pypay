import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

Rectangle {
    id: control
    width: 300
    height: 50

    property string placeholderText: ""
    property alias text: textField.text

    TextField {
        id: textField
        anchors.top: parent.top
        anchors.topMargin: 5
        anchors.left: parent.left
        anchors.leftMargin: 5
        anchors.right: parent.right
        anchors.rightMargin: 5
        anchors.bottom: parent.bottom
        anchors.bottomMargin: lineText.height + 5
        placeholderText: control.placeholderText
        background: Rectangle {
            border.color: "#FFFFFF"
        }
        selectByMouse: true
    }

    Rectangle {
        id: lineText
        anchors.top: textField.bottom
        anchors.topMargin: 1
        anchors.left: textField.left
        anchors.right: textField.right
        height: 1
        color: textField.activeFocus ? "#FD6565" : "#979797"
    }
}
