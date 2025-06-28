# E-commerce Platform

## Overview

A comprehensive e-commerce platform built with Django framework. This system allows users to browse products, add them to cart, and complete purchases. It includes an integrated admin dashboard for content and user management.

## Key Features

- User authentication and registration system
- Product and category browsing
- Shopping cart functionality
- Secure PayPal payment integration
- Advanced admin dashboard
- Product and order management
- Product rating and review system
- Rich text editor (CKEditor)
- Responsive user interface

## Technologies Used

### Backend
- Python 3.x
- Django 5.1.6
- Django REST Framework (if API endpoints exist)

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap 5

### Database
- SQLite (for development)

### External Services
- PayPal for payment processing

## Requirements

- Python 3.8+
- pip (Python package manager)
- Git (for version control)

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd graduation-project-main
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # For Windows
   source venv/bin/activate  # For Linux/Mac
   ```

3. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
graduation-project-main/
├── core/                 # Main application
├── ecomprj/              # Project settings
├── userauths/            # User authentication
├── media/                # User-uploaded files
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── manage.py             # Django command-line utility
└── requirements.txt      # Project dependencies
```

## Environment Variables

Create a `.env` file in the project root and add the following variables:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
PAYPAL_RECEIVER_EMAIL=your-paypal-email@example.com
PAYPAL_TEST=True
```

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact

- Name: Abdullah mohammed yosed
- Email: abdullahmmmm64@gmail.com

