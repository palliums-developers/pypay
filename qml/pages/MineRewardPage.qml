import QtQuick 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.15

import "../controls"

Page {
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

    Rectangle {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.topMargin: 50
        anchors.bottom: parent.bottom
        color: "#501BA2"

        Flickable {
            width: parent.width
            height: parent.height
            ScrollIndicator.vertical: ScrollIndicator { }
            contentWidth: width
            contentHeight: contentColumn.height
            Column {
                id: contentColumn
                anchors.left: parent.left
                anchors.leftMargin: 42
                anchors.right: parent.right
                anchors.rightMargin: 42
                anchors.top: parent.top
                anchors.topMargin: 60
                anchors.bottom: parent.bottom
                spacing: 12
                Image {
                    source: "../icons/mine_background.svg"
                    width: parent.width
                    height: 250
                    Text {
                        id: totalText
                        text: qsTr("总收益:  0VLS")
                        anchors.top: parent.top
                        anchors.topMargin: 44
                        anchors.left: parent.left
                        anchors.leftMargin: 40
                        color: "#FFFFFF"
                        font.pointSize: 14
                    }
                    Image {
                        id: ruleImage
                        anchors.verticalCenter: totalText.verticalCenter
                        anchors.right: parent.right
                        anchors.rightMargin: 40
                        source: "../icons/rule_rec.svg"
                        Row {
                            spacing: 5
                            anchors.centerIn: parent
                            Text {
                                text: qsTr("规则说明")
                                color: "#FFFFFF"
                            }
                            Image {
                                source: "../icons/mine_arrow.svg"
                            }
                        }
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                console.log("aaaaaaaaa")
                            }
                        }
                    }

                    Image {
                        id: detailImage
                        anchors.left: totalText.left
                        anchors.top: totalText.bottom
                        anchors.topMargin: 24
                        source: "../icons/rule_rec.svg"
                        Row {
                            spacing: 5
                            anchors.centerIn: parent
                            Text {
                                text: qsTr("挖矿明细")
                                color: "#FFFFFF"
                            }
                            Image {
                                source: "../icons/mine_arrow.svg"
                            }
                        }
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                console.log("aaaaaaaaa")
                            }
                        }
                    }

                    Image {
                        id: picImage
                        anchors.top: ruleImage.bottom
                        anchors.right: ruleImage.right
                        source: "../icons/mine_pic.png"
                    }

                    Text {
                        id: poolText
                        anchors.left: totalText.left
                        anchors.top: detailImage.bottom
                        anchors.topMargin: 50
                        text: qsTr("资金池挖矿已提取：0VLS")
                        color: "#FFFFFF"
                    }

                    Text {
                        id: poolWaitText
                        anchors.left: totalText.left
                        anchors.top: poolText.bottom
                        anchors.topMargin: 16
                        text: qsTr("待提取(VLS): 0")
                        color: "#FFFFFF"
                    }

                    Image {
                        source: "../icons/mine_wait.svg"
                        anchors.left: poolWaitText.right
                        anchors.leftMargin: 10
                        anchors.verticalCenter: poolWaitText.verticalCenter
                        Text {
                            anchors.centerIn: parent
                            text: qsTr("一键提取")
                        }
                    }

                    
                    Text {
                        id: bankText
                        anchors.verticalCenter: poolText.verticalCenter
                        anchors.left: bankWaitText.left
                        text: qsTr("数字银行挖矿已提取：0VLS")
                        color: "#FFFFFF"
                    }

                    Text {
                        id: bankWaitText
                        anchors.verticalCenter: poolWaitText.verticalCenter
                        anchors.right: bankWaitImage.left
                        anchors.rightMargin: 20
                        text: qsTr("待提取(VLS): 0")
                        color: "#FFFFFF"
                    }

                    Image {
                        id: bankWaitImage
                        source: "../icons/mine_wait.svg"
                        anchors.right: picImage.left
                        anchors.rightMargin: 10
                        anchors.verticalCenter: poolWaitText.verticalCenter
                        Text {
                            anchors.centerIn: parent
                            text: qsTr("一键提取")
                        }
                    }
                    
                }

                Rectangle {
                    width: parent.width
                    height: 200
                    color: "#FFFFFF"
                    Text {
                        id: moreText
                        anchors.top: parent.top
                        anchors.topMargin: 22
                        anchors.left: parent.left
                        anchors.leftMargin: 40
                        text: qsTr("获取更多VLS")
                    }
                    Rectangle {
                        id: hLine
                        anchors.left: parent.left
                        anchors.leftMargin: 40
                        anchors.right: parent.right
                        anchors.rightMargin: 40
                        anchors.top: moreText.bottom
                        anchors.topMargin: 10
                        height: 1
                        color: "#DEDEDE"
                    }
                    Rectangle {
                        id: vLine
                        anchors.top: hLine.bottom
                        anchors.bottom: parent.bottom
                        anchors.horizontalCenter: parent.horizontalCenter
                        width: 1
                        color: "#DEDEDE"
                    }

                    Text {
                        id: newUserText
                        anchors.left: hLine.left
                        anchors.top: hLine.bottom
                        anchors.topMargin: 20
                        text: qsTr("新用户验证") 
                    }
                    Rectangle {
                        anchors.verticalCenter: newUserText.verticalCenter
                        anchors.right: vLine.left
                        anchors.rightMargin: 50
                        color: "#7038FD"
                        width: 100
                        height: 30
                        radius: 15
                        Text {
                            anchors.centerIn: parent
                            text: qsTr("去验证")
                            color: "#FFFFFF"
                        }
                    }

                    Text {
                        id: depositText
                        anchors.left: hLine.left
                        anchors.top: newUserText.bottom
                        anchors.topMargin: 30
                        text: qsTr("存款挖矿") 
                    }
                    Rectangle {
                        anchors.verticalCenter: depositText.verticalCenter
                        anchors.right: vLine.left
                        anchors.rightMargin: 50
                        color: "#7038FD"
                        width: 100
                        height: 30
                        radius: 15
                        Text {
                            anchors.centerIn: parent
                            text: qsTr("去验证")
                            color: "#FFFFFF"
                        }
                    }

                    Text {
                        id: poolText2
                        anchors.left: hLine.left
                        anchors.top: depositText.bottom
                        anchors.topMargin: 30
                        text: qsTr("资金池挖矿") 
                    }
                    Rectangle {
                        anchors.verticalCenter: poolText2.verticalCenter
                        anchors.right: vLine.left
                        anchors.rightMargin: 50
                        color: "#7038FD"
                        width: 100
                        height: 30
                        radius: 15
                        Text {
                            anchors.centerIn: parent
                            text: qsTr("去验证")
                            color: "#FFFFFF"
                        }
                    }

                    Text {
                        id: inviteText
                        anchors.left: vLine.right
                        anchors.leftMargin: 50
                        anchors.verticalCenter: newUserText.verticalCenter
                        text: qsTr("邀请好友") 
                    }
                    Rectangle {
                        anchors.verticalCenter: newUserText.verticalCenter
                        anchors.right: hLine.right
                        anchors.rightMargin: 50
                        color: "#7038FD"
                        width: 100
                        height: 30
                        radius: 15
                        Text {
                            anchors.centerIn: parent
                            text: qsTr("去验证")
                            color: "#FFFFFF"
                        }
                    }
                    Text {
                        anchors.left: vLine.right
                        anchors.leftMargin: 50
                        anchors.verticalCenter: depositText.verticalCenter
                        text: qsTr("借款挖矿") 
                    }
                    Rectangle {
                        anchors.verticalCenter: depositText.verticalCenter
                        anchors.right: hLine.right
                        anchors.rightMargin: 50
                        color: "#7038FD"
                        width: 100
                        height: 30
                        radius: 15
                        Text {
                            anchors.centerIn: parent
                            text: qsTr("去验证")
                            color: "#FFFFFF"
                        }
                    }
                }

                Rectangle {
                    width: parent.width
                    height: 300
                    color: "#FFFFFF"
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
        }
    }
}
