import QtQuick 2.15
import QtGraphicalEffects 1.15

Item {
    id: root
    width: 41
    height: 41
    property string source
    property int radius
    
    Image {
        id: image
        smooth: true
        visible: false
        source: root.source
        sourceSize: Qt.size(parent.size, parent.size)
    }
    Rectangle {
        id: mask
        width: parent.width
        height: parent.height
        radius: root.radius
        visible: false
    }
    OpacityMask {
        anchors.fill: parent
        source: image
        maskSource: mask
        antialiasing: true
    }
} 
