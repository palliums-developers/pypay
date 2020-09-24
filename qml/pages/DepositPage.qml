import QtQuick 2.14
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"
import "../models/ViolasServer.js" as Server

import PyPay 1.0

Page {
    id: root

    property var bankDepositInfo: {}
    property int topMargin: 43
    property int bottomMargin: 49      

    signal backArrowClicked


    function getDepositInfo(id) {
        if (payController.addr) {
            Server.request('GET', '/1.0/violas/bank/deposit/info?id='+ id + '&address=' + payController.addr,
                null, function(resp) {
                    bankDepositInfo = resp.data;
                    console.log(JSON.stringify(bankDepositInfo))
                });
        }
    }

    background: Rectangle {
        color: "#F7F7F9"
    }

    ImageButton {
        id: backBtn
        anchors.top: parent.top
        anchors.topMargin: 72
        anchors.left: parent.left
        anchors.leftMargin: 72
        width: 24
        height: 24
        source: "../icons/backarrow3.svg"
        MouseArea {
            anchors.fill: parent
            onClicked: {
                backArrowClicked()
            }
        }
    }

    Text {
        id: titleText
        text: qsTr("Bank > <b><b>Deposit</b></b>")
        font.pointSize: 14
        color: "#5C5C5C"
        anchors.verticalCenter: backBtn.verticalCenter
        anchors.left: backBtn.right
        anchors.leftMargin: 8
    }

    Flickable {
        clip: true
        anchors.top: parent.top
        anchors.topMargin: 140
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 40
        anchors.horizontalCenter: parent.horizontalCenter
        width: 716
        contentHeight: contentColumn.height + root.topMargin + depositBtn.height + root.bottomMargin + contentColumn2.height

        Column {
            id: contentColumn
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            spacing: 10

            Rectangle {
                id: conRec
                width: parent.width
                height: 170
                color: "#FFFFFF"
                Row {
                    id: conRow
                    anchors.left: parent.left
                    anchors.leftMargin: 50
                    anchors.top: parent.top
                    anchors.topMargin: 32
                    spacing: 8
                    Text {
                        id: storeText
                        text: qsTr("Store")
                        color: "#5C5C5C"
                        font.pointSize: 12
                    }
                    TextFieldLine {
                        id: inputLine
                        width: conRec.width - storeText.contentWidth - tokenText.contentWidth - 50 * 2 - spacing * 2
                        anchors.verticalCenter: storeText.verticalCenter
                        placeholderText: qsTr("minimum_amount: ") + (bankDepositInfo.minimum_amount / 1000000).toFixed(6)
                    }
                    Text {
                        id: tokenText
                        text: bankDepositInfo.token_show_name
                        anchors.verticalCenter: storeText.verticalCenter
                    }
                }
                Row {
                    id: conRow2
                    anchors.left: parent.left
                    anchors.leftMargin: 50
                    anchors.top: conRow.bottom
                    anchors.topMargin: 8
                    spacing: 8
                    Image {
                        id: avaImage
                        width: 12
                        fillMode: Image.PreserveAspectFit
                        source: "../icons/availablebank.svg"
                    }
                    Text {
                        text: qsTr("avaliable balance: ")
                        font.pointSize: 10
                        color: "#5C5C5C"
                        anchors.verticalCenter: avaImage.verticalCenter
                    }
                    Text {
                        text: qsTr("All")
                        color: "#7038FD"
                        font.pointSize: 10
                        anchors.verticalCenter: avaImage.verticalCenter
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                            }
                        }
                    }
                }

                Row {
                    anchors.left: parent.left
                    anchors.leftMargin: 50
                    anchors.top: conRow2.bottom
                    anchors.topMargin: 16
                    spacing: 8
                    Image {
                        id: limitImage
                        width: 12
                        fillMode: Image.PreserveAspectFit
                        source: "../icons/limitbank.svg"
                    }
                    Text {
                        text: qsTr("limit of day: ") + (bankDepositInfo.quota_limit / 1000000).toFixed(6)
                        font.pointSize: 10
                        color: "#5C5C5C"
                        anchors.verticalCenter: limitImage.verticalCenter
                    }
                }
            }

            Rectangle {
                width: parent.width
                height: 219
                color: "#FFFFFF"
            }
        }

        MyButton3 {
            id: depositBtn
            anchors.top: contentColumn.bottom
            anchors.topMargin: root.topMargin
            anchors.horizontalCenter: parent.horizontalCenter
            text: qsTr("Deposit Now")
            width: 200
            height: 40
        }

        Column {
            id: contentColumn2
            anchors.top: depositBtn.bottom
            anchors.topMargin: root.bottomMargin
            anchors.left: parent.left
            anchors.right: parent.right
            spacing: 10

            Rectangle {
                width: parent.width
                height: 175
                color: "#FFFFFF"
            }

            Rectangle {
                width: parent.width
                height: 247
                color: "#FFFFFF"
            }
        }
    }
}
