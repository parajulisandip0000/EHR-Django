# EHR Django Application

This project is a Django-based Electronic Health Record (EHR) application built for coursework. It includes:

- Patient, Hospital, Doctor, and Registration models
- Django admin integration
- Server-rendered CRUD views
- Django form validation with custom validation rules
- Session handling example
- REST API with Django REST Framework

## Requirements

- Python 3.13 or a compatible recent Python 3 version
- `pip`
- Internet access for installing dependencies the first time

## Project Setup

1. Clone the repository:

```bash
git clone https://github.com/parajulisandip0000/EHR-Django.git
cd EHR-Django
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

This installs the exact dependency versions listed in [requirements.txt](d:/Study/KU%20HI151/EHR/requirements.txt).

## Database Setup

This project uses SQLite by default. The `db.sqlite3` file is not stored in git and will be created locally when you run migrations.

Run:

```bash
python manage.py migrate
```

After this step, `db.sqlite3` will be created automatically in the project root.

## Create an Admin User

To access Django admin, create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts for username, email, and password.

## Run the Application

Start the development server:

```bash
python manage.py runserver
```

Open these URLs in your browser:

- Main application: `http://127.0.0.1:8000/`
- Django admin: `http://127.0.0.1:8000/admin/`
- API root: `http://127.0.0.1:8000/api/`

## Main Features

### Web Views

- Dashboard
- Patient CRUD
- Hospital CRUD
- Doctor CRUD
- Registration CRUD
- Session handling demo

### Validation

- Built-in Django form validation
- Custom validation for future patient birth dates
- Custom validation to ensure a doctor belongs to the selected hospital

### Session Handling

The session demo allows you to:

- Store selected hospital information in the session
- Reuse session data to filter dashboard and registration data
- Clear session data safely

### API Endpoints

Available endpoints under `/api/`:

- `/api/patients/`
- `/api/doctors/`
- `/api/hospitals/`
- `/api/registrations/`

Each endpoint supports CRUD operations through Django REST Framework.

## Run Checks and Tests

Run Django system checks:

```bash
python manage.py check
```

Run tests:

```bash
python manage.py test
```

## Project Structure

```text
EHR-Django/
|-- config/
|-- ehr/
|   |-- migrations/
|   |-- templates/ehr/
|   |-- templatetags/
|   |-- admin.py
|   |-- api.py
|   |-- forms.py
|   |-- models.py
|   |-- serializers.py
|   |-- services.py
|   |-- tests.py
|   |-- urls.py
|   `-- views.py
|-- manage.py
|-- README.md
`-- .gitignore
```

## Notes

- Default database: SQLite
- Default timezone in settings: `Asia/Kathmandu`
- `ALLOWED_HOSTS` is configured for local development
