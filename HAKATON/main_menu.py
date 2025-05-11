import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QCheckBox,
    QMessageBox, QComboBox, QDialog, QLineEdit, QHBoxLayout, QRadioButton, QButtonGroup
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Параметри")
        self.setGeometry(300, 300, 350, 250)

        self.layout = QVBoxLayout()

        
        self.theme_label = QLabel("Тема інтерфейса:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Світла", "Сіра", "Темна"])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        self.layout.addWidget(self.theme_label)
        self.layout.addWidget(self.theme_combo)

        
        self.brightness_label = QLabel("Яскравість екрану (0-100):")
        self.brightness_input = QLineEdit()
        self.brightness_input.setPlaceholderText("Наприклад, 75")
        self.layout.addWidget(self.brightness_label)
        self.layout.addWidget(self.brightness_input)

        
        self.control_label = QLabel("Управління:")
        self.wasd_radio = QRadioButton("Клавіши W, A, S, D")
        self.arrows_radio = QRadioButton("Стрілочки ← ↑ ↓ →")
        self.wasd_radio.setChecked(True)
        self.control_group = QButtonGroup()
        self.control_group.addButton(self.wasd_radio)
        self.control_group.addButton(self.arrows_radio)

        self.layout.addWidget(self.control_label)
        self.layout.addWidget(self.wasd_radio)
        self.layout.addWidget(self.arrows_radio)

        
        self.save_button = QPushButton("Зберегти параметри")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        
        self.themes = {
            "Світла": "background-color: white; color: black;",
            "Сіра": "background-color: #aaaaaa; color: black;",
            "Теемна": "background-color: black; color: white;"
        }

    def change_theme(self, theme_name):
        if theme_name in self.themes:
            self.setStyleSheet(self.themes[theme_name])

    def save_settings(self):
        theme = self.theme_combo.currentText()
        brightness = self.brightness_input.text()
        control = "WASD" if self.wasd_radio.isChecked() else "Arrows"

        
        try:
            brightness_value = int(brightness)
            if not (0 <= brightness_value <= 100):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Помилка", "Введіть коректне значення яскравості від 0 до 100.")
            return

        
        QMessageBox.information(
            self, "Параметри збережені",
            f"🎨 Тема: {theme}\n💡 Яскравість: {brightness}%\n🎮 Управління: {control}"
        )
        self.accept()


class WarningWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Попередження")
        self.setGeometry(200, 200, 400, 250)

        
        self.sound_enabled = True

        
        layout = QVBoxLayout()
        
        self.label = QLabel("⚠️ Гра містить скримери та гучні звуки!")
        self.label.setFont(QFont("Arial", 12))
        layout.addWidget(self.label)

        
        self.sound_checkbox = QCheckBox("Відключити звук")
        self.sound_checkbox.stateChanged.connect(self.toggle_sound)
        layout.addWidget(self.sound_checkbox)

        
        self.play_button = QPushButton("Старт")
        self.play_button.clicked.connect(self.start_game)
        layout.addWidget(self.play_button)

        
        self.settings_button = QPushButton("Параметри")
        self.settings_button.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_button)

        
        self.exit_button = QPushButton("Вийти")
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def toggle_sound(self, state):
        self.sound_enabled = not bool(state)
        print("Звук вимкнен" if not self.sound_enabled else "Звук увімкнено")

    def start_game(self):
        subprocess.Popen(["python", "game.py"])
        self.close()


    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WarningWindow()
    window.show()
    sys.exit(app.exec())
