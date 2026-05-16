import sys
import os
import datetime
from threading import Thread

import qrcode

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QColorDialog,
    QMessageBox,
    QSizePolicy,
)

from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

from QrGenUI import QRGenerator


class Window(QRGenerator):

    # =========================================================
    # SIGNALS
    # =========================================================

    error_signal = QtCore.pyqtSignal(str)
    status_signal = QtCore.pyqtSignal(str)
    preview_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.current_qr_path = None

        # =====================================================
        # STATUS LABEL
        # =====================================================

        self.statusLabel = QtWidgets.QLabel("Ready")

        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setWordWrap(True)
        self.statusLabel.setStyleSheet("""
        color: #475569;
        font-size: 14px;
        font-weight: 600;
        """)

        self.statusFrame = QtWidgets.QFrame()
        self.statusFrame.setStyleSheet("""
        QFrame {
            background-color: #f8fafc;
            border-radius: 16px;
        }
        """)

        statusLayout = QtWidgets.QHBoxLayout(self.statusFrame)
        statusLayout.setContentsMargins(16, 10, 16, 10)
        statusLayout.setSpacing(0)
        statusLayout.addWidget(self.statusLabel)

        self.previewLayout.addWidget(
            self.statusFrame
        )

        # =====================================================
        # SIGNAL CONNECTIONS
        # =====================================================

        self.error_signal.connect(self.showError)

        self.status_signal.connect(self.setStatus)

        self.preview_signal.connect(self.setPreview)

        # =====================================================
        # BUTTON CONNECTIONS
        # =====================================================

        self.bgButton["button"].clicked.connect(
            self.changeBackgroundColor
        )

        self.centerButton["button"].clicked.connect(
            self.changeCenterColor
        )

        self.edgeButton["button"].clicked.connect(
            self.changeEdgeColor
        )

        self.generateButton.clicked.connect(
            self.startQRGeneration
        )

    # =========================================================
    # BUTTON STYLE UPDATER
    # =========================================================

    def updateButtonStyle(
        self,
        button,
        color
    ):

        textColor = (
            "#000000"
            if color.upper() == "#FFFFFF"
            else "#FFFFFF"
        )

        button.setText(color)

        button.setStyleSheet(f"""
        QPushButton {{
            background-color: {color};
            color: {textColor};
            border: 2px solid #dbe2ea;
            border-radius: 16px;
            font-size: 15px;
            font-weight: 700;
        }}

        QPushButton:hover {{
            border: 2px solid #2563eb;
        }}
        """)

    # =========================================================
    # COLOR PICKERS
    # =========================================================

    def changeBackgroundColor(self):

        color = QColorDialog.getColor()

        if color.isValid():

            self.bg_color = color.name()

            self.updateButtonStyle(
                self.bgButton["button"],
                self.bg_color
            )

    def changeCenterColor(self):

        color = QColorDialog.getColor()

        if color.isValid():

            self.center_color = color.name()

            self.updateButtonStyle(
                self.centerButton["button"],
                self.center_color
            )

    def changeEdgeColor(self):

        color = QColorDialog.getColor()

        if color.isValid():

            self.edge_color = color.name()

            self.updateButtonStyle(
                self.edgeButton["button"],
                self.edge_color
            )

    # =========================================================
    # UTILITIES
    # =========================================================

    def hexToRgb(self, hexval):

        if not hexval.startswith('#') or len(hexval) != 7:

            raise ValueError(
                "Color must be a hex string like #RRGGBB"
            )

        h = hexval[1:]

        return (
            int(h[0:2], 16),
            int(h[2:4], 16),
            int(h[4:6], 16)
        )

    def generateFilename(self):

        timestamp = datetime.datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        return os.path.join(
            os.getcwd(),
            f"QRCODEGen_{timestamp}.png"
        )

    # =========================================================
    # THREAD STARTER
    # =========================================================

    def startQRGeneration(self):

        worker = Thread(
            target=self.generateQR
        )

        worker.daemon = True

        worker.start()

    # =========================================================
    # QR GENERATOR
    # =========================================================

    def generateQR(self):

        self.status_signal.emit(
            "Generating QR Code..."
        )

        try:

            text = self.textEdit.toPlainText().strip()

            if not text:

                raise ValueError(
                    "Please enter text or URL for QR generation."
                )

            qr = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=14,
                border=2
            )

            qr.add_data(text)

            qr.make(fit=True)

            background_rgb = self.hexToRgb(
                self.bg_color
            )

            center_rgb = self.hexToRgb(
                self.center_color
            )

            edge_rgb = self.hexToRgb(
                self.edge_color
            )

            qr_kwargs = {
                'image_factory': StyledPilImage,

                'color_mask': RadialGradiantColorMask(
                    back_color=background_rgb,
                    center_color=center_rgb,
                    edge_color=edge_rgb,
                ),
            }

            if self.roundedCheck.isChecked():

                qr_kwargs[
                    'module_drawer'
                ] = RoundedModuleDrawer()

            img = qr.make_image(
                **qr_kwargs
            )

            filename = self.generateFilename()

            img.save(filename)

            self.current_qr_path = filename

            self.preview_signal.emit(
                filename
            )

            self.status_signal.emit(
                f"Saved Successfully:\n{filename}"
            )

        except Exception as error:

            self.error_signal.emit(
                str(error)
            )

            self.status_signal.emit(
                "Ready"
            )

    # =========================================================
    # PREVIEW SETTER
    # =========================================================

    def setPreview(self, filename):

        pixmap = QPixmap(filename)

        if pixmap.isNull():
            return

        size = min(
            self.preview.width() - 60,
            self.preview.height() - 60
        )

        scaled = pixmap.scaled(
            size,
            size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.preview.setPixmap(
            scaled
        )

    # =========================================================
    # STATUS SETTER
    # =========================================================

    def setStatus(self, text):

        text = text.replace("\n", " — ")

        self.statusLabel.setText(
            text
        )

    # =========================================================
    # ERROR POPUP
    # =========================================================

    def showError(self, message):

        msg = QMessageBox(self)

        msg.setIcon(
            QMessageBox.Warning
        )

        msg.setWindowTitle(
            "Error"
        )

        msg.setText(message)

        msg.setStandardButtons(
            QMessageBox.Ok
        )

        msg.exec_()

# =============================================================
# MAIN APPLICATION
# =============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    icon_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "AppLogo.png"
    )

    app.setWindowIcon(QIcon(icon_path))

    window = Window()
    window.setWindowIcon(QIcon(icon_path))

    window.show()

    sys.exit(app.exec_())