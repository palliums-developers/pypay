import QtQuick 2.14
import QtQuick.Controls 2.5
import "../controls"

Page {
    id: root
    signal enterClicked

    function execCommand() {
        if (appSettings.password != passwordText.text) {
            tipText.text = qsTr("密码不正确")
            tipText.visible = true
            tipTimer.running = true
        } else {
            root.enterClicked()
            appWindow.userIsLogin = true
        }
    }

    Text {
        id: titleText
        text: qsTr("进入钱包前，请输入你的密码")
        font.pointSize: 20
        color: "#3C3848"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 203.0 / 952 * parent.height
    }

    TextFieldEye {
        id: passwordText
        anchors.top: parent.top
        anchors.topMargin: 278.0 / 952 * parent.height
        anchors.horizontalCenter: parent.horizontalCenter
        width: 642.0 / 1160 * parent.width
        height: 50.0 / 952 * parent.height
        placeholderText: qsTr("8-20位，大小写字母，数字")
        imageSource: eyeIsClose ? "../icons/eye_close.svg" : "../icons/eye_open.svg"
        onReturnKeyPressed: {
            execCommand()
        }
    }

    MyButton3 {
        id: enterBtn
        anchors.top: passwordText.bottom
        anchors.topMargin: 160
        anchors.horizontalCenter: parent.horizontalCenter
        text: qsTr("进入")
        width: 200
        height: 40
        onClicked: {
            execCommand()
        }
    }

    Text {
        id: exitBtn
        text: qsTr("退出钱包")
        color: "#F74E4E"
        font.pointSize: 14
        anchors.top: enterBtn.bottom
        anchors.topMargin: 56
        anchors.horizontalCenter: parent.horizontalCenter
        MouseArea {
            anchors.fill: parent
            onClicked: {
                appWindow.close()
            }
        }
    }

    Text {
        id: tipText
        anchors.right: passwordText.right
        anchors.top: passwordText.bottom
        anchors.topMargin: 5
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
