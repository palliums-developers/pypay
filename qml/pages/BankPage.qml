import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"
import "../models/ViolasServer.js" as Server

import PyPay 1.0

Page {
    id: root

    signal showDepositPage
    signal showBorrowPage

    property var bankAccountInfo: {}

    Timer {
        interval: 5000
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: {
            getBankAccountInfo()
        }
    }

    function getBankAccountInfo() {
        if (payController.addr) {
            Server.request('GET', '/1.0/violas/bank/account/info?address='+payController.addr, null, function(resp) {
                    bankAccountInfo = resp.data;
                });
        }
    }

    background: Rectangle {
        color: "#F7F7F9"
    }

    Rectangle {
        id: bankRec
        anchors.left: parent.left
        anchors.leftMargin: 134
        anchors.right: parent.right
        anchors.rightMargin: 134
        anchors.top: parent.top
        anchors.topMargin: 77
        height: 226
        color: "#501BA2"
        radius: 24

        Text {
            id: totalText
            text: qsTr("Deposit Balance ($)")
            anchors.top: parent.top
            anchors.topMargin: 16
            anchors.left: parent.left
            anchors.leftMargin: 42
            color: "#FFFFFF"
            font.pointSize: 12
            verticalAlignment: Text.AlignVCenter
        }
        Image {
            id: eyesImage
            anchors.left: totalText.right
            anchors.leftMargin: 8
            anchors.verticalCenter: totalText.verticalCenter
            anchors.topMargin: 10
            fillMode: Image.PreserveAspectFit
            source: appSettings.eyeIsOpen ? "../icons/eyes_open.svg" : "../icons/eyes_close.svg"
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    appSettings.eyeIsOpen = !appSettings.eyeIsOpen
                }
            }
        }

        Text {
            id: depositText
            anchors.top: totalText.bottom
            anchors.topMargin: 16
            anchors.left: totalText.left
            text: appSettings.eyeIsOpen ? qsTr("≈") + bankAccountInfo.amount : "******"
            font.pointSize: 20
            color: "#FFFFFF"
            verticalAlignment: Text.AlignVCenter
        }

        // Borrow
        Image {
            id: borrowImage
            anchors.left: depositText.left
            anchors.top: depositText.bottom
            anchors.topMargin: 16
            source: "../icons/borrow.svg"
            width: 10
            fillMode: Image.PreserveAspectFit
        }
        Text {
            id: borrowText
            text: qsTr("Borrow ($)\t\t")
            color: "#FFFFFF"
            font.pointSize: 12
            anchors.left: borrowImage.right
            anchors.leftMargin: 8
            anchors.verticalCenter: borrowImage.verticalCenter
            verticalAlignment: Text.AlignVCenter
        }
        Text {
            text: appSettings.eyeIsOpen ? qsTr("≈") + bankAccountInfo.borrow : "******"
            color: "#FFFFFF"
            font.pointSize: 12
            anchors.left: borrowText.right
            anchors.leftMargin: 8
            anchors.verticalCenter: borrowText.verticalCenter
            verticalAlignment: Text.AlignVCenter
        }

        // Total
        Image {
            id: incomeImage
            anchors.left: depositText.left
            anchors.top: borrowImage.bottom
            anchors.topMargin: 16
            source: "../icons/income.png"
            width: 10
            fillMode: Image.PreserveAspectFit
        }
        Text {
            id: incomeText
            text: qsTr("Total ($)\t\t")
            color: "#FFFFFF"
            font.pointSize: 12
            anchors.left: incomeImage.right
            anchors.leftMargin: 8
            anchors.verticalCenter: incomeImage.verticalCenter
            verticalAlignment: Text.AlignVCenter
        }
        Text {
            id: incomeDataText
            text: appSettings.eyeIsOpen ? qsTr("≈") + bankAccountInfo.total : "******"
            color: "#FFFFFF"
            font.pointSize: 12
            anchors.left: incomeText.right
            anchors.leftMargin: 8
            anchors.verticalCenter: incomeText.verticalCenter
            verticalAlignment: Text.AlignVCenter
        }

        // Yesterday
        Rectangle {
            id: yesBackgroundRec
            color: "#FB8F0B"
            width: yesRow.width + 16
            height: yesRow.height
            opacity: 0.1
            anchors.left: incomeDataText.right
            anchors.leftMargin: 50
            anchors.verticalCenter: incomeDataText.verticalCenter
        }
        Row {
            id: yesRow
            anchors.horizontalCenter: yesBackgroundRec.horizontalCenter
            anchors.verticalCenter: yesBackgroundRec.verticalCenter
            spacing: 8
            Image {
                id: lastdayincomeImage
                source: "../icons/lastdayincome.svg"
                width: 10
                fillMode: Image.PreserveAspectFit
                anchors.verticalCenter: lastdayincomeText.verticalCenter
            }
            Text {
                id: lastdayincomeText
                text: qsTr("Yesterday income ")
                color: "#FB8F0B"
                font.pointSize: 12
                verticalAlignment: Text.AlignVCenter
            }

            Text {
                text: (appSettings.eyeIsOpen ? bankAccountInfo.yesterday : "******") + qsTr(" $")
                color: "#FB8F0B"
                font.pointSize: 12
                verticalAlignment: Text.AlignVCenter
            }
        }

        // "..."
        ImageButton {
            anchors.right: parent.right
            anchors.rightMargin: 42
            anchors.top: parent.top
            anchors.topMargin: 32
            fillMode: Image.PreserveAspectFit
            source: "../icons/more.svg"
        }
    }

    Rectangle {
        id: whiteRec
        anchors.top: bankRec.bottom
        anchors.topMargin: -65
        anchors.bottom: parent.bottom
        anchors.left: bankRec.left
        anchors.right: bankRec.right
        border.color: "lightsteelblue"
        border.width: 1
        radius: 20

        Component.onCompleted: {
            Server.request('GET', '/1.0/violas/bank/product/deposit', null, function(resp) {
                    var entries = resp.data;
                    for (var i=0; i<entries.length; i++) {
                        depositModel.append(entries[i])
                    }
                });
            Server.request('GET', '/1.0/violas/bank/product/borrow', null, function(resp) {
                    var entries = resp.data;
                    for (var i=0; i<entries.length; i++) {
                        borrowModel.append(entries[i])
                    }
                });
        }

        ListModel {
            id: depositModel
        }

        ListModel {
            id: borrowModel
        }

        TabBar {
            id: tabBar
            anchors.top: parent.top
            anchors.topMargin: 34
            anchors.left: whiteRec.left
            anchors.leftMargin: 29
            width: 500

            TabButton {
                text: qsTr("Deposit Marker")
                width: depositBtnText.contentWidth + 16
                contentItem: Text {
                    id: depositBtnText
                    text: parent.text
                    color: tabBar.currentIndex == 0 ? "#333333" : "#999999"
                    font.pointSize: tabBar.currentIndex == 0 ? 16 : 12
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    color: "#FFFFFF"
                }
            }

            TabButton {
                text: qsTr("Borrow Marker")
                width: borrowBtnText.contentWidth + 16
                contentItem: Text {
                    id: borrowBtnText
                    text: parent.text
                    color: tabBar.currentIndex == 1 ? "#333333" : "#999999"
                    font.pointSize: tabBar.currentIndex == 1 ? 16 : 12
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    color: "#FFFFFF"
                }
            }
        }

        StackLayout {
            anchors.top: tabBar.bottom
            anchors.topMargin: 22
            anchors.left: parent.left
            anchors.leftMargin: 20
            anchors.right: parent.right
            anchors.rightMargin: 20
            anchors.bottom: parent.bottom
            currentIndex: tabBar.currentIndex

            ListView {
                id: depositProductView
                model: depositModel
                spacing: 12
                clip: true
                ScrollIndicator.vertical: ScrollIndicator { }
                delegate: Rectangle {
                    anchors.left: parent.left
                    anchors.right: parent.right
                    height: 60
                    color: "#EBEBF1"
                    radius: 14
                    MyImage {
                        id: itemImage
                        source: logo
                        radius: 14
                        width: 41
                        anchors.left: parent.left
                        anchors.leftMargin: 8
                        anchors.verticalCenter: parent.verticalCenter
                    }
                    Text {
                        id: nameText
                        text: name
                        anchors.left: itemImage.right
                        anchors.leftMargin: 15
                        anchors.verticalCenter: parent.verticalCenter
                        color: "#333333"
                        font.pointSize: 16
                    }
                    Text {
                        text: desc
                        anchors.left: nameText.right
                        anchors.leftMargin: 45
                        anchors.verticalCenter: parent.verticalCenter
                        color: "#999999"
                        font.pointSize: 12
                    }
                    Column {
                        anchors.right: parent.right
                        anchors.rightMargin: 15
                        anchors.verticalCenter: parent.verticalCenter
                        Text {
                            id: rateText
                            text: appSettings.eyeIsOpen ? rate: "******"
                            color: "#13B788"
                            font.pointSize: 18
                            anchors.right: parent.right
                        }
                        Text {
                            text: rate_desc
                            color: "#999999"
                            font.pointSize: 10
                            anchors.right: rateText.right
                        }
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            showDepositPage()
                        }
                    }
                }
            }

            ListView {
                id: borrowProductView
                model: borrowModel
                spacing: 12
                clip: true
                ScrollIndicator.vertical: ScrollIndicator { }
                delegate: Rectangle {
                    anchors.left: parent.left
                    anchors.right: parent.right
                    height: 60
                    color: "#EBEBF1"
                    radius: 14
                    MyImage {
                        id: itemImage
                        source: logo
                        radius: 14
                        width: 41
                        anchors.left: parent.left
                        anchors.leftMargin: 8
                        anchors.verticalCenter: parent.verticalCenter
                    }
                    Text {
                        id: nameText
                        text: name
                        anchors.left: itemImage.right
                        anchors.leftMargin: 15
                        anchors.verticalCenter: parent.verticalCenter
                        color: "#333333"
                        font.pointSize: 16
                    }
                    Text {
                        text: desc
                        anchors.left: nameText.right
                        anchors.leftMargin: 45
                        anchors.verticalCenter: parent.verticalCenter
                        color: "#999999"
                        font.pointSize: 12
                    }
                    Column {
                        anchors.right: parent.right
                        anchors.rightMargin: 15
                        anchors.verticalCenter: parent.verticalCenter
                        Text {
                            id: rateText
                            text: appSettings.eyeIsOpen ? rate: "******"
                            color: "#13B788"
                            font.pointSize: 18
                            anchors.right: parent.right
                        }
                        Text {
                            text: rate_desc
                            color: "#999999"
                            font.pointSize: 10
                            anchors.right: rateText.right
                        }
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            showBorrowPage()
                        }
                    }
                }
            }
        }
    }
}
