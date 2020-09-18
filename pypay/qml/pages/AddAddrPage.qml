import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

import "../controls"
import "../models"

import PyPay 1.0

Control {
    id: root
    padding: 40

    signal goBack

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
            text: qsTr("添加地址")
            color: "#333333"
            font.pointSize: 16
            font.weight: Font.Medium
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Column {
            id: inputColumn
            anchors.left: parent.left
            anchors.leftMargin: 8
            anchors.top: titleText.bottom
            anchors.topMargin: 40
            spacing: 8
            Row {
                spacing: 8
                Text {
                    id: commentText
                    text: qsTr("备注")
                    font.pointSize: 14
                    color: "#333333"
                }
                TextFieldLine {
                    id: commentTextField
                    width: 300
                    anchors.verticalCenter: commentText.verticalCenter
                    placeholderText: qsTr("请输入备注")
                }
            }
            Row {
                spacing: 8
                Text {
                    id: addrText
                    text: qsTr("地址")
                    font.pointSize: 14
                    color: "#333333"
                }
                TextFieldLine {
                    id: addrTextField
                    width: 300
                    anchors.verticalCenter: addrText.verticalCenter
                    placeholderText: qsTr("请输入地址")
                }
            }
        }

        MyButton3 {
            id: addBtn
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: inputColumn.bottom
            anchors.topMargin: 20
            text: qsTr("添加")
            width: 200
            height: 40
            onClicked: {
                payController.addAddrBook(commentTextField.text, addrTextField.text)
                goBack()
            }
        }
    }
}
