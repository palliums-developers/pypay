// 邀请奖励页面
import QtQuick 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.15

import "../controls"

ScrollView {
    id: root

    signal backArrowClicked

    ImageButton {
        anchors.top: parent.top
        anchors.topMargin: 20
        anchors.left: parent.left
        anchors.leftMargin: 20
        width: 32
        source: "../icons/backarrow2.svg"
        MouseArea {
            anchors.fill: parent
            onClicked: {
                backArrowClicked()
            }
        }
    }

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
        id: inviRec
        anchors.left: topImage.left
        anchors.right: topImage.right   
        anchors.top: topImage.bottom
        anchors.topMargin: 10
        height: 200
        radius: 5
        Text {
            id: myInvText
            anchors.top: parent.top
            anchors.topMargin: 58
            anchors.left: parent.left
            anchors.leftMargin: 40
            text: qsTr("我的邀请")
        }
        Row {
            anchors.right: parent.right
            anchors.rightMargin: 40
            anchors.verticalCenter: myInvText.verticalCenter
            spacing: 5
            Text {
                text: qsTr("查看更多")
            }
            Image {
                source: "../icons/mine_right_arrow.svg"
            }
        }
        Rectangle {
            id: hLine
            anchors.left: parent.left
            anchors.leftMargin: 40
            anchors.right: parent.right
            anchors.rightMargin: 40
            anchors.top: myInvText.bottom
            anchors.topMargin: 10
            height: 1
            color: "#DEDEDE"
        }

        Rectangle {
            anchors.top: hLine.bottom
            anchors.topMargin: 5
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 5
            anchors.horizontalCenter: parent.horizontalCenter
            width: 1
            color: "#DEDEDE"
        }
        Text {
            id: invNumText
            anchors.left: parent.left
            anchors.leftMargin: 250
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 40
            text: qsTr("邀请人数: ")
        }
        Text {
            anchors.verticalCenter: invNumText.verticalCenter
            anchors.right: parent.right
            anchors.rightMargin: 250
            text: qsTr("邀请奖励: ")
        }
    }

    Rectangle {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: topImage.bottom
        anchors.topMargin: -80
        width: topImage.width - 100
        height: 130
        radius: 20
        border.color: "#F7F7F9"
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

    Rectangle {
        id: chartRec
        anchors.left: inviRec.left
        anchors.right: inviRec.right   
        anchors.top: inviRec.bottom
        anchors.topMargin: 10
        height: 200
        radius: 5
        Text {
            id: chartText
            anchors.top: parent.top
            anchors.topMargin: 22
            anchors.left: parent.left
            anchors.leftMargin: 40
            text: qsTr("排行榜")
        }
        Row {
            anchors.right: parent.right
            anchors.rightMargin: 40
            anchors.verticalCenter: chartText.verticalCenter
            spacing: 5
            Text {
                text: qsTr("查看更多")
            }
            Image {
                source: "../icons/mine_right_arrow.svg"
            }
        }
        Rectangle {
            id: hLine2
            anchors.left: parent.left
            anchors.leftMargin: 40
            anchors.right: parent.right
            anchors.rightMargin: 40
            anchors.top: chartText.bottom
            anchors.topMargin: 10
            height: 1
            color: "#DEDEDE"
        }
    }
    
}
