import QtQuick 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.15

import "../controls"

Page {
    id: root
    signal backArrowClicked
    signal createClicked
    property bool isSelected: false

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
        text: qsTr("创建")
        font.pointSize: 20
        color: "#3C3848"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 48
    }

    TextFieldEye {
        id: passwordText
        anchors.top: titleText.bottom
        anchors.topMargin: 56 / 952 * parent.height
        anchors.horizontalCenter: parent.horizontalCenter
        width: 0.65 * parent.width
        placeholderText: qsTr("8-20位，大小写字母，数字")
        imageSource: eyeIsClose ? "../icons/eye_close.svg" : "../icons/eye_open.svg"
    }

    TextFieldEye {
        id: confirmText
        anchors.top: passwordText.bottom
        anchors.topMargin: 8
        anchors.horizontalCenter: parent.horizontalCenter
        width: 0.65 * parent.width
        placeholderText: qsTr("重复输入密码")
        imageSource: eyeIsClose ? "../icons/eye_close.svg" : "../icons/eye_open.svg"
    }

    MyButton3 {
        id: createBtn
        anchors.top: confirmText.bottom
        anchors.topMargin: 160 / 952 * parent.height
        anchors.horizontalCenter: parent.horizontalCenter
        text: qsTr("创建")
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
            //} else if (root.isSelected == false) {
            //    tipText.text = qsTr("请勾选服务与隐私政策")
            //    tipText.visible = true
            //    tipTimer.running = true
            //    } else {
                appSettings.password = passwordText.text    // TODO
                root.createClicked()
                server.create_wallet()
                appSettings.walletIsCreate = true
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

    Row {
        anchors.top: tipText.bottom
        anchors.topMargin: 24
        anchors.horizontalCenter: parent.horizontalCenter
        spacing: 5
        Image {
            anchors.verticalCenter: checkText.verticalCenter
            width: 14
            height: 14
            source: root.isSelected ? "../icons/xuanze-2.svg" : "../icons/xuanze.svg"
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    root.isSelected = !root.isSelected
                }
            }
        }
        Text {
            id: checkText
            text: qsTr("我已阅读并同意<b>《服务与隐私政策》</b>")
            color: "#999999"
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    server.open_url("https://violas.io")
                }
            }
        }
    }
}
