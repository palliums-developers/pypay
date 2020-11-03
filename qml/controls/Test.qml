import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"

Rectangle {
    id: rec
    width: 800
    height: 600
    MouseArea {
        anchors.fill: parent
        onClicked: {
            forceActiveFocus()
        }
    }

    Component {
        id: inputCom
        Item {
            property alias isActiveFocus: textInput.activeFocus
            width: 100
            height: textInput.contentHeight + textInput.topPadding * 2
            clip: true
            TextInput {
                id: textInput
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
                topPadding: 8
                bottomPadding: 8
                text: ""
            }
            Rectangle {
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                height: 1
                color: "#008BFF"
                visible: textInput.activeFocus
            }
        }
    }

    Rectangle {
        anchors.centerIn: parent
        border.color: startInput.item.isActiveFocus || endInput.item.isActiveFocus ? "#38A7FF" : "#D9D9D9"
        width: row.width
        height: row.height
        Row {
            id: row
            spacing: 8
            leftPadding: 8
            rightPadding: 8
            topPadding: 1
            bottomPadding: 1
            Loader { id: startInput; sourceComponent: inputCom }
            Text {
                text: qsTr("->")
                anchors.verticalCenter: parent.verticalCenter
            }
            Loader { id: endInput; sourceComponent: inputCom }
        }
    }

    Button {
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        text: qsTr("Test")
    }
}
