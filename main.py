import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QSpinBox, QColorDialog
)
from PyQt5.QtGui import QPixmap
from processor import process_images


class ImageTextApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Text Embedder Pro")
        self.setGeometry(200, 200, 700, 500)

        self.input_folder = ""
        self.output_folder = ""
        self.font_path = ""
        self.color = (255, 0, 0)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.input_label = QLabel("Input Folder: Not selected")
        btn_input = QPushButton("Select Input Folder")
        btn_input.clicked.connect(self.select_input)

        self.output_label = QLabel("Output Folder: Not selected")
        btn_output = QPushButton("Select Output Folder")
        btn_output.clicked.connect(self.select_output)

        self.font_label = QLabel("Font: Not selected")
        btn_font = QPushButton("Select Font (.ttf)")
        btn_font.clicked.connect(self.select_font)

        self.font_size = QSpinBox()
        self.font_size.setRange(10, 200)
        self.font_size.setValue(30)

        self.pos_x = QSpinBox()
        self.pos_x.setRange(0, 2000)
        self.pos_x.setValue(50)

        self.pos_y = QSpinBox()
        self.pos_y.setRange(0, 2000)
        self.pos_y.setValue(50)

        btn_color = QPushButton("Select Color")
        btn_color.clicked.connect(self.select_color)

        btn_process = QPushButton("Process Images")
        btn_process.clicked.connect(self.run_processing)

        self.preview_label = QLabel("Preview will appear here")
        self.preview_label.setFixedHeight(200)

        layout.addWidget(self.input_label)
        layout.addWidget(btn_input)

        layout.addWidget(self.output_label)
        layout.addWidget(btn_output)

        layout.addWidget(self.font_label)
        layout.addWidget(btn_font)

        layout.addWidget(QLabel("Font Size"))
        layout.addWidget(self.font_size)

        layout.addWidget(QLabel("Position X"))
        layout.addWidget(self.pos_x)

        layout.addWidget(QLabel("Position Y"))
        layout.addWidget(self.pos_y)

        layout.addWidget(btn_color)
        layout.addWidget(btn_process)
        layout.addWidget(self.preview_label)

        self.setLayout(layout)

    def select_input(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_folder = folder
            self.input_label.setText(f"Input Folder: {folder}")
            self.load_preview()

    def select_output(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_label.setText(f"Output Folder: {folder}")

    def select_font(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Font", "", "Font Files (*.ttf)")
        if file:
            self.font_path = file
            self.font_label.setText(f"Font: {file}")

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = (color.red(), color.green(), color.blue())

    def load_preview(self):
        import os
        for file in os.listdir(self.input_folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                path = os.path.join(self.input_folder, file)
                pixmap = QPixmap(path)
                self.preview_label.setPixmap(pixmap.scaledToHeight(200))
                break

    def run_processing(self):
        if not all([self.input_folder, self.output_folder, self.font_path]):
            self.preview_label.setText("Please select all inputs!")
            return

        result = process_images(
            self.input_folder,
            self.output_folder,
            self.font_path,
            self.font_size.value(),
            self.color,
            self.pos_x.value(),
            self.pos_y.value()
        )

        self.preview_label.setText(result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageTextApp()
    window.show()
    sys.exit(app.exec_())
