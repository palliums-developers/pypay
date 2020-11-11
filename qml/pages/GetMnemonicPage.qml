import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"

Page {
    id: root
    signal backArrowClicked
    signal backupClicked
    signal laterBackupClicked

    ImageButton {
        anchors.top: parent.top
        anchors.topMargin: 24
        anchors.left: parent.left
        anchors.leftMargin: 24
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
        text: qsTr("获取助记词")
        font.pointSize: 20
        color: "#3B3847"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 48
    }
    Text {
        id: title2Text
        text: qsTr("等于拥有钱包资产所有权")
        font.pointSize: 16
        color: "#3B3847"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: titleText.bottom
        anchors.topMargin: 4
    }

    Image {
        id: mneImage
        source: "../icons/mne_image.svg"
        fillMode: Image.PreserveAspectFit
        width: 140
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: title2Text.bottom
        anchors.topMargin: 32 / 952 * parent.height
    }

    Item {
        id: textItem
        anchors.horizontalCenter: parent.horizontalCenter
        width: 0.65 * parent.width
        height: backupText.height + backupDetailText.height + offlineStoreText.height + offlineStoreDetailText.height + 3 * 4
        anchors.top: mneImage.bottom    
        anchors.topMargin: 32 / 952 * parent.height
        
        // 小圆圈
        Rectangle {
            id: backupRec
            width: 4
            height: 4
            radius: 2
            color: "#3B3847"
            anchors.left: parent.left
            anchors.top: parent.top
        }
        Text {
            id: backupText
            anchors.left: backupRec.left
            anchors.leftMargin: 4
            anchors.verticalCenter: backupRec.verticalCenter
            text: qsTr("备份助记词")
            font.pointSize: 12
            color: "#3B3847"
        }

        Text {
            id: backupDetailText
            anchors.left: backupText.left
            anchors.top: backupText.bottom
            anchors.topMargin: 4
            font.pointSize: 12
            color: "#3B3847"
            text: qsTr("使用纸和笔正确抄写助记词，如果你的手机丢失、被盗、损坏，Keystore将可以回复你的资产")
            width: parent.width - backupRec.width - 4 - backupRec.width
            elide: Text.ElideRight
        }

        // 小圆圈
        Rectangle {
            id: offlineRec
            width: 4
            height: 4
            radius: 2
            color: "#3B3847"
            anchors.left: backupRec.left
            anchors.top: backupDetailText.bottom
            anchors.topMargin: 4
        }
        Text {
            id: offlineStoreText
            anchors.left: offlineRec.left
            anchors.leftMargin: 4
            anchors.verticalCenter: offlineRec.verticalCenter
            text: qsTr("离线保管")
            font.pointSize: 12
            color: "#3B3847"
        }

        Text {
            id: offlineStoreDetailText
            anchors.left: offlineStoreText.left
            anchors.top: offlineStoreText.bottom
            anchors.topMargin: 4
            font.pointSize: 12
            color: "#3B3847"
            text: qsTr("请妥善保管至隔离网络的安全地方，请勿将助记词在联网环境下分享和存储，比如邮件、相册、社交应用等")
            width: parent.width - offlineRec.width - 4 - offlineRec.width
            elide: Text.ElideRight
        }
    }

    // 按钮
    MyButton3 {
        id: backupBtn
        anchors.top: textItem.bottom
        anchors.topMargin: 56 / 952 * parent.height
        anchors.horizontalCenter: parent.horizontalCenter
        text: qsTr("开始备份")
        width: 200
        height: 40
        onClicked: {
            root.backupClicked()
        }
    }

    MyButton3 {
        id: laterBackupBtn
        anchors.top: backupBtn.bottom
        anchors.topMargin: 8
        anchors.horizontalCenter: parent.horizontalCenter
        text: qsTr("稍后备份")
        width: 200
        height: 40
        onClicked: {
            root.laterBackupClicked()
        }
    }
}
