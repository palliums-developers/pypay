import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"

Rectangle {
    width: 800
    height: 600
    Rectangle {
        anchors.centerIn: parent
        border.color: "#DEDEDE"
        width: row.width
        height: row.height
        Row {
            id: row
            spacing: 8
            leftPadding: 8
            rightPadding: 8
            topPadding: 1
            bottomPadding: 1
            Item {
                width: 100
                height: startInput.contentHeight + startInput.topPadding * 2
                clip: true
                TextInput {
                    id: startInput
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
                    color: "#7038FD"
                }
            }
            Item {
                width: 100
                height: startInput.contentHeight + endInput.topPadding * 2
                clip: true
                TextInput {
                    id: endInput
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
                    color: "#7038FD"
                }
            }
        }
    }
}
