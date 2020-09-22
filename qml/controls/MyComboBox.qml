import QtQuick 2.14
import QtQuick.Controls 2.14

ComboBox {
    id: control
    model: [qsTr("English"), qsTr("简体中文")]
    spacing: 2

    delegate: ItemDelegate {
        width: control.width
        contentItem: Text {
            text: modelData
            color: control.pressed? "#FFFFFF" : "#501BA2"
            font: control.font
            elide: Text.ElideRight
            verticalAlignment: Text.AlignVCenter
        }
        highlighted: control.highlightedIndex === index
    }

    indicator: Image {
        x: control.width - width - control.rightPadding
        y: control.topPadding + (control.availableHeight - height) / 2
        width: 11
        fillMode: Image.PreserveAspectFit
        source: control.pressed? "../icons/tsswitch_pressed.svg" : "../icons/tsswitch.svg"
    }

    contentItem: Text {
        leftPadding: 10
        rightPadding: control.indicator.width + control.spacing

        text: control.displayText
        font: control.font
        color: control.pressed? "#FFFFFF" : "#501BA2"
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    background: Rectangle {
        implicitWidth: 95
        implicitHeight: 24
        border.color: "#501BA2"
        border.width: control.visualFocus ? 2 : 1
        color: control.pressed? "#501BA2" : "#FFFFFF"
        radius: width / 2
    }

    popup: Popup {
        y: control.height - 1
        width: control.width
        implicitHeight: contentItem.implicitHeight
        padding: 1

        contentItem: ListView {
            clip: true
            implicitHeight: contentHeight
            model: control.popup.visible ? control.delegateModel : null
            currentIndex: control.highlightedIndex

            ScrollIndicator.vertical: ScrollIndicator { }
        }

        background: Rectangle {
            color: "#F1EEFB"
        }
    }
}
