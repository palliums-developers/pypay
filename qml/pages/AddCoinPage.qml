import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"
import "../models/ViolasServer.js" as Server

import PyPay 1.0

Control {
    padding: 8

    property var published: []

    signal goBack

    Timer {
        interval: 5000
        running: true
        repeat: true
        onTriggered: {
            getTokenPublished()
        }
    }

    function getTokenPublished() {
        Server.request('GET', '/1.0/violas/currency/published?addr='+payController.addr, null, function(resp) {
            if (resp.code == 2000) {
                published = resp.data.published
                console.log(published)
            }
        });
    }

    Component.onCompleted: {
        getTokenPublished()

        Server.request('GET', '/1.0/violas/currency', null, function(resp) {
            if (resp.code == 2000) {
                var entries = resp.data.currencies;
                for (var i=0; i<entries.length; i++) {
                    tokenModel.append(entries[i])
                }
            }
        });

        //Server.request('GET', '/1.0/libra/currency', null, function(resp) {
        //    if (resp.code == 2000) {
        //        var entries = resp.data.currencies;
        //        for (var i=0; i<entries.length; i++) {
        //            tokenModel.append(entries[i])
        //        }
        //    }
        //});
    }

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
            text: qsTr("Add Token")
            color: "#333333"
            font.pointSize: 16
            font.weight: Font.Medium
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
        }

        ListModel {
            id: tokenModel
        }

        ListView {
            id: listView
            anchors.top: titleText.bottom
            anchors.topMargin: 22
            anchors.left: parent.left
            anchors.leftMargin: 8
            anchors.right: parent.right
            anchors.rightMargin: 8
            anchors.bottom: parent.bottom
            model: tokenModel
            spacing: 12
            clip: true
            ScrollIndicator.vertical: ScrollIndicator { }
            delegate: Rectangle {
                width: listView.width
                height: 60
                color: "#EBEBF1"
                radius: 14
                MyImage {
                    id: itemImage
                    source: show_icon
                    radius: 20
                    width: 41
                    anchors.left: parent.left
                    anchors.leftMargin: 8
                    anchors.verticalCenter: parent.verticalCenter
                }
                Text {
                    text: show_name
                    anchors.left: itemImage.right
                    anchors.leftMargin: 15
                    anchors.verticalCenter: parent.verticalCenter
                    color: "#333333"
                    font.pointSize: 16
                }
                MySwitch {
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    checkable: true
                    checked: published.includes(show_name)
                    onClicked: {
                        //payController.updateTokenShow(tokenEntry.chain, tokenEntry.name, tokenEntry.isShow)
                    }
                }
            }
        }
    }
}
