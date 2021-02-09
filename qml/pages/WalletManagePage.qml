import QtQuick 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.15

import "../controls"

Page {
    id: root
    signal backArrowClicked
    property bool isShowMne: false

    ImageButton {
        anchors.top: parent.top
        anchors.topMargin: 98
        anchors.left: parent.left
        anchors.leftMargin: 92
        width: 32
        source: "../icons/backarrow2.svg"
        MouseArea {
            anchors.fill: parent
            onClicked: {
                backArrowClicked()
            }
        }
    }

    Text {
        id: titleText
        text: qsTr("钱包管理")
        font.pointSize: 20
        color: "#3B3847"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 197.0 / 952 * parent.height
    }

    Row {
        id: mneRow
        spacing: 8
        anchors.top: titleText.bottom
        anchors.topMargin: 50
        anchors.left: parent.left
        anchors.leftMargin: 100
        Text {
            text: qsTr("助记词管理:\t") 
        }
        Text {
            id: tMneText
            text: root.isShowMne ? qsTr("隐藏助记词 ") : qsTr("显示助记词 ")
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    root.isShowMne = !root.isShowMne
                }
            }
        }
        Text {
            id: mneText
            text: root.isShowMne ? server.mnemonic : "******"
            anchors.verticalCenter: tMneText.verticalCenter
        }
        ImageButton {
            id: copyBtn
            visible: root.isShowMne
            source: "../icons/copy.svg"
            width: 10
            height: 12
            anchors.verticalCenter: tMneText.verticalCenter
            MouseArea {
                anchors.fill: parent
                onClicked: server.copy_text(mneText.text)
            }
        }
    }

    Row {
        spacing: 8
        anchors.top: mneRow.bottom
        anchors.topMargin: 50
        anchors.left: mneRow.left
        Text {
            text: qsTr("地址管理:\t") 
        }
    }

    MyButton3 {
        id: delBtn
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 100
        text: qsTr("删除钱包")
        width: 200
        height: 40
        onClicked: {
            server.delete_wallet()
            appWindow.close()
        }
    }
}
