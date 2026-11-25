# SriMart - Django E-Commerce Website

SriMart is a Django-based e-commerce web application developed for selling homemade pickles and food products online.

## Features

- User registration and login
- Product listing and product categories
- Product details
- Shopping cart
- Increase and decrease cart quantity
- Wishlist
- User profile
- Order and checkout functionality
- Django admin panel for managing products

## Technologies Used

- Python
- Django
- HTML
- CSS
- SQLite
- Pillow

## Project Structure

```text
SriMart/
├── config/
├── store/
├── products/
├── manage.py
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/srilatha-0309/SriMart-Django.git
```

### 2. Navigate to the project folder

```bash
cd SriMart-Django
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install django pillow python-dotenv
```

### 6. Configure environment variables

Create a `.env` file in the project root and add:

```env
DJANGO_SECRET_KEY=your-secret-key
```

Replace `your-secret-key` with your own Django secret key.

### 7. Apply database migrations

```bash
python manage.py migrate
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open the application in your browser:

http://127.0.0.1:8000/

## Author

Srilatha

GitHub: https://github.com/srilatha-0309
