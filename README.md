# Sky Group Work Project - Mohammad Bari, Rahath Ali, Rtihik Jeyathees, Hashim Khan

Django-Web Based Application for SKY Coursework

---

##  Cloning and seting up the project

Follow the instructions below to set up the project for your own system

---

### Windows Setup Instructions

1. **Clone the repository**  
   Open Command Prompt
   Go line by line: <br>
   git clone https://github.com/sophiaSyn/SkyGroupWork.git
   cd SkyGroupWork
   

2. **Create and activate virtual environment**
   
   python -m venv venv <br>
   venv\Scripts\activate
   

3. **Install required packages**
   
   pip install -r requirements.txt
   

4. **Apply database migrations**
   
   python manage.py migrate
   

5. **Run the development server to test if set up has worked**
   
   python manage.py runserver
   

---

### macOS /  Linux Setup Instructions

1. **Clone the repository**
   Go line by line: <br>
   git clone https://github.com/sophiaSyn/SkyGroupWork.git
   cd SkyGroupWork
   

1. **Create and activate virtual environment**
   
   python3 -m venv venv <br>
   source venv/bin/activate
   

2. **Install required packages**
   
   pip install -r requirements.txt
   

3. **Apply database migrations**
   
   python3 manage.py migrate
   

4. **Run the development server**
   
   python3 manage.py runserver
   

---

### 🔐 Create a Superuser (Optional for Admin Access)


python manage.py createsuperuser


Follow the prompts to set a username, email, and password.

---
