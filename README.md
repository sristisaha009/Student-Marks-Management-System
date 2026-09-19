# 📚 Student Marks Management System

A Python-based desktop application built using **Kivy** that simplifies student marks management through role-based authentication, faculty-controlled updates, and automated Word document synchronization.

## 🎯 Objective

The primary objective of this project is to digitize student marks management by providing a user-friendly interface for students and faculty.

The system enables:

* Students to securely view their academic marks.
* Faculty members to upload student records.
* Faculty members to view and update student marks.
* Automatic synchronization of marks between CSV records and Word documents.
* Faculty name and timestamp logging for accountability.

## 🛠️ Tech Stack

| Technology      | Purpose                                 |
| --------------- | --------------------------------------- |
| Python          | Core programming language               |
| Kivy            | GUI development and screen navigation   |
| python-docx     | Word document extraction and generation |
| CSV             | Student records storage                 |


## 🏗️ System Architecture

The application follows a modular architecture consisting of a graphical user interface, authentication module, data processing module, and document management module.

```text
                 ┌──────────────────────────┐
                 │       Kivy GUI           │
                 │   (ScreenManager)        │
                 └────────────┬─────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
      ┌───────▼────────┐            ┌─────────▼────────┐
      │ Student Portal │            │ Faculty Portal   │
      └───────┬────────┘            └─────────┬────────┘
              │                               │
      ┌───────▼────────┐            ┌─────────▼────────┐
      │ Authentication │            │ Faculty Actions  │
      └───────┬────────┘            └───────┬──────────┘
              │                             │
      ┌───────▼────────┐        ┌───────────┼───────────┐
      │ Grade Display  │        │           │           │
      └────────────────┘   ┌────▼────┐ ┌────▼────┐ ┌────▼─────┐
                            │ Upload │ │ View &  │ │ Document │
                            │ Files  │ │ Edit    │ │ Generator│
                            └────┬───┘ └────┬────┘ └────┬─────┘
                                 │           │           │
                                 └───────────┬┴───────────┘
                                             │
                                    ┌────────▼────────┐
                                    │  CSV Database   │
                                    └────────┬────────┘
                                             │
                                    ┌────────▼────────┐
                                    │ Student Word    │
                                    │ Documents       │
                                    └─────────────────┘
```

### Core Modules

* **UI Module (`ui.py`):** Handles screens, navigation, user input, and GUI interactions.
* **Authentication Module (`validity.py`):** Validates student and faculty credentials.
* **Extraction Module (`extractor.py`):** Extracts student information from Word documents and appends records to CSV.
* **Document Generation Module (`generator.py`):** Creates and updates student Word documents with modified marks and metadata.

## 🔄 Workflow

### 1. User Authentication

1. The user opens the application.
2. The system displays Student and Faculty login options.
3. The user enters the required credentials.
4. The system validates the credentials.
5. The user is redirected to the appropriate portal.

### 2. Student Workflow

1. Student logs in using enrollment number and password.
2. Credentials are validated.
3. Student details and marks are retrieved.
4. Marks are displayed in a read-only format.
5. Student can return to the login screen.

### 3. Faculty Workflow

#### View and Edit Marks

1. Faculty logs in using Faculty ID and password.
2. Faculty accesses the dashboard.
3. All student records are loaded from the CSV file.
4. Faculty enters the enrollment number, subject, and new marks.
5. The system validates the requested student and subject.
6. Updated marks are written to the CSV file.
7. The corresponding Word document is updated.
8. Faculty name and timestamp are recorded.
9. The interface refreshes to display the updated marks.

#### Upload Word Files

1. Faculty selects one or more Word documents using the file chooser.
2. The system validates the `.docx` file type.
3. Student information is extracted from the documents.
4. Records are appended to the CSV file.
5. Student-specific Word documents are generated.

## ⚙️ Key Features

* Role-based student and faculty login.
* Read-only student marks display.
* Faculty-controlled marks editing.
* Multiple Word file selection.
* CSV-based student record management.
* Automated Word document generation and updates.
* Faculty identity and timestamp logging.
* Kivy-based graphical interface.
* Screen navigation using ScreenManager.
* Error handling through popup notifications.

## ⚠️ Limitations

1. **CSV-Based Storage:** CSV is not ideal for large datasets, concurrent access, or complex queries.
2. **Basic Authentication:** The current implementation requires stronger password security, including password hashing.
3. **Limited Scalability:** Processing Word files for large numbers of students may impact performance.
4. **No Multi-Factor Authentication:** The system currently uses basic credential validation.
5. **Limited Bulk Operations:** Advanced bulk editing and batch processing features are not implemented.
6. **Desktop Application:** The current system is primarily designed as a desktop GUI application.


## 🚀 Future Work

* **Database Integration:** Migrate from CSV to MySQL or PostgreSQL for scalable data management.
* **Enhanced Security:** Implement password hashing, role-based permissions, and multi-factor authentication.
* **Web Application:** Develop a web-based version using Flask or Django for remote access.
* **Advanced Search:** Add student search, filtering, and sorting capabilities.
* **Bulk Processing:** Support bulk student record uploads and marks updates.
* **Audit Trail:** Maintain a structured database of all changes made to student records.
* **Automated Backups:** Implement secure data backup and recovery mechanisms.
* **Mobile Deployment:** Explore mobile application deployment using Kivy.
