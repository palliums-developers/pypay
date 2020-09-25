import QtQuick 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.15

import "../controls"
import "../models/ViolasServer.js" as Server

import PyPay 1.0

Page {
    id: root
    signal backArrowClicked

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
        text: qsTr("Bank> <b><b>Deposit Order</b></b>")
        font.pointSize: 14
        color: "#5C5C5C"
        anchors.verticalCenter: backBtn.verticalCenter
        anchors.left: backBtn.right
        anchors.leftMargin: 8
    }

    Rectangle {
        anchors.left: parent.left
        anchors.leftMargin: 50
        anchors.right: parent.right
        anchors.rightMargin: 50
        anchors.top: backBtn.bottom
        anchors.topMargin: 24
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 24
        color: "#FFFFFF"
        
        TabBar {
            id: tabBar
            anchors.top: parent.top
            anchors.topMargin: 40
            anchors.left: parent.left
            anchors.leftMargin: 54
            width: 500

            TabButton {
                text: qsTr("Current Deposit")
                width: depositBtnText.contentWidth + 50
                leftPadding: 0
                contentItem: Text {
                    id: depositBtnText
                    text: parent.text
                    color: tabBar.currentIndex == 0 ? "#333333" : "#999999"
                    font.pointSize: tabBar.currentIndex == 0 ? 16 : 12
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    color: "#FFFFFF"
                }
            }

            TabButton {
                text: qsTr("Deposit Detail")
                width: depositDetailText.contentWidth + 50
                leftPadding: 0
                contentItem: Text {
                    id: depositDetailText
                    text: parent.text
                    color: tabBar.currentIndex == 1 ? "#333333" : "#999999"
                    font.pointSize: tabBar.currentIndex == 1 ? 16 : 12
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    color: "#FFFFFF"
                }
            }
        }

        StackLayout {
            anchors.top: tabBar.bottom
            anchors.topMargin: 55
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            currentIndex: tabBar.currentIndex

            ListView {
                id: currentDepositView
                model: currentDepositModel
                spacing: 12
                clip: true
                ScrollIndicator.vertical: ScrollIndicator { }
                header: Rectangle {
                    width: parent.width
                    height: 50
                    Text {
                        id: tokenText
                        anchors.left: parent.left
                        anchors.leftMargin: 54
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Token")
                    }
                    Text {
                        id: principalText
                        anchors.left: tokenText.left
                        anchors.leftMargin: 100 / (1070 - 54*2) * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Principal")
                    }
                    Text {
                        id: incomeText
                        anchors.left: principalText.left
                        anchors.leftMargin: 206 / (1070 - 54*2) * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Income")
                    }
                    Text {
                        id: rateText
                        anchors.left: incomeText.left
                        anchors.leftMargin: 192 / (1070 - 54*2) * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Rate")
                    }
                    Text {
                        id: statusText
                        anchors.left: rateText.left
                        anchors.leftMargin: 150 / (1070 - 54*2) * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Status")
                    }
                    Text {
                        id: operationText
                        anchors.right: parent.right
                        anchors.rightMargin: 54
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Operation")
                    }
                    Rectangle {
                        anchors.left: parent.left
                        anchors.leftMargin: 27
                        anchors.right: parent.right
                        anchors.rightMargin: 27
                        anchors.bottom: parent.bottom
                        height: 1
                        color: "#DEDEDE"
                        opacity: 0.5
                    }
                }
                headerPositioning: ListView.OverlayHeader
                delegate: Rectangle {
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                        }
                    }
                }
            }

            ListView {
                id: borrowDetailView
                model: borrowDetailModel
                spacing: 12
                clip: true
                ScrollIndicator.vertical: ScrollIndicator { }
                delegate: Rectangle {
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                        }
                    }
                }
            }
        }
    }
}
