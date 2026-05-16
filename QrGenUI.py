import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QCheckBox,
    QSizePolicy,
    QGraphicsDropShadowEffect,
)


class QRGenerator(QMainWindow):

    def __init__(self):
        super().__init__()

        self.bg_color = "#FFFFFF"
        self.center_color = "#000000"
        self.edge_color = "#000000"

        self.initUI()

    # =========================================================
    # MAIN UI
    # =========================================================

    def initUI(self):

        self.setWindowTitle("QR Code Generator")

        self.setFixedSize(1350, 960)

        self.setStyleSheet("""
        QMainWindow {
            background-color: #f4f7fb;
        }

        QLabel {
            color: #0f172a;
            font-size: 14px;
        }

        QTextEdit {
            background-color: white;
            border: 2px solid #e2e8f0;
            border-radius: 18px;
            padding: 14px;
            font-size: 14px;
            color: #0f172a;
        }

        QTextEdit:focus {
            border: 2px solid #2563eb;
        }

        QPushButton {
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 16px;
            padding: 12px;
            font-size: 15px;
            font-weight: 700;
        }

        QPushButton:hover {
            background-color: #1d4ed8;
        }

        QPushButton:pressed {
            background-color: #1e40af;
        }

        QCheckBox {
            font-size: 14px;
            spacing: 8px;
        }

        QScrollBar:vertical {
            border: none;
            background: transparent;
            width: 10px;
            margin: 0px;
        }

        QScrollBar::handle:vertical {
            background: #cbd5e1;
            border-radius: 5px;
            min-height: 25px;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }
        """)

        # =====================================================
        # CENTRAL WIDGET
        # =====================================================

        centralWidget = QWidget()

        self.setCentralWidget(centralWidget)

        self.mainLayout = QHBoxLayout(centralWidget)

        self.mainLayout.setSpacing(25)

        self.mainLayout.setContentsMargins(40, 40, 40, 40)

        # =====================================================
        # LEFT SIDEBAR
        # =====================================================

        self.sidebar = QFrame()

        self.sidebar.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Expanding
        )

        self.sidebar.setMinimumWidth(370)

        self.sidebar.setMaximumWidth(430)

        self.sidebar.setStyleSheet("""
        QFrame {
            background-color: white;
            border-radius: 26px;
            border: none;
        }
        """)

        self.addShadow(self.sidebar)

        self.sidebarLayout = QVBoxLayout(self.sidebar)

        self.sidebarLayout.setContentsMargins(
            32,
            32,
            32,
            32
        )

        self.sidebarLayout.setSpacing(22)

        # =====================================================
        # TITLE
        # =====================================================

        title = QLabel("⚡QR Code Settings")

        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("""
        font-size: 35px;
        font-weight: 795;
        color: #0f172a;
        """)
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.sidebarLayout.addWidget(title, alignment=Qt.AlignLeft)

        # =====================================================
        # QR TEXT
        # =====================================================

        qrLabel = QLabel("QR Code Text")

        qrLabel.setStyleSheet("""
        font-size: 16px;
        font-weight: 700;
        margin-top: 6px;
        """)

        self.sidebarLayout.addWidget(qrLabel)

        self.textEdit = QTextEdit()

        self.textEdit.setPlaceholderText(
            "Enter text or URL for QR generation..."
        )

        self.textEdit.setMinimumHeight(140)

        self.textEdit.setMaximumHeight(220)

        self.textEdit.setStyleSheet("""
        QTextEdit {
            background-color: white;
            border: 2px solid #e2e8f0;
            border-radius: 18px;
            padding: 14px;
            font-size: 14px;
            color: #0f172a;
        }

        QTextEdit:focus {
            border: 2px solid #2563eb;
        }
        """)

        self.textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.sidebarLayout.addWidget(self.textEdit)

        # =====================================================
        # CHECKBOX
        # =====================================================

        self.roundedCheck = QCheckBox(
            "Rounded Modules"
        )

        self.roundedCheck.setChecked(True)

        self.sidebarLayout.addWidget(
            self.roundedCheck
        )

        # =====================================================
        # COLOR SECTION
        # =====================================================

        colorTitle = QLabel("🎨 Color Scheme")

        colorTitle.setStyleSheet("""
        font-size: 24px;
        font-weight: 800;
        margin-top: 8px;
        """)

        self.sidebarLayout.addWidget(colorTitle)

        # BACKGROUND COLOR

        self.bgButton = self.createColorRow(
            "Background Color",
            self.bg_color,
            None
        )

        self.sidebarLayout.addWidget(
            self.bgButton["widget"]
        )

        # CENTER COLOR

        self.centerButton = self.createColorRow(
            "Center Color",
            self.center_color,
            None
        )

        self.sidebarLayout.addWidget(
            self.centerButton["widget"]
        )

        # EDGE COLOR

        self.edgeButton = self.createColorRow(
            "Edge Color",
            self.edge_color,
            None
        )

        self.sidebarLayout.addWidget(
            self.edgeButton["widget"]
        )

        # =====================================================
        # GENERATE BUTTON
        # =====================================================

        self.generateButton = QPushButton(
            "🚀 Generate QR Code"
        )

        self.generateButton.setMinimumHeight(66)

        self.generateButton.setCursor(
            QtGui.QCursor(Qt.PointingHandCursor)
        )

        self.sidebarLayout.addWidget(
            self.generateButton
        )

        # =====================================================
        # INFO CARD
        # =====================================================

        infoCard = QFrame()

        infoCard.setStyleSheet("""
        QFrame {
            background-color: transparent;
            border: 2px solid #b3d9ff;
            border-radius: 16px;
        }
        """)

        infoLayout = QHBoxLayout(infoCard)

        infoLayout.setContentsMargins(
            16,
            16,
            16,
            16
        )

        infoLayout.setSpacing(12)

        infoIcon = QLabel("ℹ")

        infoIcon.setStyleSheet("""
        color: #2563eb;
        font-size: 20px;
        font-weight: 800;
        border-radius: 12px;
        border: 2px solid #2563eb;
        """)

        infoIcon.setFixedWidth(24)

        infoLayout.addWidget(infoIcon, alignment=Qt.AlignTop)

        infoLabel = QLabel(
            "Enter QR text, customize colors, and click Generate to create your QR code."
        )

        infoLabel.setWordWrap(True)

        infoLabel.setStyleSheet("""
        color: #2563eb;
        font-size: 13px;
        font-weight: 500;
        border: none;
        background-color: transparent;
        """)

        infoLayout.addWidget(infoLabel)

        self.sidebarLayout.addWidget(infoCard)

        self.sidebarLayout.addStretch()

        # =====================================================
        # RIGHT PREVIEW PANEL
        # =====================================================

        self.previewCard = QFrame()

        self.previewCard.setStyleSheet("""
        QFrame {
            background-color: white;
            border-radius: 26px;
        }
        """)

        self.addShadow(self.previewCard)

        self.previewCard.setFixedWidth(760)
        self.previewCard.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Expanding
        )

        self.previewLayout = QVBoxLayout(
            self.previewCard
        )

        self.previewLayout.setContentsMargins(
            36,
            36,
            36,
            36
        )

        self.previewLayout.setSpacing(18)

        # PREVIEW TITLE

        previewTitle = QLabel(
            "👁️ Preview"
        )

        previewTitle.setAlignment(Qt.AlignLeft)
        previewTitle.setStyleSheet("""
        font-size: 32px;
        font-weight: 800;
        """)
        previewTitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.previewLayout.addWidget(
            previewTitle,
            alignment=Qt.AlignLeft
        )

        # =====================================================
        # PREVIEW CONTAINER
        # =====================================================

        self.previewContainer = QWidget()
        self.previewContainer.setFixedWidth(700)
        self.previewContainer.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed
        )

        self.previewContainerLayout = QVBoxLayout(
            self.previewContainer
        )

        self.previewContainerLayout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.previewWrapper = QWidget()

        self.previewWrapperLayout = QHBoxLayout(
            self.previewWrapper
        )

        self.previewWrapperLayout.addStretch()

        self.preview = QLabel()

        self.preview.setFixedSize(
            620,
            620
        )

        self.preview.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed
        )

        self.preview.setAlignment(Qt.AlignCenter)

        self.preview.setStyleSheet("""
        QLabel {
            background-color: white;
            border: 3px dashed #cbd5e1;
            border-radius: 20px;
            color: #9ca3af;
            font-size: 16px;
            font-weight: 500;
        }
        """)

        self.preview.setText("Your QR Code will appear here!\nEnter text and click Generate to see your QR Code preview!")

        self.preview.setWordWrap(True)

        self.previewWrapperLayout.addWidget(
            self.preview
        )

        self.previewWrapperLayout.addStretch()

        self.previewContainerLayout.addWidget(
            self.previewWrapper
        )

        self.previewContainerLayout.addStretch()

        self.previewLayout.addWidget(
            self.previewContainer
        )

        # =====================================================
        # ADD TO MAIN LAYOUT
        # =====================================================

        self.mainLayout.addWidget(
            self.sidebar,
            32
        )

        self.mainLayout.addWidget(
            self.previewCard,
            68
        )

    # =========================================================
    # SHADOW
    # =========================================================

    def addShadow(self, widget):

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(45)

        shadow.setXOffset(0)

        shadow.setYOffset(8)

        shadow.setColor(
            QColor(0, 0, 0, 35)
        )

        widget.setGraphicsEffect(
            shadow
        )

    # =========================================================
    # COLOR ROW
    # =========================================================

    def createColorRow(
        self,
        label_text,
        color,
        callback
    ):

        container = QWidget()

        layout = QHBoxLayout(container)

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(14)

        label = QLabel(label_text)

        label.setMinimumWidth(150)

        button = QPushButton(color)

        button.setCursor(
            QtGui.QCursor(
                Qt.PointingHandCursor
            )
        )

        button.setMinimumHeight(56)

        button.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        textColor = (
            "#000000"
            if color.upper() == "#FFFFFF"
            else "#FFFFFF"
        )

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

        if callback:
            button.clicked.connect(callback)

        layout.addWidget(label)

        layout.addWidget(button)

        return {
            "widget": container,
            "button": button
        }