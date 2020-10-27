import QtQuick 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.15

import "../controls"
import "../pages"

import PyPay 1.0

PyPayPage {
    id: root
    isShowHeader: true
    title: qsTr("Bank > <b>Borrow Orders</b>")

    Component.onCompleted: {
        startBusy()
        var params = { "address": payController.addr, "offset": 0, "limit": 10 }
        server.getViolasBankBorrowOrders(params, function() {
            var count =  server.currentBorrowModel.count == 0 ? 0 : server.currentBorrowModel.get(0).total_count
            var numOfPerPage = currentBorrowSwitchPage.numOfPerPage
            for (var i = 0; i <  count / numOfPerPage; i++) {
                currentBorrowSwitchPage.listModel.append({index: i})
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
                text: qsTr("Current Borrow")
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
                onToggled: {
                    if (server.currentBorrowModel.count == 0) {
                    }
                }
            }

            TabButton {
                text: qsTr("Borrow Detail")
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
                    if (server.borrowDetailModel.count == 0) {
                        startBusy()
                        var params = { "address": payController.addr, "offset": 0, "limit": 10 }
                        server.getViolasBankBorrowOrderList(params, function() {
                            var count =  server.borrowDetailModel.count == 0 ? 0 : server.borrowDetailModel.get(0).total_count
                            var numOfPerPage = borrowDetailSwitchPage.numOfPerPage
                            for (var i = 0; i <  count / numOfPerPage; i++) {
                                borrowDetailSwitchPage.listModel.append({index: i})
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
                id: currentBorrowView
                model: server.currentBorrowModel
                spacing: 12
                clip: true
                ScrollIndicator.vertical: ScrollIndicator { }
                ScrollIndicator.horizontal: ScrollIndicator { }
                header: Rectangle {
                    z: 2
                    width: parent.width
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
                                text: qsTr("Token")
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
                                text: qsTr("Amount")
                            }
                        }
                        Item {
                            Layout.fillWidth: true
                            Layout.preferredHeight: parent.height
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: qsTr("Available Borrow")
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
                    width: currentBorrowView.width
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
                                text: name
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
                                text: amount.toFixed(2)
                            }
                        }
                        Item {
                            Layout.fillWidth: true
                            Layout.preferredHeight: parent.height
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: available_borrow.toFixed(2)
                            }
                        }
                        Item {
                            Layout.rightMargin: 54
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 4 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumWidth: 250
                            RowLayout {
                                anchors.fill: parent
                                spacing: 0
                                TextButton {
                                    text: qsTr("Repayment")
                                    onClicked: {
                                        console.log("...")
                                    }
                                }
                                TextButton {
                                    Layout.alignment: Qt.AlignmentVCenter | Qt.AlignHCenter
                                    text: qsTr("Borrow")
                                    onClicked: {
                                        console.log("...")
                                    }
                                }
                                TextButton {
                                    Layout.alignment: Qt.AlignmentVCenter | Qt.AlignRight
                                    text: qsTr("Detail")
                                    onClicked: {
                                        console.log("...")
                                    }
                                }
                            }
                        }
                    }
                }
            }

            ListView {
                id: borrowDetailView
                model: server.borrowDetailModel
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
                            width: borrowDetailView.width
                            height: 30
                            color: "blue"
                            visible: false
                        }
                        Rectangle {
                            width: borrowDetailView.width
                            height: 50
                            RowLayout {
                                anchors.fill: parent
                                Item {
                                    Layout.leftMargin: 54
                                    Layout.minimumWidth: 100
                                    Layout.preferredWidth: 1 / 5 * parent.width
                                    Layout.preferredHeight: parent.height
                                    Layout.maximumHeight: 400
                                    Text {
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        text: qsTr("Date")
                                    }
                                }
                                Item {
                                    Layout.minimumWidth: 100
                                    Layout.preferredWidth: 1 / 5 * parent.width
                                    Layout.preferredHeight: parent.height
                                    Layout.maximumHeight: 400
                                    Text {
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        text: qsTr("Token")
                                    }
                                }
                                Item {
                                    Layout.minimumWidth: 100
                                    Layout.preferredWidth: 1 / 5 * parent.width
                                    Layout.preferredHeight: parent.height
                                    Layout.maximumHeight: 400
                                    Text {
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        text: qsTr("Amount")
                                    }
                                }
                                Item {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: parent.height
                                    Text {
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        text: qsTr("Fee")
                                    }
                                }
                                Item {
                                    Layout.rightMargin: 54
                                    Layout.minimumWidth: 100
                                    Layout.preferredWidth: 1 / 5 * parent.width
                                    Layout.preferredHeight: parent.height
                                    Layout.maximumHeight: 400
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
                    width: borrowDetailView.width
                    height: 50
                    RowLayout {
                        anchors.fill: parent
                        Item {
                            Layout.leftMargin: 54
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 5 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumHeight: 400
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: date
                            }
                        }
                        Item {
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 5 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumHeight: 400
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: currency
                            }
                        }
                        Item {
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 5 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumHeight: 400
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: value
                            }
                        }
                        Item {
                            Layout.fillWidth: true
                            Layout.preferredHeight: parent.height
                            Text {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: "ーー"
                            }
                        }
                        Item {
                            Layout.rightMargin: 54
                            Layout.minimumWidth: 100
                            Layout.preferredWidth: 1 / 5 * parent.width
                            Layout.preferredHeight: parent.height
                            Layout.maximumHeight: 400
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
            id: currentBorrowSwitchPage
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: stackView.bottom
            anchors.topMargin: 16
            visible: tabBar.currentIndex == 0 && listModel.count != 0
            onPageClicked: {
                startBusy()
                var params = { "address": payController.addr, "offset": index * numOfPerPage, "limit": numOfPerPage }
                server.getViolasBankBorrowOrders(params, function() {
                    var count =  server.currentBorrowModel.count == 0 ? 0 : server.currentBorrowModel.get(0).total_count
                    listModel.clear()
                    for (var i = 0; i <  count / numOfPerPage; i++) {
                        listModel.append({index: i})
                    }
                    stopBusy()
                })
            }
        }

        SwitchPage {
            id: borrowDetailSwitchPage
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: stackView.bottom
            anchors.topMargin: 16
            visible: tabBar.currentIndex == 1 && listModel.count != 0
            onPageClicked: {
                startBusy()
                var params = { "address": payController.addr, "offset": index * numOfPerPage, "limit": numOfPerPage }
                server.getViolasBankBorrowOrderList(params, function() {
                    var count =  server.borrowDetailModel.count == 0 ? 0 : server.borrowDetailModel.get(0).total_count;
                    listModel.clear()
                    for (var i = listModel.count; i <  count / numOfPerPage; i++) {
                        listModel.append({index: i})
                    }
                    stopBusy()
                })
            }
        }

        Column {
            visible: tabBar.currentIndex == 0 ? server.currentBorrowModel.count == 0 : server.borrowDetailModel.count == 0
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
