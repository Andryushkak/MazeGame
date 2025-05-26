import sys
import os
import sqlite3
from datetime import datetime
import csv

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QComboBox,
    QLabel, QPushButton, QCheckBox, QMessageBox, QHBoxLayout,
    QTextEdit, QSpinBox, QFrame, QInputDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from app.coffee.factory import CoffeeFactory
from app.coffee.decorators import Milk, Chocolate, Syrup
from app.order.order import Order
from app.order.observer import Customer

class CoffeeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("☕ Coffee Order & Inventory System")
        self.setGeometry(300, 100, 700, 600)

        self.language = "en"
        self.translations = {
            "en": {
                "title": "☕ Coffee Management Dashboard",
                "select_coffee": "Select your coffee:",
                "quantity": "Quantity:",
                "milk": "Add Milk",
                "chocolate": "Add Chocolate",
                "syrup": "Add Syrup",
                "order": "🛒 Order Coffee",
                "refill": "➕ Refill Ingredients",
                "report": "📊 Show Report",
                "export": "💾 Export Report to CSV",
                "lang": "🌐 Switch to Ukrainian",
                "inv_label": "📦 Inventory:",
                "sales": "💰 Sales",
                "exp": "💸 Expenses",
                "not_enough": "Not enough {}!",
                "order_success": "✅ Order complete! Earned ${:.2f}",
                "restocked": "✅ Ingredients restocked.",
                "report_title": "📅 Report from {} to {}:",
                "exported": "Report exported to sales_report.csv!",
            },
            "uk": {
                "title": "☕ Панель керування кав'ярнею",
                "select_coffee": "Виберіть каву:",
                "quantity": "Кількість:",
                "milk": "Додати молоко",
                "chocolate": "Додати шоколад",
                "syrup": "Додати сироп",
                "order": "🛒 Замовити каву",
                "refill": "➕ Поповнити інгредієнти",
                "report": "📊 Показати звіт",
                "export": "💾 Експортувати звіт у CSV",
                "lang": "🌐 Switch to English",
                "inv_label": "📦 Склад:",
                "sales": "💰 Продажі",
                "exp": "💸 Витрати",
                "not_enough": "Недостатньо {}!",
                "order_success": "✅ Замовлення виконано! Зароблено ${:.2f}",
                "restocked": "✅ Інгредієнти поповнено.",
                "report_title": "📅 Звіт з {} по {}:",
                "exported": "Звіт збережено у sales_report.csv!",
            }
        }

        self.factory = CoffeeFactory()
        self.order = Order()
        self.customer = Customer("Ivan")
        self.order.add_observer(self.customer)

        self.ingredients = {
            "coffee": 1000,
            "milk": 2000,
            "chocolate": 1000
        }

        self.costs = {
            "coffee": 0.05,
            "milk": 0.02,
            "chocolate": 0.04
        }

        self.sales = 0.0
        self.expenses = 0.0

        self.init_db()
        self.init_ui()

    def tr(self, key):
        return self.translations[self.language][key]

    def init_db(self):
        self.conn = sqlite3.connect("orders.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, cost REAL, date TEXT)"
        )
        self.conn.commit()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #ffffff;
                font-family: Segoe UI;
                font-size: 14px;
            }
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QTextEdit, QComboBox, QSpinBox, QCheckBox {
                background-color: #2e2e3f;
                color: white;
                border-radius: 4px;
                padding: 4px;
            }
        """)

        layout = QVBoxLayout()
        self.title = QLabel(self.tr("title"))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(self.title)

        self.label = QLabel(self.tr("select_coffee"))
        layout.addWidget(self.label)

        self.coffee_combo = QComboBox()
        self.coffee_combo.addItems(["Espresso", "Latte", "Cappuccino"])
        layout.addWidget(self.coffee_combo)

        layout.addWidget(QLabel(self.tr("quantity")))
        self.amount = QSpinBox()
        self.amount.setMinimum(1)
        self.amount.setValue(1)
        layout.addWidget(self.amount)

        self.chk_milk = QCheckBox(self.tr("milk"))
        self.chk_chocolate = QCheckBox(self.tr("chocolate"))
        self.chk_syrup = QCheckBox(self.tr("syrup"))
        layout.addWidget(self.chk_milk)
        layout.addWidget(self.chk_chocolate)
        layout.addWidget(self.chk_syrup)

        self.order_btn = QPushButton(self.tr("order"))
        self.order_btn.clicked.connect(self.process_order)
        layout.addWidget(self.order_btn)

        self.buy_btn = QPushButton(self.tr("refill"))
        self.buy_btn.clicked.connect(self.refill_ingredients)
        layout.addWidget(self.buy_btn)

        self.report_btn = QPushButton(self.tr("report"))
        self.report_btn.clicked.connect(self.show_report)
        layout.addWidget(self.report_btn)

        self.export_btn = QPushButton(self.tr("export"))
        self.export_btn.clicked.connect(self.export_report)
        layout.addWidget(self.export_btn)

        self.lang_btn = QPushButton(self.tr("lang"))
        self.lang_btn.clicked.connect(self.switch_language)
        layout.addWidget(self.lang_btn)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        self.history_box = QTextEdit()
        self.history_box.setReadOnly(True)
        layout.addWidget(self.history_box)

        self.setLayout(layout)

    def process_order(self):
        coffee_type = self.coffee_combo.currentText()
        quantity = self.amount.value()
        base_cost = 0

        if self.ingredients["coffee"] < 100 * quantity:
            QMessageBox.warning(self, "!", self.tr("not_enough").format("coffee"))
            return

        self.ingredients["coffee"] -= 100 * quantity
        base_cost += 100 * quantity * self.costs["coffee"]

        if self.chk_milk.isChecked():
            if self.ingredients["milk"] < 50 * quantity:
                QMessageBox.warning(self, "!", self.tr("not_enough").format("milk"))
                return
            self.ingredients["milk"] -= 50 * quantity
            base_cost += 50 * quantity * self.costs["milk"]

        if self.chk_chocolate.isChecked():
            if self.ingredients["chocolate"] < 30 * quantity:
                QMessageBox.warning(self, "!", self.tr("not_enough").format("chocolate"))
                return
            self.ingredients["chocolate"] -= 30 * quantity
            base_cost += 30 * quantity * self.costs["chocolate"]

        coffee = self.factory.create_coffee(coffee_type)
        if self.chk_milk.isChecked(): coffee = Milk(coffee)
        if self.chk_chocolate.isChecked(): coffee = Chocolate(coffee)
        if self.chk_syrup.isChecked(): coffee = Syrup(coffee)

        total = coffee.cost() * quantity
        profit = total - base_cost
        self.sales += total

        self.order.set_status("Ready")
        date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("INSERT INTO orders (description, cost, date) VALUES (?, ?, ?)", 
                            (coffee.get_description(), total, date))
        self.conn.commit()

        self.result_label.setText(self.tr("order_success").format(profit))
        self.show_inventory()

    def refill_ingredients(self):
        for item in self.ingredients:
            qty, ok = QInputDialog.getInt(self, self.tr("refill"), f"{item}:")
            if ok:
                self.ingredients[item] += qty
                self.expenses += qty * self.costs[item]
        self.result_label.setText(self.tr("restocked"))
        self.show_inventory()

    def show_inventory(self):
        inv = "\n".join([f"{k.capitalize()}: {v}" for k, v in self.ingredients.items()])
        self.history_box.setText(f"{self.tr('inv_label')}\n{inv}\n\n{self.tr('sales')}: ${self.sales:.2f}\n{self.tr('exp')}: ${self.expenses:.2f}")

    def show_report(self):
        df, ok1 = QInputDialog.getText(self, "From", "YYYY-MM-DD:")
        dt, ok2 = QInputDialog.getText(self, "To", "YYYY-MM-DD:")
        if ok1 and ok2:
            self.cursor.execute("SELECT * FROM orders WHERE date BETWEEN ? AND ?", (df, dt))
            rows = self.cursor.fetchall()
            report = "\n".join([f"{desc} - ${cost:.2f} ({d})" for _, desc, cost, d in rows])
            self.history_box.setText(f"{self.tr('report_title').format(df, dt)}\n{report}")

    def export_report(self):
        self.cursor.execute("SELECT * FROM orders")
        rows = self.cursor.fetchall()
        with open("sales_report.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Description", "Cost", "Date"])
            writer.writerows(rows)
        QMessageBox.information(self, "✓", self.tr("exported"))

    def switch_language(self):
        self.language = "uk" if self.language == "en" else "en"
        self.title.setText(self.tr("title"))
        self.label.setText(self.tr("select_coffee"))
        self.chk_milk.setText(self.tr("milk"))
        self.chk_chocolate.setText(self.tr("chocolate"))
        self.chk_syrup.setText(self.tr("syrup"))
        self.order_btn.setText(self.tr("order"))
        self.buy_btn.setText(self.tr("refill"))
        self.report_btn.setText(self.tr("report"))
        self.export_btn.setText(self.tr("export"))
        self.lang_btn.setText(self.tr("lang"))
        self.show_inventory()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec_())
