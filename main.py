from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)
import sys
from peewee import Model, AutoField, CharField
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from models import DatabaseManager, Contact


class PhoneBookApp(QWidget):
    item_changed_connected = False

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create a tab widget to switch between "Add Contact" and "Search Contacts" tabs
        self.tabs = QTabWidget()

        # Add tabs to the widget
        self.tabs.addTab(self.create_add_tab(), "Add Contact")
        self.tabs.addTab(self.create_search_tab(), "Search Contacts")

        # Create the main layout and add the tab widget to it
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        # Set the main layout for the application window
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle("Phone Book")

        # Set the fixed size of the main window
        self.setFixedSize(650, 400)  # Width x Height
        self.show()

    def create_add_tab(self):
        # Create the "Add Contact" tab
        add_tab = QWidget()

        # Create labels and input fields for user input
        first_name_label = QLabel("First Name:")
        self.first_name_input = QLineEdit()

        last_name_label = QLabel("Last Name:")
        self.last_name_input = QLineEdit()

        phone_label = QLabel("Phone Number:")
        self.phone_input = QLineEdit()

        address_label = QLabel("Address:")
        self.address_input = QLineEdit()

        # Create a button to add a new contact
        add_button = QPushButton("Add Contact")
        add_button.clicked.connect(self.add_contact)

        # Arrange widgets vertically in a layout
        layout = QVBoxLayout()
        layout.addWidget(first_name_label)
        layout.addWidget(self.first_name_input)
        layout.addWidget(last_name_label)
        layout.addWidget(self.last_name_input)
        layout.addWidget(phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(address_label)
        layout.addWidget(self.address_input)
        layout.addWidget(add_button)

        # Set the layout for the "Add Contact" tab
        add_tab.setLayout(layout)
        return add_tab

    def create_search_tab(self):
        # Create the "Search Contacts" tab
        search_tab = QWidget()

        # Create labels, input fields, and a button for searching contacts
        first_name_label = QLabel("First Name:")
        self.first_name_search_input = QLineEdit()

        last_name_label = QLabel("Last Name:")
        self.last_name_search_input = QLineEdit()

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_contacts)

        # Create a table widget to display search results
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels(
            ["id", "First Name", "Last Name", "Phone Number", "Address", "Delete"]
        )

        # Hide the vertical header (row numbers)
        self.results_table.verticalHeader().setVisible(False)

        # Connect the itemDoubleClicked signal to a custom slot
        self.results_table.itemDoubleClicked.connect(self.item_double_clicked_slot)

        # Arrange widgets vertically and horizontally in layouts
        search_layout = QVBoxLayout()
        search_layout.addWidget(first_name_label)
        search_layout.addWidget(self.first_name_search_input)
        search_layout.addWidget(last_name_label)
        search_layout.addWidget(self.last_name_search_input)
        search_layout.addWidget(search_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.results_table)

        # Set the main layout for the "Search Contacts" tab
        search_tab.setLayout(main_layout)

        return search_tab

    def on_item_changed(self, item):
        # Get edited item row and column
        row = item.row()
        col = item.column()
        # Get edited contact.id
        id = self.results_table.item(row, 0).text()

        # Get edited item value
        new_value = item.text()

        reply = QMessageBox.question(
            self,
            "Question",
            "Do you want to update it?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        # Process the user's response
        if reply == QMessageBox.Yes:
            # Update contact in database
            updated_contact = Contact.get(Contact.id == id)
            updated_contact.first_name = self.results_table.item(row, 1).text()
            updated_contact.last_name = self.results_table.item(row, 2).text()
            updated_contact.phone_number = self.results_table.item(row, 3).text()
            updated_contact.address = self.results_table.item(row, 4).text()
            updated_contact.save()
            print("Contact Updated Successfully!")
            # Get the name of column in the table
            header_item = self.results_table.horizontalHeaderItem(col).text()
            QMessageBox.information(
                self,
                "Contact Updated",
                f"For Contact ID: {updated_contact.id}, {header_item} changed to: {new_value}",
            )
        else:
            self.search_contacts()

    def item_double_clicked_slot(self, item):
        # This slot is called when an item is double-clicked
        if item is not None:
            row = item.row()
            col = item.column()
            # print(f'Item at row {row}, column {col} double-clicked: {item.text()}')
            if col == 5:
                id = self.results_table.item(row, 0).text()
                deleted_contact = Contact.get(Contact.id == id)
                reply = QMessageBox.question(
                    self,
                    "Question",
                    "Do you want to delete it?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )
                if reply == QMessageBox.Yes:
                    deleted_contact.delete_instance()
                    self.search_contacts()
                    print("Contact Deleted Successfully!")

    def add_contact(self):
        # Add a new contact to the database based on user input
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        phone_number = self.phone_input.text()
        address = self.address_input.text()

        new_contact = Contact.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
        )
        new_contact.save()

        # Clear input fields after adding
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.phone_input.clear()
        self.address_input.clear()

    def search_contacts(self):
        if self.item_changed_connected == True:
            self.results_table.itemChanged.disconnect(self.on_item_changed)
            self.item_changed_connected = False

        # Search for contacts in the database based on user input
        first_name_search_term = self.first_name_search_input.text()
        last_name_search_term = self.last_name_search_input.text()

        # Query database for contacts matching the search terms
        contacts = Contact.select().where(
            (Contact.first_name.contains(first_name_search_term))
            & (Contact.last_name.contains(last_name_search_term))
        )

        # Display search results in the table
        self.results_table.setRowCount(0)  # Clear existing rows

        for row, contact in enumerate(contacts):
            self.results_table.insertRow(row)
            # Make contact id field uneditable
            item = QTableWidgetItem(str(contact.id))
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            item.setTextAlignment(Qt.AlignCenter)

            self.results_table.setItem(row, 0, item)
            self.results_table.setItem(row, 1, QTableWidgetItem(contact.first_name))
            self.results_table.setItem(row, 2, QTableWidgetItem(contact.last_name))
            self.results_table.setItem(row, 3, QTableWidgetItem(contact.phone_number))
            self.results_table.setItem(row, 4, QTableWidgetItem(contact.address))

            # Add a delete icon to the last column and customize it
            delete_item = QTableWidgetItem("Delete")
            delete_item.setFlags(delete_item.flags() ^ Qt.ItemIsEditable)
            delete_item.setIcon(QIcon.fromTheme("edit-delete"))
            self.results_table.setItem(row, 5, delete_item)
            delete_item.setBackground(QColor("#EA9999"))
            delete_item.setTextAlignment(Qt.AlignCenter)
            delete_item.setToolTip("This is a delete button.")

        # Connect itemChanged signal to custom slot
        self.results_table.itemChanged.connect(self.on_item_changed)
        self.item_changed_connected = True


if __name__ == "__main__":
    # Entry point of the application
    app = QApplication(sys.argv)
    phone_book_app = PhoneBookApp()
    sys.exit(app.exec_())
