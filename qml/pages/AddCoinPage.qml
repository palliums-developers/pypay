import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"
import "../models"

import PyPay 1.0

Control {
    padding: 8

    signal goBack

    contentItem: Item {
        Image {
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
            text: qsTr("Add Token")
            color: "#333333"
            font.pointSize: 16
            font.weight: Font.Medium
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
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
            model: server.tokenModel
            spacing: 12
            clip: true
            ScrollIndicator.vertical: ScrollIndicator { }
            delegate: Rectangle {
                width: listView.width
                height: 60
                color: "#EBEBF1"
                radius: 14
                MyImage {
                    id: itemImage
                    source: show_icon
                    radius: 20
                    width: 41
                    anchors.left: parent.left
                    anchors.leftMargin: 8
                    anchors.verticalCenter: parent.verticalCenter
                }
                Text {
                    text: show_name
                    anchors.left: itemImage.right
                    anchors.leftMargin: 15
                    anchors.verticalCenter: parent.verticalCenter
                    color: "#333333"
                    font.pointSize: 16
                }
                MySwitch {
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    visible: show_name != "BTC" && show_name != "LBR" && show_name != "VLS"
                    checkable: true
                    checked: server.localPublished.includes(show_name)
                    onClicked: {
                        if (server.localPublished.includes(show_name)) {
                            server.localPublished.splice(server.localPublished.indexOf(show_name), 1)
                        } else {
                            server.localPublished.push(show_name)
                            if (!server.published.includes(show_name)) {
                                //payController.publish_currency(chain, name)
                            }
                        }
                        server.get_token_blanace()
                    }
                }
            }
        }
    }
}
