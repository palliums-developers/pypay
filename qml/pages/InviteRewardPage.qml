// 邀请奖励页面
import QtQuick 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.15

import "../controls"

ScrollView {
    id: root

    background: Rectangle {
        color: "#F7F7F9"
    }

    Item {
        id: topImage
        anchors.top: parent.top
        anchors.topMargin: 70
        anchors.left: parent.left
        anchors.leftMargin: 48
        anchors.right: parent.right
        anchors.rightMargin: 48
        height: 262
        Image {
            anchors.fill: parent
            source: "../icons/inviteReward.png"
            Image {
                id: planText
                anchors.left: parent.left
                anchors.leftMargin: 150
                anchors.top: parent.top
                anchors.topMargin: 52
                source: "../icons/rewardPlan.png"
            }
            Image {
                anchors.left: planText.left
                anchors.leftMargin: -20
                anchors.top: planText.bottom
                anchors.topMargin: 6
                source: "../icons/rewardText.png"
            }
        }
    }

    Rectangle {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: topImage.bottom
        anchors.topMargin: -80
        width: topImage.width - 100
        height: 130
        radius: 20
        color: "#FFFFFF"
        RowLayout {
            anchors.fill: parent
            Column {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                spacing: 4
                Image {
                    id: image1
                    source: "../icons/sendLink.png"
                }
                Text {
                    text: qsTr("发送邀请链接给好友")
                    anchors.horizontalCenter: image1.horizontalCenter
                }
            }
            Image {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                source: "../icons/rewardArrow.svg"
                Layout.preferredWidth: 32
                fillMode: Image.PreserveAspectFit
            }
            Column {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                spacing: 4
                Image {
                    id: image2
                    source: "../icons/sendLink.png"
                }
                Text {
                    text: qsTr("好友通过手机号验证")
                    anchors.horizontalCenter: image2.horizontalCenter
                }
            }
            Image {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                source: "../icons/rewardArrow.svg"
                Layout.preferredWidth: 32
                fillMode: Image.PreserveAspectFit
            }
            Column {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                spacing: 4
                Image {
                    id: image3
                    source: "../icons/sendLink.png"
                }
                Text {
                    text: qsTr("对方获得相应奖励")
                    anchors.horizontalCenter: image3.horizontalCenter
                }
            }
        }
    }
}
