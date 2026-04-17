import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QComboBox, QLineEdit, QLabel, 
                             QPushButton, QFrame, QGridLayout)
from PyQt6.QtCore import Qt

class SchedulerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OS Scheduler Simulator - GUI Squad")
        self.setMinimumSize(1000, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.left_panel = QVBoxLayout()
        self.main_layout.addLayout(self.left_panel, 1)

        self.setup_header()
        self.setup_adaptive_inputs()
        self.setup_mode_toggle()
        
        self.left_panel.addStretch()

        self.right_panel = QVBoxLayout()
        self.viz_placeholder = QFrame()
        self.viz_placeholder.setFrameShape(QFrame.Shape.StyledPanel)
        self.viz_placeholder.setStyleSheet("background-color: #2b2b2b; border-radius: 10px;")
        
        placeholder_text = QLabel("Live Gantt Chart & Tables Area\n(Member 5's Domain)", self.viz_placeholder)
        placeholder_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder_text.setStyleSheet("color: #666; font-size: 18px;")
        
        self.right_panel.addWidget(placeholder_text)
        self.main_layout.addLayout(self.right_panel, 2)

    def setup_header(self):
        title = QLabel("Simulation Settings")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #3498db;")
        self.left_panel.addWidget(title)

    def setup_adaptive_inputs(self):
        grid = QGridLayout()
        
        grid.addWidget(QLabel("Algorithm:"), 0, 0)
        self.algo_box = QComboBox()
        self.algo_box.addItems([
            "FCFS", 
            "Non-Preemptive SJF", 
            "Preemptive SJF", 
            "Non-Preemptive Priority", 
            "Preemptive Priority", 
            "Round Robin"
        ])
        self.algo_box.currentTextChanged.connect(self.update_ui_state)
        grid.addWidget(self.algo_box, 0, 1)

        self.prio_label = QLabel("Priority (Lower = Higher):")
        self.prio_input = QLineEdit()
        self.prio_input.setPlaceholderText("e.g. 1")
        grid.addWidget(self.prio_label, 1, 0)
        grid.addWidget(self.prio_input, 1, 1)

        self.quantum_label = QLabel("Time Quantum:")
        self.quantum_input = QLineEdit()
        self.quantum_input.setPlaceholderText("e.g. 2")
        grid.addWidget(self.quantum_label, 2, 0)
        grid.addWidget(self.quantum_input, 2, 1)

        self.left_panel.addLayout(grid)
        self.update_ui_state()

    def update_ui_state(self):
        algo = self.algo_box.currentText()
        
        show_prio = "Priority" in algo
        self.prio_label.setVisible(show_prio)
        self.prio_input.setVisible(show_prio)

        show_quantum = (algo == "Round Robin")
        self.quantum_label.setVisible(show_quantum)
        self.quantum_input.setVisible(show_quantum)

    def setup_mode_toggle(self):
        self.left_panel.addWidget(QLabel("\nExecution Mode:"))
        self.mode_toggle = QComboBox()
        self.mode_toggle.addItems(["Static/Existing Only", "Live Scheduling (1:1 mapping)"])
        self.left_panel.addWidget(self.mode_toggle)

        self.add_btn = QPushButton("Add Process to Queue")
        self.add_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; font-weight: bold;")
        self.left_panel.addWidget(self.add_btn)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchedulerGUI()
    window.show()
    sys.exit(app.exec())
