import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"

Control {
    id: root
    padding: 8

    signal goBack
    property string addr: ""

    contentItem: Item {
        Image {
            source: "../icons/backarrow.svg"
            anchors.left: parent.left
            anchors.verticalCenter: titleText.verticalCenter
            width: 16
            fillMode: Image.PreserveAspectFit
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    goBack()
                }
            }
        }
        Text {
            id: titleText
            text: qsTr("币种详情")
            color: "#333333"
            font.pointSize: 16
            font.weight: Font.Medium
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Image {
            id: ima
            anchors.left: parent.left
            anchors.leftMargin: 8
            anchors.right: parent.right
            anchors.rightMargin: 8
            anchors.top: titleText.bottom
            anchors.topMargin: 25
            height: 140
            source: "../icons/coindetailbackground.svg"
            Item {
                anchors.fill: parent
                ColumnLayout {
                    id: colLayout
                    anchors.fill: parent
                    Row {
                        spacing: 8
                        MyImage {
                            source: server.token_requested_wallet.show_icon
                            width: height
                            height: 14
                            radius: 0.5 * width
                            anchors.verticalCenter: nameText.verticalCenter
                        }
                        Text {
                            id: nameText
                            text: server.token_requested_wallet.show_name
                            color: "#999999"
                            font.weight: Font.Normal
                            font.pointSize: 12
                        }
                    }
                    Text {
                        text: appSettings.eyeIsOpen ? server.format_balance(server.token_requested_wallet.chain, server.token_requested_wallet.balance) : "******"
                        color: "#333333"
                        font.weight: Font.Bold
                        font.pointSize: 18
                    }
                    Text {
                        text: appSettings.eyeIsOpen ? "≈$" + (server.get_rate(server.token_requested_wallet.chain, server.token_requested_wallet.show_name) * server.format_balance(server.token_requested_wallet.chain, server.token_requested_wallet.balance)).toFixed(2) : "******"
                        color: "#999999"
                        font.weight: Font.Normal
                        font.pointSize: 12
                    }
                    Row {
                        spacing: 4
                        Text {
                            id: addrText
                            text: {
                                if (server.token_requested_wallet.chain == 'bitcoin') {
                                    root.addr = server.address_bitcoin
                                    return server.address_bitcoin
                                } else if (server.token_requested_wallet.chain == 'diem') {
                                    root.addr = server.address_libra
                                    return server.address_libra
                                } else if (server.token_requested_wallet.chain == 'violas') {
                                    root.addr = server.address_violas
                                    return server.address_violas
                                } else {
                                    return 'noknown chain'
                                }
                            }
                            color: "#5C5C5C"
                            font.weight: Font.Medium
                            font.pointSize: 14
                            width: colLayout.width - 8 * 2 - 4 - copyImgBtn.width
                            elide: Text.ElideMiddle
                            verticalAlignment: Text.AlignVCenter
                        }
                        ImageButton {
                            id: copyImgBtn
                            source: "../icons/copy.svg"
                            width: 10
                            height: 12
                            anchors.verticalCenter: addrText.verticalCenter
                            MouseArea {
                                anchors.fill: parent
                                onClicked: server.copy_text(addrText.text)
                            }
                        }
                    }
                }
            }
        }

        Row {
            id: rowBar
            anchors.left: ima.left
            anchors.leftMargin: 16
            anchors.top: ima.bottom
            anchors.topMargin: 32
            spacing: 40

            function disableSelect() {
                allText.isSelected = false
                inText.isSelected = false
                outText.isSelected = false
            }

            Text {
                id: allText
                text: qsTr("全部")
                property bool isSelected: true
                color: isSelected? "#7038FD" : "#C2C2C2"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        rowBar.disableSelect()
                        parent.isSelected = !parent.isSelected
                        if (server.token_requested_wallet.chain == "diem") {
                            //
                        } else if (server.token_requested_wallet.chain == "violas") {
                            var addr = server.address_violas
                            var name = server.token_requested_wallet.show_name
                            var offset = 0
                            var limit = 20
                            var params = { "addr": addr , "currency": name , "offset": offset, "limit": limit}
                            server.get_history_violas(params)
                        } else if (server.token_requested_wallet.chain == 'bitcoin') {
                            //
                        } else {
                            console.log("invaild")
                        }
                    }
                }
            }
            Text {
                id: inText
                text: qsTr("转入")
                property bool isSelected: false
                color: isSelected? "#7038FD" : "#C2C2C2"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        rowBar.disableSelect()
                        parent.isSelected = !parent.isSelected
                        if (server.token_requested_wallet.chain == "diem") {
                            //
                        } else if (server.token_requested_wallet.chain == "violas") {
                            var addr = server.address_violas
                            var name = server.token_requested_wallet.show_name
                            var flows = 1
                            var offset = 0
                            var limit = 20
                            var params = { "addr": addr , "currency": name , "flows": flows, "offset": offset, "limit": limit}
                            server.get_history_violas(params)
                        } else if (server.token_requested_wallet.chain == 'bitcoin') {
                        } else {
                            console.log("invaild")
                        }
                    }
                }
            }
            Text {
                id: outText
                text: qsTr("转出")
                property bool isSelected: false
                color: isSelected? "#7038FD" : "#C2C2C2"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        rowBar.disableSelect()
                        parent.isSelected = !parent.isSelected
                        if (server.token_requested_wallet.chain == "diem") {
                            //
                        } else if (server.token_requested_wallet.chain == "violas") {
                            var addr = server.address_violas
                            var name = server.token_requested_wallet.show_name
                            var flows = 0
                            var offset = 0
                            var limit = 20
                            var params = { "addr": addr , "currency": name , "flows": flows, "offset": offset, "limit": limit}
                            server.get_history_violas(params)
                        } else if (server.token_requested_wallet.chain == 'bitcoin') {
                        } else {
                            console.log("invaild")
                        }
                    }
                }
            }
        }

        ListView {
            id: listView
            anchors.top: rowBar.bottom
            anchors.topMargin: 22
            anchors.left: rowBar.left
            anchors.right: ima.right
            anchors.rightMargin: 16
            anchors.bottom: parent.bottom
            model: server.model_history
            spacing: 8
            clip: true
            ScrollIndicator.vertical: ScrollIndicator { }
            delegate: Rectangle {
                width: listView.width
                height: 40
                radius: 5
                color: "#EBEBF1"
                Image {
                    id: itemImage
                    source: sender == root.addr ? "../icons/send_history.svg" : "../icons/receive_history.svg"
                    width: 24
                    fillMode: Image.PreserveAspectFit
                    anchors.left: parent.left
                    anchors.leftMargin: 8
                    anchors.verticalCenter: parent.verticalCenter
                }
                Column {
                    anchors.left: itemImage.right
                    anchors.leftMargin: 16
                    anchors.verticalCenter: parent.verticalCenter
                    Text {
                        id: versionText
                        text: version
                        color: "#333333"
                        font.pointSize: 12
                    }
                    Text {
                        id: dateTime
                        text: server.format_timestamp(confirmed_time)
                        color: "#BCBCBC"
                        font.pointSize: 10
                    }
                }
                Text {
                    id: amountText
                    text: server.format_balance('violas', amount)
                    anchors.right: parent.right
                    anchors.rightMargin: 8
                    anchors.verticalCenter: parent.verticalCenter   
                    color: sender == root.addr ? "#FB8F0B" : "#13B788"
                    font.pointSize: 12
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        server.violas_transaction_detail = {
                            'amount':  amount,
                            'confirmed_time': confirmed_time,
                            'currency': currency,
                            'expiration_time': expiration_time,
                            'gas': gas,
                            'gas_currency': gas_currency,
                            'receiver': receiver,
                            'sender': sender,
                            'sequence_number': sequence_number,
                            'status': status,
                            'type': type,
                            'version': version
                        }
                        transactionDetail.open()
                    }
                }
            }
        }
    }
}
