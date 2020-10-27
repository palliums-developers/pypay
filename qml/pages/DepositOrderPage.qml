import QtQuick 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.15

import "../controls"
import "../pages"

import PyPay 1.0

PyPayPage {
    id: root
    isShowHeader: true
    title: qsTr("Bank > <b>Deposit Orders</b>")

    Component.onCompleted: {
        startBusy()
        var params = { "address": payController.addr, "offset": 0, "limit": 10 }
        server.getViolasBankDepositOrders(params, function() {
            var count =  server.currentDepositModel.count == 0 ? 0 : server.currentDepositModel.get(0).total_count
            var numOfPerPage = currentDepositSwitchPage.numOfPerPage
            for (var i = 0; i <  count / numOfPerPage; i++) {
                currentDepositSwitchPage.listModel.append({index: i})
            }
            stopBusy()
        })
    }

    Rectangle {
        anchors.left: parent.left
        anchors.leftMargin: 50
        anchors.right: parent.right
        anchors.rightMargin: 50
        anchors.top: parent.top
        anchors.topMargin: 140
        anchors.bottom: parent.bottom
        color: "#FFFFFF"
        
        TabBar {
            id: tabBar
            anchors.top: parent.top
            anchors.topMargin: 40
            anchors.left: parent.left
            anchors.leftMargin: 54
            width: 500

            TabButton {
                text: qsTr("Current Deposit")
                width: 200
                leftPadding: 0
                contentItem: Text {
                        text: parent.text
                        color: tabBar.currentIndex == 0 ? "#333333" : "#999999"
                        font.pointSize: tabBar.currentIndex == 0 ? 16 : 12
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    color: "#FFFFFF"
                }
            }

            TabButton {
                text: qsTr("Deposit Detail")
                width: 200
                leftPadding: 0
                contentItem: Text {
                    text: parent.text
                    color: tabBar.currentIndex == 1 ? "#333333" : "#999999"
                    font.pointSize: tabBar.currentIndex == 1 ? 16 : 12
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    color: "#FFFFFF"
                }
                onToggled: {
                    if (server.depositDetailModel.count == 0) {
                        startBusy()
                        var params = { "address": payController.addr, "offset": 0, "limit": 10 }
                        server.getViolasBankDepositOrderList(params, function() {
                            var count =  server.depositDetailModel.count == 0 ? 0 : server.depositDetailModel.get(0).total_count
                            var numOfPerPage = depositDetailSwitchPage.numOfPerPage
                            for (var i = 0; i <  count / numOfPerPage; i++) {
                                depositDetailSwitchPage.listModel.append({index: i})
                            }
                            stopBusy()
                        })
                    }
                }
            }
        }
        Rectangle {
            anchors.left: tabBar.left
            anchors.leftMargin: tabBar.currentIndex == 0 ? 0 : 200
            anchors.top: tabBar.bottom
            anchors.topMargin: 8
            width: 40
            height: 3
            color: "blue"
        }

        StackLayout {
            id: stackView
            anchors.top: tabBar.bottom
            anchors.topMargin: 32
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 80
            currentIndex: tabBar.currentIndex

            ListView {
                id: currentDepositView
                model: server.currentDepositModel
                spacing: 12
                clip: true
                ScrollIndicator.vertical: ScrollIndicator { }
                header: Rectangle {
                    z: 2
                    width: parent.width
                    height: 50
                    RowLayout {
                        anchors.fill: parent
                        Item {
                            Layout.leftMargin: 54
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 6 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumWidth: 300
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: qsTr("Token")
                            }
                        }
                        Item {
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 6 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumWidth: 300
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: qsTr("Principal")
                            }
                        }
                        Item {
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 6 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumWidth: 300
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: qsTr("Income")
                            }
                        }
                        Item {
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 6 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumWidth: 300
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: qsTr("Rate")
                            }
                        }
                        Item {
                            Layout.fillWidth: true
                            Layout.preferredHeight: parent.height
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: qsTr("Status")
                            }
                        }
                        Item {
                            Layout.rightMargin: 54
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 6 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumWidth: 300
                            Text {
                                anchors.right: parent.right
                                anchors.verticalCenter: parent.verticalCenter
                                text: qsTr("Operation")
                            }
                        }
                    }
                    Rectangle {
                        anchors.left: parent.left
                        anchors.leftMargin: 27
                        anchors.right: parent.right
                        anchors.rightMargin: 27
                        anchors.bottom: parent.bottom
                        height: 1
                        color: "#DEDEDE"
                        opacity: 0.5
                    }
                }
                headerPositioning: ListView.OverlayHeader
                delegate: Rectangle {
                    width: currentDepositView.width
                    height: 50
                    RowLayout {
                        anchors.fill: parent
                        Item {
                            Layout.leftMargin: 54
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 6 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumWidth: 300
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: currency
                            }
                        }
                        Item {
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 6 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumWidth: 300
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: principal.toFixed(2)
                            }
                        }
                        Item {
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 6 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumWidth: 300
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: earnings.toFixed(2)
                            }
                        }
                        Item {
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 6 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumWidth: 300
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: rate * 100 + "%"
                                color: "#13B788"
                            }
                        }
                        Item {
                            Layout.fillWidth: true
                            Layout.preferredHeight: parent.height
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: {
                                    if (status == 0) {
                                        return qsTr("Deposited")
                                    } else if (status == 1) {
                                        return qsTr("Extraction")
                                    } else if (status == -1) {
                                        return qsTr("Extraction failed")
                                    } else if (status == -2) {
                                        return qsTr("Deposition failed")
                                    } else {
                                        return qsTr("Unknown, ") + status
                                    }
                                }
                                color: "#13B788"
                            }
                        }
                        Item {
                            Layout.rightMargin: 54
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 6 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumWidth: 300
                            Text {
                                anchors.right: parent.right
                                anchors.verticalCenter: parent.verticalCenter
                                text: qsTr("Extraction")
                                color: "#7038FD"
                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: {
                                    }
                                }
                            }
                        }
                    }
                }
            }

            ListView {
                id: depositDetailView
                model: server.depositDetailModel
                spacing: 12
                clip: true
                ScrollIndicator.vertical: ScrollIndicator { }
                header: Rectangle {
                    z: 2
                    width: parent.width
                    height: headCol.height
                    Column {
                        id: headCol
                        spacing: 8
                        Rectangle {
                            width: depositDetailView.width
                            height: 30
                            color: "blue"
                            visible: false
                        }
                        Rectangle {
                            width: depositDetailView.width
                            height: 50
                            //color: "red"
                            RowLayout {
                                anchors.fill: parent
                                Item {
                                    Layout.leftMargin: 54
                                    Layout.minimumWidth: 100
                                    Layout.preferredWidth: 1 / 4 * parent.width
                                    Layout.preferredHeight: parent.height
                                    Layout.maximumWidth: 500
                                    Text {
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        text: qsTr("Date")
                                    }
                                }
                                Item {
                                    Layout.minimumWidth: 100
                                    Layout.preferredWidth: 1 / 4 * parent.width
                                    Layout.preferredHeight: parent.height
                                    Layout.maximumWidth: 500
                                    Text {
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        text: qsTr("Token")
                                    }
                                }
                                Item {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: parent.height
                                    Text {
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        text: qsTr("Amount")
                                    }
                                }
                                Item {
                                    Layout.rightMargin: 54
                                    Layout.minimumWidth: 100
                                    Layout.preferredWidth: 1 / 4 * parent.width
                                    Layout.preferredHeight: parent.height
                                    Layout.maximumWidth: 500
                                    Text {
                                        anchors.right: parent.right
                                        anchors.verticalCenter: parent.verticalCenter
                                        text: qsTr("Status")
                                    }
                                }
                            }
                            Rectangle {
                                anchors.left: parent.left
                                anchors.leftMargin: 27
                                anchors.right: parent.right
                                anchors.rightMargin: 27
                                anchors.bottom: parent.bottom
                                height: 1
                                color: "#DEDEDE"
                                opacity: 0.5
                            }
                        }
                    }
                }
                headerPositioning: ListView.OverlayHeader
                delegate: Rectangle {
                    width: depositDetailView.width
                    height: 50
                    RowLayout {
                        anchors.fill: parent
                        Item {
                            Layout.leftMargin: 54
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 4 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumWidth: 500
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: date
                            }
                        }
                        Item {
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 4 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumWidth: 500
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: currency
                            }
                        }
                        Item {
                            Layout.fillWidth: true
                            Layout.preferredHeight: parent.height
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: value
                            }
                        }
                        Item {
                            Layout.rightMargin: 54
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 4 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumWidth: 500
                            Text {
                                anchors.right: parent.right
                                anchors.verticalCenter: parent.verticalCenter
                                text: status
                            }
                        }
                    }
                }
            }
        }

        SwitchPage {
            id: currentDepositSwitchPage
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: stackView.bottom
            anchors.topMargin: 16
            visible: tabBar.currentIndex == 0 && listModel.count != 0
            onPageClicked: {
                startBusy()
                var params = { "address": payController.addr, "offset": index * numOfPerPage, "limit": numOfPerPage }
                server.getViolasBankDepositOrders(params, function() {
                    var count =  server.currentDepositModel.count == 0 ? 0 : server.currentDepositModel.get(0).total_count
                    listModel.clear()
                    for (var i = 0; i <  count / numOfPerPage; i++) {
                        listModel.append({index: i})
                    }
                    stopBusy()
                })
            }
        }

        SwitchPage {
            id: depositDetailSwitchPage
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: stackView.bottom
            anchors.topMargin: 16
            visible: tabBar.currentIndex == 1 && listModel.count != 0
            onPageClicked: {
                startBusy()
                var params = { "address": payController.addr, "offset": index * numOfPerPage, "limit": numOfPerPage }
                server.getViolasBankDepositOrderList(params, function() {
                    var count =  server.depositDetailModel.count == 0 ? 0 : server.depositDetailModel.get(0).total_count;
                    listModel.clear()
                    for (var i = listModel.count; i <  count / numOfPerPage; i++) {
                        listModel.append({index: i})
                    }
                    stopBusy()
                })
            }
        }


        Column {
            visible: tabBar.currentIndex == 0 ? server.currentDepositModel.count == 0 : server.depositDetailModel.count == 0
            anchors.centerIn: parent
            spacing: 8
            Image {
                source: "../icons/bank_no_data.svg"
                width: 196
                fillMode: Image.PreserveAspectFit
            }
            Text {
                text: qsTr("No Data")
                anchors.horizontalCenter: parent.horizontalCenter
                color: "#BABABA"
            }
        }
    }
}
