import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"

Page {
    id: root
    signal backArrowClicked
    signal importClicked

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
        text: qsTr("导入")
        font.pointSize: 20
        color: "#3C3848"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 203.0 / 952 * parent.height
    }

    TextArea {
        id: textArea
        anchors.top: parent.top
        anchors.topMargin: 294.0 / 952 * parent.height
        anchors.horizontalCenter: parent.horizontalCenter
        placeholderText: qsTr("输入助记单词，并用空格分隔")
        width: 642.0 / 1160 * parent.width
        height: 110.0 / 952 * parent.height
        wrapMode: TextEdit.Wrap
        selectByMouse: true
        background: Rectangle {
            implicitWidth: 642.0 / 1160 * parent.width
            implicitHeight: 110.0 / 952 * parent.height
            border.color: textArea.activeFocus ? "#FD6565" : "#979797"
        }
    }

    TextFieldEye {
        id: passwordText
        anchors.top: parent.top
        anchors.topMargin: 424.0 / 952 * parent.height
        anchors.horizontalCenter: parent.horizontalCenter
        width: 642.0 / 1160 * parent.width
        height: 50.0 / 952 * parent.height
        placeholderText: qsTr("8-20位，大小写字母，数字")
        imageSource: eyeIsClose ? "../icons/eye_close.svg" : "../icons/eye_open.svg"
    }

    TextFieldEye {
        id: confirmText
        anchors.top: passwordText.bottom
        anchors.topMargin: 20
        anchors.horizontalCenter: parent.horizontalCenter
        width: 642.0 / 1160 * parent.width
        height: 50.0 / 952 * parent.height
        placeholderText: qsTr("重复输入密码")
        imageSource: eyeIsClose ? "../icons/eye_close.svg" : "../icons/eye_open.svg"
    }

    MyButton3 {
        id: createBtn
        anchors.top: confirmText.bottom
        anchors.topMargin: 160
        anchors.horizontalCenter: parent.horizontalCenter
        text: qsTr("开始导入")
        width: 200
        height: 40
        onClicked: {
            //if (passwordText.text != confirmText.text) {
            //    console.log(passwordText.text, confirmText.text)
            //    tipText.text = qsTr("两次密码输入不一致")
            //    tipText.visible = true
            //    tipTimer.running = true
            //} else if (passwordText.text.length < 8) {
            //    tipText.text = qsTr("密码长度应为8~20位")
            //    tipText.visible = true
            //    tipTimer.running = true
            //} else {
                appSettings.password = passwordText.text    // TODO
                root.importClicked()
                server.create_wallet_from_mnemonic(textArea.text)
                appSettings.walletIsCreate = true
                appSettings.mnemonicIsBackup = true
            //}
        }
    }

    Text {
        id: tipText
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: createBtn.bottom
        anchors.topMargin: 3
        visible: false
        font.pointSize: 14
        color: "#FD6565"
    }

    Timer {
        id: tipTimer
        interval: 3000
        onTriggered: tipText.visible = false
    }
}
