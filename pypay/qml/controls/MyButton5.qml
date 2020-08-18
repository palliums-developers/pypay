// 我的资金池 按钮
import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

Button {
    id: control
    text: qsTr("MyButton5")
    hoverEnabled: true
    display: AbstractButton.TextBesideIcon
    opacity: hovered? 0.8 : 1

    property bool selected: false

    background: Rectangle {
        width: control.width
        height: control.height
        color: "#FFFFFF"
        border.color: "#501BA2"
        radius: width / 2
    }

    contentItem: RowLayout {
        spacing: 8
        Image {
            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            source: control.icon.source
        }
        Text {
            text: control.text
            font: control.font
            color: "#501BA2"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
        }
    }
}
