import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

Rectangle {
    id: root
    width: 642
    height: 50
    border.color: textField.activeFocus ? "#FD6565" : "#979797"

    property string placeholderText: ""
    property alias text: textField.text
    property alias chain: control.chain
    property alias name: control.name
    signal tokenSelectedChanged
    property bool isShowViolasCoin: true

    TextField {
        id: textField
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: 2
        anchors.right: parent.right
        anchors.rightMargin: control.width + 5
        placeholderText: root.placeholderText
        background: Rectangle {
            border.color: "#FFFFFF"
        }
        selectByMouse: true
    }

    TokenComboBox {
        id: control
        anchors.right: parent.right
        anchors.rightMargin: 5
        anchors.verticalCenter: parent.verticalCenter
        isShowViolasCoin: root.isShowViolasCoin
        onTokenSelected: {
            tokenSelectedChanged()
        }
    }
}
