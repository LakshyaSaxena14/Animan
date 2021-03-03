import sys
from PySide2.QtCore import Qt, QUrl
from PySide2.QtWidgets import QDialog, QWidget, QApplication, QToolButton, QLabel, QHBoxLayout, QFrame, QVBoxLayout, \
    QSizePolicy, QPushButton, QStackedWidget
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtGui import QIcon, QPalette


class TitleBar(QDialog):
    def __init__(self):
        super(TitleBar, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        css = """
        QWidget{
            Background: #000000;
            color:white;
            font:12px bold;
            font-weight:bold;
            height: 11px;
        }
        QDialog{
            background-color: #000000;
            font-size:12px;
            color: black;

        }
        QToolButton{
            Background:#000000;
            font-size:11px;
        }
        QToolButton:hover{
            Background: #ffffff;
            font-size:12px;
        }
        """
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Highlight)
        self.setStyleSheet(css)

        self.minimize = QToolButton(self)
        self.minimize.setIcon(QIcon('img\\min.png'))
        self.minimize.setStyleSheet("QToolButton:hover{"
                                    "Background: #101010;"
                                    "font-size:12px}")

        self.maximize = QToolButton(self)
        self.maximize.setIcon(QIcon('img\\max.png'))
        self.maximize.setStyleSheet("QToolButton:hover{"
                                    "Background: #101010;"
                                    "font-size:12px}")

        close = QToolButton(self)
        close.setIcon(QIcon('img\\close.png'))
        close.setStyleSheet("QToolButton:hover{"
                            "Background: #ED1136;"
                            "font-size:12px}")

        self.minimize.setMinimumHeight(10)
        close.setMinimumHeight(10)
        self.maximize.setMinimumHeight(10)

        label = QLabel(self)
        label.setText("Anime")
        self.setWindowTitle("Anime")

        hbox = QHBoxLayout(self)
        hbox.addWidget(label)
        hbox.addWidget(self.minimize)
        hbox.addWidget(self.maximize)
        hbox.addWidget(close)

        hbox.insertStretch(1, 500)
        hbox.setSpacing(0)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.maxNormal = False
        close.clicked.connect(self.close)
        self.minimize.clicked.connect(self.showSmall)
        self.maximize.clicked.connect(self.showMaxRestore)

    def showSmall(self):
        box.showMinimized()

    def showMaxRestore(self):
        if self.maxNormal:
            box.showNormal()
            self.maxNormal = False
            self.maximize.setIcon(QIcon('img\\max.png'))
            print('1')
        else:
            box.showMaximized()
            self.maxNormal = True
            print('2')
            self.maximize.setIcon(QIcon('img\\max2.png'))

    def close(self):
        sys.exit()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            box.moving = True
            box.offset = event.pos()

    def mouseMoveEvent(self, event):
        if box.moving: box.move(event.globalPos() - box.offset)


class Anime(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        self.m_mouse_down = False
        self.setFrameShape(QFrame.StyledPanel)

        css = """
        QFrame{
            Background:  #212121;
            color:white;
            font: 12pt "Roboto";
            font-weight:bold;
            }
        """
        self.setStyleSheet(css)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)

        self.m_titleBar = TitleBar()
        self.m_content = QWidget(self)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.m_titleBar)
        vbox.setMargin(0)
        vbox.setSpacing(0)

        layout = QVBoxLayout(self)
        layout.addWidget(self.m_content)
        layout.setMargin(5)
        layout.setSpacing(0)
        vbox.addLayout(layout)
        self.widgets()

    def contentWidget(self):
        return self.m_content

    def titleBar(self):
        return self.m_titleBar

    def mousePressEvent(self, event):
        self.m_old_pos = event.pos()
        self.m_mouse_down = event.button() == Qt.LeftButton

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()

    def mouseReleaseEvent(self, event):
        m_mouse_down = False

    def widgets(self):
        self.combined_hor_layout = QHBoxLayout(self.contentWidget())
        self.combined_hor_layout.setMargin(0)

        ################################################################################################################
        # on the left
        ################################################################################################################

        self.option_layout = QVBoxLayout(self.contentWidget())

        self.download_anime = QPushButton(self)
        self.manga = QPushButton(self)

        self.left_button_properties()

        self.option_layout.addWidget(self.download_anime, stretch=0)
        self.option_layout.addWidget(self.manga, stretch=0)
        self.option_layout.addStretch()
        self.option_layout.setSpacing(10)

        ################################################################################################################
        # on the right
        ################################################################################################################

        self.vertical_right_layout = QVBoxLayout(self.contentWidget())
        self.vertical_right_layout.setMargin(1)

        self.stack = QStackedWidget(self)

        self.page_1 = QWidget()
        self.page_2 = QWidget()

        self.stack_details()

        self.stack.addWidget(self.page_1)
        self.stack.addWidget(self.page_2)

        self.stack.setCurrentWidget(self.page_1)

        self.vertical_right_layout.addWidget(self.stack)

        ################################################################################################################

        self.combined_hor_layout.addLayout(self.option_layout)
        self.combined_hor_layout.addLayout(self.vertical_right_layout)

    def left_button_properties(self):
        self.button_css = '''QPushButton {color: #ffffff; 
        background-color: #212121; 
        border: 0px solid; 
        font:13px \"Roboto\";}
        
        QPushButton:hover {background-color: rgb(85, 170, 255);}'''

        self.download_anime.setText("Download Anime")
        self.download_anime.setStyleSheet(self.button_css)
        self.download_anime.setMinimumHeight(40)
        self.download_anime.setCursor(Qt.PointingHandCursor)
        self.download_anime.setFixedWidth(120)
        self.download_anime.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_1))

        self.manga.setText("Read mangas")
        self.manga.setStyleSheet(self.button_css)
        self.manga.setMinimumHeight(40)
        self.manga.setCursor(Qt.PointingHandCursor)
        self.manga.setFixedWidth(120)
        self.manga.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_2))

    def stack_details(self):
        page_css = '''background-color: #2D2D2D; color: #ffffff;'''

        ################################################################################################################
        # page1
        ################################################################################################################
        self.page_1.setStyleSheet(page_css)
        self.page_1_layout = QVBoxLayout(self)

        self.anime = QWebEngineView()
        self.anime.setUrl(QUrl("https://animixplay.to"))

        self.page_1_layout.addWidget(self.anime)

        self.page_1.setLayout(self.page_1_layout)

        ################################################################################################################
        # page 2
        ################################################################################################################
        self.page_2.setStyleSheet(page_css)
        self.page_2_layout = QVBoxLayout(self)

        self.manga_read = QWebEngineView()
        self.manga_read.setUrl(QUrl("https://manganelo.com"))

        self.page_2_layout.addWidget(self.manga_read)

        self.page_2.setLayout(self.page_2_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    box = Anime()
    # box.move(60, 60)
    box.showFullScreen()
    box.show()
    app.exec_()
