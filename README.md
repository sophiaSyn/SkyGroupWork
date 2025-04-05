# 🌐 SkyGroupWork – Django Web Application

A collaborative Django-based web application developed for group coursework. This project follows best practices in version control, virtual environments, and team workflows using GitHub.

---

## 📥 How to Clone & Set Up the Project

Follow the instructions below to set up the project on your local machine for development.

---

### 🪟 Windows Setup Instructions

1. **Clone the repository**  
   Open Command Prompt or PowerShell:
   ```powershell
   git clone https://github.com/sophiaSyn/SkyGroupWork.git
   cd SkyGroupWork
   ```

2. **Create and activate virtual environment**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install required packages**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```powershell
   python manage.py migrate
   ```

5. **Run the development server**
   ```powershell
   python manage.py runserver
   ```

---

### 🍎 macOS / 🐧 Linux Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/sophiaSyn/SkyGroupWork.git
   cd SkyGroupWork
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python3 manage.py migrate
   ```

5. **Run the development server**
   ```bash
   python3 manage.py runserver
   ```

---

### 🔐 Create a Superuser (Optional for Admin Access)

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

---
