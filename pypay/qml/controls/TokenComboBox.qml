import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

ComboBox {
    id: control
    width: 70
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

    indicator: Canvas {
        id: canvas
        x: control.width - width - control.rightPadding
        y: control.topPadding + (control.availableHeight - height) / 2
        width: 12
        height: 8
        contextType: "2d"

        Connections {
            target: control
            function onPressedChanged() { canvas.requestPaint(); }
        }

        onPaint: {
            var ctx = getContext("2d")
            ctx.strokeStyle = "#7038FD"
            ctx.beginPath()
            ctx.moveTo(2,2)
            ctx.lineTo(width/2,height - 2)
            ctx.lineTo(width - 2,2)
            ctx.stroke()
        }
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
        color: control.pressed? "#501BA2" : "#F1EEFB"
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
