import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"

Control {
    padding: 40

    signal goBack
    signal addAddrClicked
    signal editClicked

    contentItem: Item {
        ImageButton {
            source: "../icons/backarrow.svg"
            anchors.left: parent.left
            anchors.verticalCenter: titleText.verticalCenter
            width: 16
            fillMode: Image.PreserveAspectFit
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    goBack()
                }
            }
        }
        Text {
            id: titleText
            text: qsTr("地址薄")
            color: "#333333"
            font.pointSize: 16
            font.weight: Font.Medium
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
        }

        ImageButton {
            id: addAddr
            source: "../icons/addAddr.svg"
            anchors.right: parent.right
            anchors.verticalCenter: titleText.verticalCenter
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    addAddrClicked()  
                }
            }
        }

        ListView {
            id: listView
            anchors.top: titleText.bottom
            anchors.topMargin: 22
            anchors.left: parent.left
            anchors.leftMargin: 8
            anchors.right: parent.right
            anchors.rightMargin: 8
            anchors.bottom: parent.bottom
            //model: payController.addrBookModel
            spacing: 2
            clip: true
            ScrollIndicator.vertical: ScrollIndicator { }
            delegate: Rectangle {
                anchors.left: parent.left
                anchors.right: parent.right
                height: 40
                Column {
                    id: column
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    Text {
                        text: addrBookEntry.name
                        color: "#333333"
                        font.pointSize: 14
                    }
                    Text {
                        text: addrBookEntry.addr
                        color: "#999999"
                        font.pointSize: 10
                    }
                }
                Text {
                    anchors.right: parent.right
                    anchors.bottom: column.bottom
                    anchors.bottomMargin: 2
                    text: qsTr("编辑")
                    color: "#7038FD"
                    font.pointSize: 10
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            editClicked()
                        }
                    }
                }
                Rectangle {
                    id: line
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 2
                    height: 1
                    color: "#DEDFE0"
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        //payController.currentSelectedAddr = addrBookEntry.addr
                        goBack()                       
                    }
                }
            }
        }
    }
}
