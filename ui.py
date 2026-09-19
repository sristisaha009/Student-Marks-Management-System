from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import csv
from extractor import extract_student_data_from_word, append_students_to_csv
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class LoginScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager  # Store the screen_manager as an instance attribute
        self.layout = BoxLayout(orientation='vertical', spacing=30, padding=20)
        self.add_widget(self.layout)

        # Title Label
        self.layout.add_widget(Label(text="Welcome to Student Management System", font_size=20))

        # Buttons for Login Options
        self.student_button = Button(text="Login as Student", size_hint=(1, 0.2))
        self.student_button.bind(on_press=self.student_login)
        self.layout.add_widget(self.student_button)

        self.faculty_button = Button(text="Login as Faculty", size_hint=(1, 0.2))
        self.faculty_button.bind(on_press=self.faculty_login)
        self.layout.add_widget(self.faculty_button)

    def student_login(self, instance):
        self.clear_login_form()
        self.layout.add_widget(Label(text="Student Login", font_size=24))

        self.enrollment_input = self.add_input_field("Enter Enrollment Number:")
        self.password_input = self.add_input_field("Enter Password:", password=True)

        self.add_button("Login", self.validate_student_login)
        self.add_button("Back", self.reset_screen)

    def faculty_login(self, instance):
        self.clear_login_form()
        self.layout.add_widget(Label(text="Faculty Login", font_size=24))

        self.id_input = self.add_input_field("Enter Faculty ID:")
        self.password_input = self.add_input_field("Enter Password:", password=True)

        self.add_button("Login", self.validate_faculty_login)
        self.add_button("Back", self.reset_screen)

    def clear_login_form(self):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text="Welcome to Student Management System", font_size=24))

    def add_input_field(self, label_text, password=False):
        self.layout.add_widget(Label(text=label_text, font_size=20))
        input_field = TextInput(multiline=False, password=password)
        self.layout.add_widget(input_field)
        return input_field

    def add_button(self, text, on_press_callback):
        button = Button(text=text, size_hint=(1, 0.9))
        button.bind(on_press=on_press_callback)
        self.layout.add_widget(button)

    def reset_screen(self, instance):
        self.layout.clear_widgets()  # Clear all widgets
        self.__init__(screen_manager=self.screen_manager)  # Reinitialize the screen

    def validate_student_login(self, instance):
        from validity import validate_student
        enrollment = self.enrollment_input.text
        password = self.password_input.text

        try:
            student_details = validate_student(enrollment, password)
            if student_details:
                self.screen_manager.get_screen("student_detail_screen").update_details(student_details)
                self.screen_manager.current = "student_detail_screen"
            else:
                self.show_popup("Login Failed", "Invalid Credentials")
        except ImportError:
            self.show_popup("Error", "Student login module not found")

    def validate_faculty_login(self, instance):
        from validity import validate_faculty
        faculty_id = self.id_input.text
        password = self.password_input.text

        try:
            faculty_name = validate_faculty(faculty_id, password)
            if faculty_name:
                faculty_screen = self.screen_manager.get_screen("faculty_options_screen")
                faculty_screen.faculty_name = faculty_name  # Store it in FacultyOptionsScreen
                self.screen_manager.current = "faculty_options_screen"
            else:
                self.show_popup("Login Failed", "Invalid Credentials")
        except ImportError:
            self.show_popup("Error", "Faculty login module not found")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.5, 0.5))
        popup.open()

class StudentDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)

        # Label to display student details
        self.details_label = Label(
            text="",
            font_size=18,
            halign="center",  # Center-align text horizontally
            valign="middle",  # Center-align text vertically
            size_hint=(1, 0.8)  # Take up most of the screen height
        )
        self.details_label.bind(size=self.details_label.setter('text_size'))  # Ensure text respects alignment
        self.layout.add_widget(self.details_label)

        # Back Button
        back_button = Button(text="Back to Login", size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

    def update_details(self, student_details):
        """
        Updates the student details displayed in the label.
        """
        details = "\n".join([f"{key}: {value}" for key, value in student_details.items() if key not in ["Password"]])
        self.details_label.text = details

    def go_back(self, instance):
        """
        Navigates back to the login screen.
        """
        self.manager.current = "login_screen"

class FacultyOptionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)

        # Buttons for Faculty Options
        self.view_edit_button = Button(text="View and Edit", size_hint=(1, 0.2))
        self.view_edit_button.bind(on_press=self.view_and_edit)
        self.layout.add_widget(self.view_edit_button)

        self.upload_button = Button(text="Upload Word Files", size_hint=(1, 0.2))
        self.upload_button.bind(on_press=self.open_file_chooser)
        self.layout.add_widget(self.upload_button)

        # Back Button
        self.back_button = Button(text="Back to Login", size_hint=(1, 0.2))
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

    def open_file_chooser(self, instance):
        """
        Opens a file chooser dialog to select multiple Word files.
        """
        file_chooser = FileChooserListView(multiselect=True)  # Enable multiple file selection
        file_chooser.bind(on_submit=self.process_word_files)

        # Add a "Confirm" button to the file chooser
        confirm_button = Button(text="Confirm", size_hint=(1, 0.1))
        confirm_button.bind(on_press=lambda x: self.process_word_files(file_chooser, file_chooser.selection))

        # Create a layout for the file chooser and confirm button
        file_chooser_layout = BoxLayout(orientation='vertical')
        file_chooser_layout.add_widget(file_chooser)
        file_chooser_layout.add_widget(confirm_button)

        # Create a popup to display the file chooser
        popup = Popup(title="Upload Word Files", content=file_chooser_layout, size_hint=(0.9, 0.9))
        popup.open()

    def process_word_files(self, file_chooser, file_paths, *args):
        """
        Processes the selected Word files and appends student data to the CSV file.
        Also creates clean Word files (without update entries) for each student.
        """
        if file_paths:
            from generator import create_student_word_file

            success_count = 0
            for file_path in file_paths:
                if file_path.endswith(".docx"):
                    students = extract_student_data_from_word(file_path)
                    if students:
                        append_students_to_csv(students, "Student DataBase.csv")
                        success_count += 1

                        # ✅ Create clean Word file for each student
                        for student in students:
                            create_student_word_file(student)
                    else:
                        self.show_popup("Error", f"No valid student data found in {file_path}.")
                else:
                    self.show_popup("Error", f"Invalid file type: {file_path}. Please select .docx files.")

            if success_count > 0:
                self.show_popup("Success", f"Student data uploaded from {success_count} file(s).")
        else:
            self.show_popup("Error", "No files selected.")

    def view_and_edit(self, instance):
        view_edit_screen = self.manager.get_screen("view_edit_screen")
        view_edit_screen.faculty_name = getattr(self, 'faculty_name', 'Unknown')
        self.manager.current = "view_edit_screen"

    def go_back(self, instance):
        self.manager.current = "login_screen"

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.5, 0.5))
        popup.open()

class ViewEditScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.faculty_name="Anonymouus"
        self.layout = BoxLayout(orientation='horizontal', padding=20, spacing=10)
        self.add_widget(self.layout)

        # Left Side: Scrollable List of Students
        self.student_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.student_list_layout.bind(minimum_height=self.student_list_layout.setter('height'))

        self.student_scroll_view = ScrollView(size_hint=(0.5, 1))
        self.student_scroll_view.add_widget(self.student_list_layout)
        self.layout.add_widget(self.student_scroll_view)

        # Right Side: Input Fields for Updating Marks
        self.update_layout = BoxLayout(orientation='vertical', size_hint=(0.5, 1), spacing=10)
        self.layout.add_widget(self.update_layout)

        self.enrollment_input = TextInput(hint_text="Enter Student Enrollment Number", size_hint=(1, 0.1))
        self.update_layout.add_widget(self.enrollment_input)

        self.subject_input = TextInput(hint_text="Enter Subject Name", size_hint=(1, 0.1))
        self.update_layout.add_widget(self.subject_input)

        self.new_marks_input = TextInput(hint_text="Enter New Marks", size_hint=(1, 0.1))
        self.update_layout.add_widget(self.new_marks_input)

        self.update_button = Button(text="Update Marks", size_hint=(1, 0.2))
        self.update_button.bind(on_press=self.update_student_marks)
        self.update_layout.add_widget(self.update_button)

        self.back_button = Button(text="Back", size_hint=(1, 0.2))
        self.back_button.bind(on_press=self.go_back)
        self.update_layout.add_widget(self.back_button)

        # Load student data when the screen is initialized
        self.load_student_data()

    def on_enter(self, *args):
        """
        Reloads student data every time the screen is displayed.
        """
        self.load_student_data()

    def load_student_data(self):
        """
        Loads student data from the CSV file and displays it in the scrollable list.
        """
        # Clear the existing student list
        self.student_list_layout.clear_widgets()

        try:
            with open("Student DataBase.csv", mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Display student details
                    student_info = f"{row['Name']} - {row['Enrollment']}"
                    for subject, marks in row.items():
                        if subject not in ["Name", "Enrollment", "Password", "Sex"]:
                            student_info += f"\n  {subject}: {marks}"

                    # Add the student details to the scrollable list
                    self.student_list_layout.add_widget(Label(text=student_info, size_hint_y=None, height=100))

                    # Add 3-4 blank lines after each student's details
                    for _ in range(3):  # Add 3 blank lines
                        self.student_list_layout.add_widget(Label(text="", size_hint_y=None, height=20))
        except FileNotFoundError:
            self.show_popup("Error", "Student DataBase.csv not found.")

    def update_student_marks(self, instance):
        """
        Updates the marks of a specific student for a given subject.
        Refreshes the student list to show the updated marks in real-time.
        """
        enrollment = self.enrollment_input.text
        subject = self.subject_input.text
        new_marks = self.new_marks_input.text

        if not enrollment or not subject or not new_marks:
            self.show_popup("Error", "Please fill all fields.")
            return

        try:
            with open("Student DataBase.csv", mode="r") as file:
                students = list(csv.DictReader(file))

            updated = False
            for student in students:
                if student["Enrollment"] == enrollment:
                    if subject in student:
                        original_student = student.copy()  # Make a copy BEFORE modification
                        original_marks = student[subject]  # Save the pre-edit value
                        student[subject] = new_marks
                        updated = True
                    break

            if updated:
                # Write the updated data back to the CSV file
                with open("Student DataBase.csv", mode="w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=students[0].keys())
                    writer.writeheader()
                    writer.writerows(students)

                #Automated Word file generation
                from generator import update_or_create_student_word_file
                update_or_create_student_word_file(original_student, subject, new_marks, self.faculty_name)

                # Reload the student data to reflect the updated marks
                self.load_student_data()

                self.show_popup("Success", "Marks updated successfully.")
            else:
                self.show_popup("Error", "Student or subject not found.")
        except FileNotFoundError:
            self.show_popup("Error", "Student DataBase.csv not found.")

    def go_back(self, instance):
        """
        Navigates back to the FacultyOptionsScreen.
        """
        self.manager.current = "faculty_options_screen"

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.5, 0.5))
        popup.open()

class StudentManagementApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        # Add screens to the screen manager
        login_screen = LoginScreen(name="login_screen", screen_manager=self.screen_manager)
        self.screen_manager.add_widget(login_screen)

        student_detail_screen = StudentDetailScreen(name="student_detail_screen")
        self.screen_manager.add_widget(student_detail_screen)

        faculty_options_screen = FacultyOptionsScreen(name="faculty_options_screen")
        self.screen_manager.add_widget(faculty_options_screen)

        view_edit_screen = ViewEditScreen(name="view_edit_screen")
        self.screen_manager.add_widget(view_edit_screen)

        return self.screen_manager

if __name__ == "__main__":
    StudentManagementApp().run()