import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"

Page {
    id: root
    signal backArrowClicked
    property string chain: "bitcoin"

    function getBalance(chain, name) {
        //payController.getCurBalance(chain, name)
    }

    ImageButton {
        id: backBtn
        anchors.top: parent.top
        anchors.topMargin: 98
        anchors.left: parent.left
        anchors.leftMargin: 92
        width: 24
        height: 24
        source: "../icons/backarrow3.svg"
        MouseArea {
            anchors.fill: parent
            onClicked: {
                backArrowClicked()
            }
        }
    }

    Text {
        id: titleText
        text: qsTr("钱包 > <b>映射</b>")
        font.pointSize: 14
        color: "#333333"
        anchors.verticalCenter: backBtn.verticalCenter
        anchors.left: backBtn.right
        anchors.leftMargin: 8
    }

    Row {
        id: tipRow
        anchors.left: amountTextField.left
        anchors.bottom: amountTextField.top
        anchors.bottomMargin: 8
        spacing: 4
        Image {
            id: tipImage
            source: "../icons/availablebalance.svg"
            width: 12
            fillMode: Image.PreserveAspectFit
        }
        Text {
            anchors.verticalCenter: tipImage.verticalCenter
            //text: qsTr("可用余额: ") + payController.curBalance
            font.pointSize: 12
            color: "#5C5C5C"
        }
    }

    // 输入框 + 币种选择
    TextFieldComboBox {
        id: amountTextField
        placeholderText: qsTr("转出数量")
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 147 / 825 * parent.height
        width: 636 / 1160 * parent.width
        isShowViolasCoin: false
        Component.onCompleted: {
            getBalance(chain, name)
        }
        onTokenSelectedChanged: {
            getBalance(chain, name)
        }
    }
    
    // 箭头
    Image {
        id: arrowImage
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: amountTextField.bottom
        anchors.topMargin: 8
        source: "../icons/bottomarrow.svg"
        width: 12
        fillMode: Image.PreserveAspectFit
    }

    // 输出显示
    Text {
        id: outText
        text: "0 " + "V-BTC"
        font.pointSize: 14
        color: "#333333"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: arrowImage.bottom
        anchors.topMargin: 8
    }

    // 横线
    Rectangle {
        id: hLine
        width: 598 / 1160 * parent.width
        height: 1
        color: "#3C3848"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: outText.bottom
        anchors.topMargin: 30
        opacity: 0.1
    }

    // 汇率， 矿工费用
    Text {
        id: rateText
        anchors.left: hLine.left
        anchors.top: hLine.bottom
        anchors.topMargin: 24
        text: qsTr("汇率: 1BTC = 0.01V-BTC") 
        font.pointSize: 12
        color: "#333333"
    }
    Text {
        id: feeText
        anchors.left: hLine.left
        anchors.top: rateText.bottom
        anchors.topMargin: 4
        text: qsTr("矿工费用: ")
        font.pointSize: 12
        color: "#333333"
    }

    MyButton3 {
        id: exchangeBtn
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: feeText.bottom
        anchors.topMargin: 24
        text: qsTr("确定映射")
        width: 200
    }
}
