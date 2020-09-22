import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

import "../controls"

import PyPay 1.0

Control {
    padding: 40

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
            text: qsTr("交易详情")
            color: "#333333"
            font.pointSize: 16
            font.weight: Font.Medium
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            id: txidText
            anchors.top: titleText.bottom
            anchors.topMargin: 200
            anchors.horizontalCenter: parent.horizontalCenter
            text: payController.currentBitTransactionEntry.txid
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    payController.copy(txidText.text)
                }
            }
        }

        Text {
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 16
            anchors.horizontalCenter: parent.horizontalCenter
            text: qsTr("浏览器查询更详细信息")
            font.pointSize: 14
            color: "#7038FD"
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    payController.openUrl("https://testnet.violas.io/app/tBTC")
                }
            }
        }
    }
}
