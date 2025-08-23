import sys
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QRect,QAbstractAnimation,QProcess
from PyQt6.QtGui import QFont, QPixmap, QPainter ,QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QToolButton,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
)
import os
import subprocess
import threading

os.environ["QSG_RHI_BACKEND"] = "opengl"
os.environ["QSG_RHI_PREFER_SOFTWARE_RENDERER"] = "1"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-gpu-rasterization --enable-native-gpu-memory-buffers --num-raster-threads=4"
os.environ["QSG_INFO"] = "1"


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

app = QApplication(sys.argv)
texts = [
    "inject",
    "checking connection.",
    "download DLL..",
    "download DLL...",
    "download DLL....",
    "LOL stupid hacker q(≧▽≦q)"
]

# Main frameless window with transparency
window = QWidget()
window.setWindowTitle("Horion Injector")
window.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
ico_path=resource_path("horion.ico")
window.setWindowIcon(QIcon(ico_path))
window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
window.resize(500, 300)

# Inner widget
inner = QWidget(window)
inner.setGeometry(0, 0, 500, 300)
inner.setStyleSheet("""
    background-color: #121212;
    border-radius: 12px;
""")

# Photo view
photo_view = QGraphicsView(inner)
photo_view.setGeometry(98, 25, 305, 170)
photo_view.setStyleSheet("background-color: transparent; border: none;")
photo_view.setRenderHint(QPainter.RenderHint.Antialiasing)
photo_view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
scene = QGraphicsScene()
photo_view.setScene(scene)
banner_path=resource_path('horion-banner.png')
banner_photo = QPixmap(banner_path)
pixmap_item = QGraphicsPixmapItem(banner_photo)
scene.addItem(pixmap_item)
photo_view.fitInView(pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)

# Version label
version_font = QFont("Bahnschrift", 9)
version_font.setBold(True)
version_label = QLabel("v1.1.2", inner)
version_label.setFont(version_font)
version_label.setStyleSheet("color: #ffffff;")
version_label.move(9, inner.height() - 23)

# Close button
close_btn = QToolButton(inner)
close_btn.setText("✕")
close_btn.setFont(QFont("ExtraBold", 16))
close_btn.setStyleSheet("""
    QToolButton {
        color: #ffffff;
        background: transparent;
        border: none;
    }
    QToolButton:hover {
        color: #ff7f50;
    }
""")
close_btn.adjustSize()
close_btn.move(460, 5)
close_btn.clicked.connect(window.close)

# Inject button 
inj_font = QFont("Bahnschrift", 13)
inj_font.setBold(True)
inj_btn = QPushButton("inject", inner)
inj_btn.setFont(inj_font)
inj_btn.setStyleSheet("""
    QPushButton {
        background-color: #489b5e;
        color: white;
        border: none;
        border-radius: 10px;
    }
    QPushButton:pressed {
        background-color: #3f8f52;
    }
""")
inj_btn.setMinimumSize(250, 60)
inj_btn.move(125, 190)

# Enable window dragging
old_pos = None
def mousePressEvent(event):
    global old_pos
    if event.button() == Qt.MouseButton.LeftButton:
        old_pos = event.globalPosition().toPoint()

def mouseMoveEvent(event):
    global old_pos
    if old_pos:
        delta = event.globalPosition().toPoint() - old_pos
        window.move(window.pos() + delta)
        old_pos = event.globalPosition().toPoint()

# Animation: one QPropertyAnimation reused, but we always stop() before reuse
anim = QPropertyAnimation(inj_btn, b"geometry")
anim.setDuration(150)
anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
anim.setLoopCount(1)

orig_geo = inj_btn.geometry()

def on_anim_finished():
    try:
        end = anim.endValue()
        if isinstance(end, QRect):
            inj_btn.setGeometry(end)
    except Exception:
        pass

anim.finished.connect(on_anim_finished)

def play_video(video_path):
    while True:
        proc = QProcess()
        proc.startDetached("explorer", [video_path])

        
def on_hover_enter(event):

    geo = inj_btn.geometry()
    w, h = geo.width(), geo.height()
    dw, dh = int(w * 0.05), int(h * 0.05)
    scaled = QRect(geo.x() - dw//2, geo.y() - dh//2, w + dw, h + dh)

    anim.setStartValue(geo)
    anim.setEndValue(scaled)
    anim.start()
    return QPushButton.enterEvent(inj_btn, event)

def on_hover_leave(event):
    if anim.state() == QAbstractAnimation.State.Running:
        anim.stop()

    geo = inj_btn.geometry()
    anim.setStartValue(geo)
    anim.setEndValue(orig_geo)
    anim.start()
    return QPushButton.leaveEvent(inj_btn, event)

# Text cycling timer
text_index = 0
timer = QTimer()
def update_text():
    global text_index
    text_index += 1
    if text_index >= len(texts):
        timer.stop()
        inj_btn.setEnabled(True)
        text_index = 0
        inj_btn.setText(texts[0])
        return
    inj_btn.setText(texts[text_index])

def on_click():
    global text_index
    inj_btn.setEnabled(False)
    text_index = 0
    inj_btn.setText(texts[text_index])
    timer.timeout.connect(update_text)
    timer.start(1000)
    
inj_btn.enterEvent = on_hover_enter
inj_btn.leaveEvent = on_hover_leave
inj_btn.clicked.connect(on_click)

window.mousePressEvent = mousePressEvent
window.mouseMoveEvent = mouseMoveEvent

window.show()
app.exec()
good_video = resource_path("trailer.mp4")
play_video(good_video)