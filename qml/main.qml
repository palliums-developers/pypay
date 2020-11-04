import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import Qt.labs.settings 1.0

import "controls"
import "models"
import "pages"

ApplicationWindow {
    id: appWindow
    width: 1440
    height: 1024
    minimumWidth: 960
    minimumHeight: 540
    visible: true
    title: qsTr("Desktop Pay Wallet")

    property bool userIsLogin: false

    property double leftRecWidth1 : 200
    property double leftRecWidth2 : 300
    property double topRecHeight : 64
    property double fMargin: 8

    function showWalletPage() {
        walletMenuBtn.selected = true
        marketMenuBtn.selected = false
        bankMenuBtn.selected = false
        walletStack.visible = true
        marketStack.visible = false
        bankStack.visible = false
    }

    function showMarketPage() {
        walletMenuBtn.selected = false
        marketMenuBtn.selected = true
        bankMenuBtn.selected = false
        walletStack.visible = false
        marketStack.visible = true
        bankStack.visible = false
    }

    function showBankPage() {
        walletMenuBtn.selected = false
        marketMenuBtn.selected = false
        bankMenuBtn.selected = true
        walletStack.visible = false
        marketStack.visible = false
        bankStack.visible = true
    }

    function showCreatePage(b) {
        createStack.visible = b
    }

    function showImportPage(b) {
        importStack.visible = b
    }

    Settings {
        id: appSettings
        fileName: payController.datadir + "/pypay.ini"
        property alias x: appWindow.x
        property alias y: appWindow.y
        property alias width: appWindow.width
        property alias height: appWindow.height
        property bool eyeIsOpen: false
        property bool walletIsCreate: false
        property bool mnemonicIsBackup: false
        property string password: ""
    }

    Component.onCompleted: {
        if (appSettings.walletIsCreate) {
            payController.createWallet()
        }
        //console.log(payController.datadir)
        server.getViolasCurrency()
        server.getViolasBankProductDeposit()
        server.getViolasBankProductBorrow()
    }

    Connections {
        target: payController
        function onAddr_changed() {
            var params = {"address": payController.addr}
            server.getTokenPublished(params)
            server.getViolasBankAccountInfo(params)
            server.getViolasBalance(params)
        }
    }

    onClosing: {
        payController.shutdown()
        timer.running = false
    }

    Timer {
        id: timer
        interval: 10000
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: {
            walletPage.getTokenBalance()
            var params = { "address": payController.addr }
            server.getViolasBankAccountInfo(params)
            server.getViolasBalance(params)
        }
    }

    ViolasServer {
        id: server
    }
    
    Rectangle {
        anchors.fill: parent
        color: "#F7F7F9"
        
        // Left rectangle
        Rectangle {
            id: leftRec
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            //width: parent.width > 1920 ? leftRecWidth2 : leftRecWidth1
            width: leftRecWidth1
            color: "#501BA2"
            z: 999
            // logo
            Item {
                anchors.top: parent.top
                anchors.left: parent.left
                width: parent.width
                height: topRecHeight
                Image {
                    anchors.centerIn: parent
                    height: 0.7 * parent.height
                    source: "icons/logo.svg"
                    fillMode: Image.PreserveAspectFit
                }
            }

            MenuButton {
                id: walletMenuBtn
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.topMargin: 140
                height: 80
                icon.source: "icons/walleticon.svg"
                text: qsTr("Wallet")
                selected: true
                onClicked: {
                    showWalletPage()
                }
            }
            MenuButton {
                id: marketMenuBtn
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: walletMenuBtn.bottom
                anchors.topMargin: 10
                height: 80
                icon.source: "icons/marketicon.svg"
                text: qsTr("Market")
                onClicked: {
                    showMarketPage()
                }
            }
            MenuButton {
                id: bankMenuBtn
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: marketMenuBtn.bottom
                anchors.topMargin: 10
                height: 80
                icon.source: "icons/bank.svg"
                text: qsTr("Bank")
                onClicked: {
                    showBankPage()

                }
            }
        }

        // Top rectangle
        Rectangle {
            id: topRec
            anchors.top: parent.top
            anchors.left: leftRec.right
            anchors.right: parent.right
            height: topRecHeight
            color: "#FFFFFF"

            Row {
                spacing: 43
                anchors.right: parent.right
                anchors.rightMargin: 43
                anchors.verticalCenter: parent.verticalCenter
                ImageButton {
                    id: myButton
                    source: "./icons/me.svg"
                    height: 24
                    anchors.verticalCenter: parent.verticalCenter
                    fillMode: Image.PreserveAspectFit
                    visible: appSettings.walletIsCreate
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            if (appWindow.userIsLogin) {
                                myPopupPage.open()
                            }
                        }
                    }
                    Popup {
                        id: myPopupPage
                        x: parent.x
                        y: parent.y + parent.height + 5
                        width: 170
                        height: 250
                        background: Rectangle {
                            border.color: "lightsteelblue"
                        }
                        contentItem: MyPage {
                            id: myPage
                            anchors.fill: parent
                            onReceiveClicked: {
                                walletStack.push(receivePage)
                                myPopupPage.close()
                            }
                            onSendClicked: {
                                walletStack.push(sendPage)
                                myPopupPage.close()
                            }
                            onWalletManageClicked: {
                                walletStack.push(walletManagePage)
                                myPopupPage.close()
                            }
                        }
                    }
                }

                // Import button
                MyButton {
                    id: importBtn
                    text: qsTr("Import")
                    anchors.verticalCenter: parent.verticalCenter
                    background.implicitWidth: 29
                    background.implicitHeight: 14
                    visible: !appSettings.walletIsCreate
                    onClicked: {
                        showImportPage(true)
                    }
                }

                // Create button
                MyButton {
                    id: createBtn
                    text: qsTr("Create")
                    anchors.verticalCenter: parent.verticalCenter
                    background.implicitWidth: 29
                    background.implicitHeight: 14
                    visible: !appSettings.walletIsCreate
                    onClicked: {
                        showCreatePage(true)
                    }
                }

                //// Download button
                //MyButton {
                //    id: downloadBtn
                //    text: qsTr("下载")
                //    anchors.verticalCenter: parent.verticalCenter
                //    background.implicitWidth: 29
                //    background.implicitHeight: 14
                //}

                // i18n MyComboBox
                MyComboBox {
                    id: tsComboBox               
                    width: 150
                    anchors.verticalCenter: parent.verticalCenter
                }
            }
        }

        // Right bottom center area
        Rectangle {
            anchors.top: topRec.bottom
            anchors.topMargin: fMargin
            anchors.bottom: parent.bottom
            anchors.left: leftRec.right
            anchors.leftMargin: fMargin
            anchors.right: parent.right
            color: "#FFFFFF"

            // Wallet stack view
            StackView {
                id: walletStack
                anchors.fill: parent
                initialItem: walletPage
            }

            // Wallet page
            WalletPage {
                id: walletPage
                onBackupMnemonicClicked: {
                    createStack.clear()
                    createStack.push(backupMnemonic)
                    showCreatePage(true)
                }
                onReceiveClicked: {
                    walletStack.push(receivePage)
                }
                onSendClicked: {
                    walletStack.push(sendPage)
                }
                onExchangeClicked: {
                    walletStack.push(exchangePage)
                }
            }

            // Receive
            Component {
                id: receivePage
                ReceivePage {
                    onBackArrowClicked: {
                        walletStack.pop()
                    }
                }
            }

            // Send
            Component {
                id: sendPage
                SendPage {
                    onBackArrowClicked: {
                        walletStack.pop()
                    }
                }
            }

            // Exchange
            Component {
                id: exchangePage
                ExchangePage {
                    onBackArrowClicked: {
                        walletStack.pop()
                    }
                }
            }

            // Wallet manage
            Component {
                id: walletManagePage
                WalletManagePage {
                    onBackArrowClicked: {
                        walletStack.pop()
                    }
                }
            }

            // Market stack view
            StackView {
                id: marketStack
                anchors.fill: parent
                initialItem: marketPage
                visible: false
            }

            // Market page
            Component {
                id: marketPage
                MarketPage {
                }
            }

            // Bank view

            StackView {
                id: bankStack
                anchors.fill: parent
                initialItem: bankPage
                visible: false
            }

            // Bank page
            Loader {
                id: bankPage
                source: "pages/BankPage.qml"
            }
            Connections {
                target: bankPage.item
                function onShowDepositPage(requestID) {
                    server.requestID = requestID
                    depositPage.source = "pages/DepositPage.qml"
                    bankStack.push(depositPage)
                }
                function onShowBorrowPage(requestID) {
                    server.requestID = requestID
                    borrowPage.source = "pages/BorrowPage.qml"
                    bankStack.push(borrowPage)
                }
                function onShowDepositOrderPage() {
                    depositOrderPage.source = "pages/DepositOrderPage.qml"
                    bankStack.push(depositOrderPage)
                }
                function onShowBorrowOrderPage() {
                    borrowOrderPage.source = "pages/BorrowOrderPage.qml"
                    bankStack.push(borrowOrderPage)
                }
            }

            // Deposit page
            Loader {
                id: depositPage
            }
            Connections {
                target: depositPage.item
                function onBackArrowClicked() {
                    bankStack.pop()
                    depositPage.source = ""
                }
            }

            // Borrow page
            Loader {
                id: borrowPage
            }
            Connections {
                target: borrowPage.item
                function onBackArrowClicked() {
                    bankStack.pop()
                    borrowPage.source = ""
                }
            }

            Loader {
                id: depositOrderPage
            }
            Connections {
                target: depositOrderPage.item
                function onBackArrowClicked() {
                    bankStack.pop()
                    depositOrderPage.source = ""
                }
            }

            Loader {
                id: borrowOrderPage
            }
            Connections {
                target: borrowOrderPage.item
                function onBackArrowClicked() {
                    bankStack.pop()
                    borrowOrderPage.source = ""
                }
            }

            EnterPasswordPage {
                id: enterPasswordPage
                anchors.fill: parent
                visible: appSettings.walletIsCreate
                onEnterClicked: {
                    enterPasswordPage.visible = false
                }
            }

            // Create stack view
            StackView {
                id: createStack
                anchors.fill: parent
                initialItem: setPasswordPage
                visible: false
            }

            // Set password
            Component {
                id: setPasswordPage
                SetPasswordPage {
                    onBackArrowClicked: {
                        showCreatePage(false)
                    }
                    onCreateClicked: {
                        createStack.push(getMnemonic)
                    }
                }
            }

            // Get Mnemonic
            Component {
                id: getMnemonic
                GetMnemonicPage {
                    onBackArrowClicked: {
                        createStack.pop()
                    }
                    onBackupClicked: {
                        createStack.push(backupMnemonic)
                    }
                    onLaterBackupClicked: {
                        showCreatePage(false)
                        enterPasswordPage.visible = false
                        appWindow.userIsLogin = true
                    }
                }
            }

            // Backup Mnemonic
            Component {
                id: backupMnemonic
                BackupMnemonicPage {
                    onBackArrowClicked: {
                        createStack.pop()
                    }
                    onNextBtnClicked: {
                        createStack.push(confirmMnemonic)
                    }
                }
            }

            // Confirm Mnemonic
            Component {
                id: confirmMnemonic
                ConfirmMnemonicPage {
                    onBackArrowClicked: {
                        createStack.pop()
                    }
                    onCompleteBtnClicked: {
                        showCreatePage(false)
                        enterPasswordPage.visible = false
                        appWindow.userIsLogin = true
                    }
                }
            }

            // Import wallet stack view
            StackView {
                id: importStack
                anchors.fill: parent
                initialItem: importPage
                visible: false
            }

            // Import
            Component {
                id: importPage
                ImportPage {
                    onBackArrowClicked: {
                        showImportPage(false)
                    }
                    onImportClicked: {
                        showImportPage(false)
                        enterPasswordPage.visible = false
                        appWindow.userIsLogin = true
                    }
                }
            }
        }

        // Coin detail
        Popup {
            id: coinDetailPage
            x: parent.width - width
            y: topRec.height
            width: 436
            height: parent.height - topRec.height
            background: Rectangle {
                border.color: "lightsteelblue"
            }
            contentItem: Item {
                CoinDetailPage {
                    id: coinDetail
                    anchors.fill: parent
                    onGoBack: {
                        coinDetailPage.close()
                    }
                    onTransactionDetailOpened: {
                        coinDetail.visible = false
                        transactionDetail.visible = true
                    }
                }
                TransactionDetailPage {
                    id: transactionDetail
                    anchors.fill: parent
                    visible: false
                    onGoBack: {
                        coinDetail.visible = true
                        transactionDetail.visible = false
                    }
                }
            }
            onOpened: {
                coinDetail.visible = true
                transactionDetail.visible = false
            }
        }

        // Add coin
        Popup {
            id: addCoinPage
            x: parent.width - width
            y: topRec.height
            width: 436
            height: parent.height - topRec.height
            background: Rectangle {
                border.color: "lightsteelblue"
            }
            contentItem: AddCoinPage {
                id: addCoin
                anchors.fill: parent
                onGoBack: {
                    addCoinPage.close()
                }
            }
        }

        // Addr book
        Popup {
            id: addrBookPage
            x: parent.width - width
            y: topRec.height
            width: 436
            height: parent.height - topRec.height
            background: Rectangle {
                border.color: "lightsteelblue"
            }
            contentItem: Item {
                AddrBookPage {
                    id: addrBook
                    anchors.fill: parent
                    onGoBack: {
                        addrBookPage.close()
                    }
                    onAddAddrClicked: {
                        addrBook.visible = false
                        addAddrPage.visible = true
                        console.log("main add addr")
                    }
                }
                AddAddrPage {
                    id: addAddrPage
                    anchors.fill: parent
                    visible: false
                    onGoBack: {
                        addrBook.visible = true
                        addAddrPage.visible = false
                    }
                }
            }
            onOpened: {
                addrBook.visible = true
                addAddrPage.visible = false
            }
        }
    }
}
