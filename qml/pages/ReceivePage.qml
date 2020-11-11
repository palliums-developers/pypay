import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"

Page {
    id: root
    signal backArrowClicked
    property string chain: "bitcoin"

    function getImageSource() {
        var src = server.data_dir + "/qr_%1-%2.png"
        return src.arg(tokenComboBox.chain).arg(tokenComboBox.name)
    }

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
        text: qsTr("收款")
        font.pointSize: 20
        color: "#3B3847"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 197.0 / 952 * parent.height
    }

    TokenComboBox {
        id: tokenComboBox
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 272.0 / 952 * parent.height
        width: 100
        height: 33
        onTokenSelected: {
            server.gen_qr(chain, name)
            qrImage.source = getImageSource()
            root.chain = chain
        }
        Component.onCompleted: {
            server.gen_qr(chain, name)
            qrImage.source = getImageSource()
            root.chain = chain
        }
    }

    // 二维码 TODO
    Image {
        id: qrImage
        width: 155
        height: 155
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 347.0 / 952 * parent.height
    }

    // 地址, 复制按钮
    Row {
        anchors.top: qrImage.bottom
        anchors.topMargin: 40
        anchors.horizontalCenter: parent.horizontalCenter
        spacing: 16
        Text {
            id: addrText
            text: root.chain == "bitcoin" ? server.address_bitcoin : server.address_violas      // TODO
            color: "#382F44"
            font.weight: Font.Medium
            font.pointSize: 18
            anchors.verticalCenter: copyBtn.verticalCenter
        }
        ImageButton {
            id: copyBtn
            source: "../icons/copy.svg"
            width: 20
            height: 23
            MouseArea {
                anchors.fill: parent
                onClicked: server.copy(addrText.text)
            }
        }
    }
}
