import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import Qt.labs.settings 1.0

import "models"
import "controls"
import "pages"

ApplicationWindow {
    id: appWindow
    width: 1440
    height: 1024
    minimumWidth: 960
    minimumHeight: 540
    visible: true
    title: qsTr("ViolasPay桌面钱包")

    property bool userIsLogin: false
    property var currencies_show: ["BTC","XUS","VLS"]

    property double leftRecWidth1 : 200
    property double leftRecWidth2 : 300
    property double topRecHeight : 64
    property double fMargin: 8

    function popStackView() {
        walletStack.pop(null)
        marketStack.pop(null)
        bankStack.pop(null)
    }

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
        fileName: server.data_dir + "/pypay.ini"
        property alias x: appWindow.x
        property alias y: appWindow.y
        property alias width: appWindow.width
        property alias height: appWindow.height
        property bool eyeIsOpen: false
        property bool walletIsCreate: false
        property bool mnemonicIsBackup: false
        property string password: ""
        property string currencies: ""
        property string locale_name: ""
    }

    Component.onCompleted: {
        if (appSettings.locale_name == "") {
            appSettings.locale_name = server.system_locale_name
        }
        server.change_locale(appSettings.locale_name)
        if (appSettings.walletIsCreate) {
            server.create_wallet()
            currencies_show = appSettings.currencies.split(",")
        }
        console.log(server.data_dir)
    }

    onClosing: {
        appSettings.currencies = currencies_show.join(",")
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
                    height: parent.height * 0.5
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
                text: qsTr("钱包")
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
                text: qsTr("市场")
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
                text: qsTr("数字银行")
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

                // Import button
                MyButton {
                    id: importBtn
                    text: qsTr("导入")
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
                    text: qsTr("创建")
                    anchors.verticalCenter: parent.verticalCenter
                    background.implicitWidth: 29
                    background.implicitHeight: 14
                    visible: !appSettings.walletIsCreate
                    onClicked: {
                        showCreatePage(true)
                    }
                }

                ImageButton {
                    id: notifyButton
                    source: "./icons/notify.svg"
                    height: 24
                    anchors.verticalCenter: parent.verticalCenter
                    fillMode: Image.PreserveAspectFit
                    visible: appSettings.walletIsCreate
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                        }
                    }
                }

                // Download button
                MyButton {
                    id: downloadBtn
                    text: qsTr("下载")
                    anchors.verticalCenter: parent.verticalCenter
                    background.implicitWidth: 29
                    background.implicitHeight: 14
                }

                ImageButton {
                    id: myButton
                    source: "./icons/me.svg"
                    height: 22
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
                        x: 0
                        y: parent.height + 4
                        width: 170
                        height: 355
                        background: Rectangle {
                            border.color: "lightsteelblue"
                            radius: 4
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
                            onShowWalletHomeClicked: {
                                popStackView()
                                showWalletPage()
                                myPopupPage.close()
                            }
                            onMineRewardClicked: {
                                walletStack.push(mineRewardPage)
                                myPopupPage.close()
                            }
                            onInviteRewardClicked: {
                                walletStack.push(inviteRewardPage)
                                myPopupPage.close()
                            }
                        }
                    }
                }

                // i18n MyComboBox
                MyComboBox {
                    id: tsComboBox               
                    width: 150
                    anchors.verticalCenter: parent.verticalCenter
                    currentIndex: {
                        if (appSettings.locale_name == "en_US") {
                            return 0
                        } else if (appSettings.locale_name == "zh_CN") {
                            return 1
                        } else {
                            return 1
                        }
                    }
                    onActivated: {
                        if (index == 0) {
                            appSettings.locale_name = "en_US"
                        } else if (index == 1) {
                            appSettings.locale_name = "zh_CN"
                        } else {
                            appSettings.locale_name = "zh_CN"
                        }
                        server.change_locale(appSettings.locale_name)
                    }
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

            // MineReward
            Component {
                id: mineRewardPage
                MineRewardPage {
                    //onBackArrowClicked: {
                    //    walletStack.pop()
                    //}
                }
            }

            // InviteRewardPage
            Component {
                id: inviteRewardPage
                InviteRewardPage {
                    
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
            MarketPage {
                id: marketPage
            }

            // Bank view
            StackView {
                id: bankStack
                anchors.fill: parent
                initialItem: bankPage
                visible: false
            }

            // Bank page
            BankPage {
                id: bankPage
                onShowDepositPage: {
                    server.id_requested_bank = id
                    bankStack.push(depositPage)
                }
                onShowBorrowPage: {
                    server.id_requested_bank = id
                    bankStack.push(borrowPage)
                }
                onShowDepositOrderPage: {
                    bankStack.push(depositOrderPage)
                }
                onShowBorrowOrderPage: {
                    bankStack.push(borrowOrderPage)
                }
            }

            // Deposit page
            Component {
                id: depositPage
                DepositPage {
                    onBackArrowClicked: {
                        bankStack.pop()
                    }
                }
            }

            // Borrow page
            Component {
                id: borrowPage
                BorrowPage {
                    onBackArrowClicked: {
                        bankStack.pop()
                    }
                }
            }

            Component {
                id: depositOrderPage
                DepositOrderPage {
                    onBackArrowClicked: {
                        bankStack.pop()
                    }
                }
            }

            Component {
                id: borrowOrderPage
                BorrowOrderPage {
                    onBackArrowClicked: {
                        bankStack.pop()
                    }
                }
            }

            // Password page
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
            SetPasswordPage {
                id: setPasswordPage
                onBackArrowClicked: {
                    showCreatePage(false)
                }
                onCreateClicked: {
                    createStack.push(getMnemonic)
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
            ImportPage {
                id: importPage
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
