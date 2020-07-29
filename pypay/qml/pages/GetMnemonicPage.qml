import QtQuick 2.14
import QtQuick.Controls 2.5
import "../controls"

Page {
    id: root
    signal backArrowClicked
    signal backupClicked
    signal laterBackupClicked

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
        text: qsTr("获取助记词")
        font.pointSize: 20
        color: "#3B3847"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 197.0 / 952 * parent.height
    }
    Text {
        id: title2Text
        text: qsTr("等于拥有钱包资产所有权")
        font.pointSize: 16
        color: "#3B3847"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: titleText.bottom
        anchors.topMargin: 3
    }

    Image {
        source: "../icons/mne_image.svg"
        fillMode: Image.PreserveAspectFit
        width: 140
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: title2Text.bottom
        anchors.topMargin: 30
    }

    // 小圆圈
    Rectangle {
        width: 4
        height: 4
        radius: 2
        color: "#3B3847"
        anchors.verticalCenter: backupText.verticalCenter
        anchors.right: backupText.left
        anchors.rightMargin: 5
    }
    Text {
        id: backupText
        anchors.left: offlineStoreTextDetail.left
        anchors.top: parent.top
        anchors.topMargin: 436.0 / 952 * parent.height
        text: qsTr("备份助记词")
        font.pointSize: 16
        color: "#3B3847"
    }

    Text {
        anchors.left: offlineStoreTextDetail.left
        anchors.top: backupText.bottom
        anchors.topMargin: 8
        font.pointSize: 12
        color: "#3B3847"
        text: qsTr("使用纸和笔正确抄写助记词，如果你的手机丢失、被盗、损坏，Keystore将可以回复你的资产")
    }

    // 小圆圈
    Rectangle {
        width: 4
        height: 4
        radius: 2
        color: "#3B3847"
        anchors.verticalCenter: offlineStoreText.verticalCenter
        anchors.right: offlineStoreText.left
        anchors.rightMargin: 5
    }
    Text {
        id: offlineStoreText
        anchors.left: offlineStoreTextDetail.left
        anchors.top: parent.top
        anchors.topMargin: 513.0 / 952 * parent.height
        text: qsTr("离线保管")
        font.pointSize: 16
        color: "#3B3847"
    }

    // 这个的文字最长，其他文字以它为基准对齐
    Text {
        id: offlineStoreTextDetail
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: offlineStoreText.bottom
        anchors.topMargin: 8
        font.pointSize: 12
        color: "#3B3847"
        text: qsTr("请妥善保管至隔离网络的安全地方，请勿将助记词在联网环境下分享和存储，比如邮件、相册、社交应用等")
    }

    // 按钮
    MyButton3 {
        id: backupBtn
        anchors.top: parent.top
        anchors.topMargin: 614.0 / 952 * parent.height
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
