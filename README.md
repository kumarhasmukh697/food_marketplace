# 🍽️ FoodHub --- Multi-Vendor Food Delivery Marketplace

**FoodHub** is a full-stack multi-vendor food delivery marketplace built
with **Django, Django REST Framework, PostgreSQL, Redis, Celery,
JavaScript, Nginx, and Gunicorn**.

The platform is designed around three primary user roles --- **Customer,
Vendor, and Delivery Partner** --- with an administrative role for
platform management.

## 🌐 Live Project

**Live Website:** https://foodhub.net.in

> The application is deployed on a Linux VPS with Nginx, Gunicorn,
> PostgreSQL, Redis, Celery, and HTTPS.

------------------------------------------------------------------------

## 📌 Project Overview

FoodHub is designed as a marketplace where:

-   Customers can discover food products from multiple vendors.
-   Vendors can manage their shops and food products.
-   Customers can add products to a cart and place orders.
-   Vendors can process orders through different order statuses.
-   Delivery partners can receive delivery assignments and update
    delivery status.
-   Customers can track delivery information.
-   Authentication and authorization are handled according to user
    roles.
-   Background jobs can be processed using Celery and Redis.
-   Payments are integrated with Razorpay.
-   Google Maps is used for location-related functionality.
-   Email/OTP functionality is supported through Gmail SMTP.

The project follows a production-oriented deployment architecture rather
than being limited to local development.

------------------------------------------------------------------------

## ✨ Key Features

### 👤 Customer

-   User registration and login
-   Email OTP verification
-   Customer profile management
-   Address management
-   Browse vendors and food products
-   Product search
-   Product categories
-   Shopping cart
-   Wishlist
-   Coupons/discount support
-   Order placement
-   Order status tracking
-   Delivery tracking
-   Review functionality
-   Payment integration
-   Google Maps-based location functionality

### 🏪 Vendor

-   Vendor registration/profile
-   Shop information management
-   Opening and closing times
-   Accepting-orders control
-   Food type configuration
-   Product management
-   Product availability management
-   Vendor order management
-   Order status updates
-   Vendor-specific order handling

### 🛵 Delivery Partner

-   Delivery profile
-   Availability management
-   Delivery assignment
-   Order pickup/status updates
-   Out-for-delivery status
-   Delivered status
-   Current location updates
-   Customer delivery tracking support

### 🔐 Authentication & Security

-   Custom Django user model
-   Role-based access
-   JWT authentication for APIs
-   Django sessions for server-rendered pages
-   JWT refresh-token handling
-   Refresh-token rotation
-   Token blacklisting
-   OTP verification
-   Environment-based secret configuration
-   Production security settings
-   HTTPS/SSL
-   Secure cookies in production
-   CSRF protection
-   CORS configuration
-   HSTS configuration

### 💳 Payments

-   Razorpay integration
-   Environment-based Razorpay credentials
-   Payment-related backend structure

### 📍 Location & Delivery Tracking

-   Google Maps integration
-   Delivery partner location updates
-   Customer delivery tracking
-   Periodic location updates
-   Nearest available delivery partner assignment using geographic
    distance calculations

### ⚙️ Background Processing

-   Celery
-   Redis
-   Background task processing
-   Production Celery worker managed by systemd

------------------------------------------------------------------------

# 🏗️ Technology Stack

  Layer                Technology
  -------------------- -----------------------------------------
  Backend              Django
  API                  Django REST Framework
  Authentication       JWT + Django Sessions
  Database             PostgreSQL
  Background Tasks     Celery
  Message Broker       Redis
  Frontend             HTML, CSS, JavaScript
  UI                   Tailwind CSS, Font Awesome, SweetAlert2
  Payments             Razorpay
  Maps                 Google Maps JavaScript API
  Web Server           Nginx
  Application Server   Gunicorn
  Operating System     Ubuntu Linux
  Deployment           VPS
  SSL                  Let's Encrypt / Certbot
  Version Control      Git + GitHub

------------------------------------------------------------------------

# 🧩 Project Architecture

``` text
                         Internet
                            │
                            ▼
                    foodhub.net.in
                            │
                            ▼
                     ┌─────────────┐
                     │    Nginx    │
                     │   :80/:443  │
                     └──────┬──────┘
                            │
                            ▼
                     ┌─────────────┐
                     │   Gunicorn  │
                     │    :8000    │
                     └──────┬──────┘
                            │
                            ▼
                     ┌─────────────┐
                     │   Django    │
                     │    + DRF    │
                     └──────┬──────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        PostgreSQL        Redis        External APIs
              │             │        ┌──────────────┐
              │             ▼        │   Razorpay   │
              │          Celery      │ Google Maps  │
              │         Worker       │ Gmail SMTP   │
              │                     └──────────────┘
              ▼
        Application Data
```

------------------------------------------------------------------------

# 📁 Project Structure

``` text
food_marketplace/
│
├── venv/
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── backend/
│   ├── manage.py
│   │
│   ├── config/
│   │   ├── settings/
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── accounts/
│   ├── vendors/
│   ├── categories/
│   ├── products/
│   ├── cart/
│   ├── orders/
│   ├── payments/
│   ├── reviews/
│   ├── coupons/
│   ├── wishlist/
│   ├── notifications/
│   ├── delivery/
│   ├── customer/
│   │
│   ├── media/
│   ├── static/
│   ├── staticfiles/
│   └── templates/
│
└── frontend/
```

> Django applications are intentionally located directly inside the
> `backend/` directory.

------------------------------------------------------------------------

# 🧱 Django Applications

  App               Responsibility
  ----------------- ---------------------------------------------
  `accounts`        Authentication, users, OTP, addresses
  `vendors`         Vendor profiles and vendor management
  `categories`      Food categories
  `products`        Food/product management
  `cart`            Shopping cart
  `orders`          Order management and status workflow
  `payments`        Payment integration
  `reviews`         Customer reviews
  `coupons`         Coupons and discounts
  `wishlist`        Customer wishlist
  `notifications`   Notifications
  `delivery`        Delivery partner and tracking functionality
  `customer`        Customer-specific functionality

------------------------------------------------------------------------

# 🔄 Order & Delivery Workflow

A simplified order lifecycle is:

``` text
Customer places order
        │
        ▼
     Confirmed
        │
        ▼
    Preparing
        │
        ▼
       Ready
        │
        ▼
Delivery Partner Assigned
        │
        ▼
     Picked Up
        │
        ▼
 Out for Delivery
        │
        ▼
     Delivered
```

When an order becomes ready, the backend can identify an available
delivery partner based on online/availability status and geographic
proximity.

After delivery is completed, the delivery partner becomes available
again.

------------------------------------------------------------------------

# 🔐 Authentication Architecture

FoodHub uses different authentication mechanisms for different parts of
the application.

### API Authentication

REST APIs use:

``` text
JWT Access Token
       +
JWT Refresh Token
```

The application supports:

-   Access-token expiration
-   Refresh-token rotation
-   Refresh-token blacklisting
-   Centralized API requests
-   Automatic access-token refresh

### Web Page Authentication

Django sessions are used for server-rendered page authentication.

This provides a separation between:

``` text
API authentication → JWT
Page authentication → Django Sessions
```

------------------------------------------------------------------------

# 🗄️ Database

FoodHub uses **PostgreSQL** in production.

Important application data includes:

-   Users
-   Vendor profiles
-   Products
-   Categories
-   Customers
-   Addresses
-   Carts
-   Orders
-   Order items
-   Payments
-   Reviews
-   Coupons
-   Wishlist data
-   Delivery information

------------------------------------------------------------------------

# ⚡ Redis & Celery

Redis is used as the message broker/backend for Celery.

``` text
Django
   │
   │ creates background task
   ▼
 Redis
   │
   ▼
Celery Worker
   │
   ▼
Background processing
```

The production server runs Celery as a systemd service.

------------------------------------------------------------------------

# 💳 Third-Party Services

FoodHub integrates with external services for specific functionality.

### Razorpay

Used for payment-related functionality.

### Google Maps

Used for:

-   Maps
-   Location functionality
-   Delivery tracking

### Gmail SMTP

Used for email/OTP-related functionality.

> API keys, passwords, SMTP credentials, Razorpay secrets, and Django
> `SECRET_KEY` are never intended to be stored in the Git repository.

------------------------------------------------------------------------

# 🔒 Environment Variables

Production secrets are stored in a server-side `.env` file.

Example structure:

``` env
DEBUG=False

SECRET_KEY=your-secret-key

ALLOWED_HOSTS=foodhub.net.in,www.foodhub.net.in

DATABASE_NAME=foodhub_db
DATABASE_USER=foodhub_user
DATABASE_PASSWORD=your-database-password
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432

CSRF_TRUSTED_ORIGINS=https://foodhub.net.in,https://www.foodhub.net.in

CORS_ALLOWED_ORIGINS=https://foodhub.net.in,https://www.foodhub.net.in
CORS_ALLOW_CREDENTIALS=True

RAZORPAY_KEY_ID=your-key
RAZORPAY_KEY_SECRET=your-secret

GOOGLE_MAPS_API_KEY=your-key

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email

CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```

**Never commit `.env` to GitHub.**

------------------------------------------------------------------------

# 🚀 Local Development Setup

## 1. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd food_marketplace
```

## 2. Create a virtual environment

### Windows

``` bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

``` bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

``` bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create:

``` text
backend/.env
```

and add the required development configuration.

## 5. Run migrations

``` bash
cd backend
python manage.py migrate
```

## 6. Create a superuser

``` bash
python manage.py createsuperuser
```

## 7. Run the development server

``` bash
python manage.py runserver
```

The local application will normally be available at:

``` text
http://127.0.0.1:8000/
```

------------------------------------------------------------------------

# 🖥️ Production Deployment

The production deployment uses:

``` text
Ubuntu
    │
    ├── PostgreSQL
    ├── Redis
    ├── Celery
    ├── Gunicorn
    └── Nginx
```

### Production services

  Service      Purpose
  ------------ --------------------------------------------
  Nginx        Reverse proxy, HTTPS, static/media serving
  Gunicorn     Django application server
  PostgreSQL   Production database
  Redis        Celery broker/backend
  Celery       Background worker

### Production commands

Collect static files:

``` bash
python manage.py collectstatic --noinput
```

Run migrations:

``` bash
python manage.py migrate
```

Check Django:

``` bash
python manage.py check
```

Gunicorn is managed using:

``` bash
sudo systemctl status foodhub
```

Celery is managed using:

``` bash
sudo systemctl status foodhub-celery
```

Nginx is managed using:

``` bash
sudo systemctl status nginx
```

------------------------------------------------------------------------

# 🌍 Production Domain

The application is deployed at:

**https://foodhub.net.in**

The `www` version is also configured:

**https://www.foodhub.net.in**

HTTPS is provided using a Let's Encrypt certificate managed through
Certbot.

------------------------------------------------------------------------

# 🛡️ Production Security

The deployment includes several production security measures:

-   `DEBUG=False`
-   Secret values stored in environment variables
-   Root SSH login disabled
-   SSH password authentication disabled
-   SSH key authentication
-   Firewall protection
-   PostgreSQL not publicly exposed
-   Redis not publicly exposed
-   Gunicorn bound to localhost
-   Nginx used as the public-facing server
-   HTTPS/SSL
-   CSRF protection
-   CORS restrictions
-   Secure production cookies
-   HSTS configuration
-   JWT refresh-token rotation
-   Token blacklisting

Public server ports are intentionally limited to required services such
as:

``` text
22   SSH
80   HTTP
443  HTTPS
```

Internal services such as PostgreSQL, Redis, and Gunicorn are kept
private.

------------------------------------------------------------------------

# 🔄 CI/CD

The project is designed to support GitHub-based continuous deployment.

The intended deployment flow is:

``` text
Developer
    │
    ▼
Git Push
    │
    ▼
GitHub
    │
    ▼
GitHub Actions
    │
    ├── Pull latest code
    ├── Install/update dependencies
    ├── Run migrations
    ├── Collect static files
    └── Restart application services
    │
    ▼
Production Server
```

This allows future deployments to be automated rather than manually
updating the server after every change.

------------------------------------------------------------------------

# 🧪 Useful Production Checks

Check Django:

``` bash
python manage.py check
```

Check Gunicorn:

``` bash
sudo systemctl status foodhub
```

Check Celery:

``` bash
sudo systemctl status foodhub-celery
```

Check Redis:

``` bash
redis-cli ping
```

Expected:

``` text
PONG
```

Check Nginx configuration:

``` bash
sudo nginx -t
```

Check Nginx:

``` bash
sudo systemctl status nginx
```

View Gunicorn logs:

``` bash
sudo journalctl -u foodhub -n 50 --no-pager
```

View Celery logs:

``` bash
sudo journalctl -u foodhub-celery -n 50 --no-pager
```

------------------------------------------------------------------------

# 📚 What This Project Demonstrates

FoodHub demonstrates practical experience with:

-   Python
-   Django
-   Django REST Framework
-   REST APIs
-   JWT authentication
-   Role-based permissions
-   PostgreSQL
-   Redis
-   Celery
-   Background processing
-   JavaScript
-   AJAX/fetch API integration
-   Payment integration
-   Maps integration
-   Geolocation
-   Order management
-   Delivery workflows
-   Multi-vendor marketplace architecture
-   Linux server administration
-   Nginx
-   Gunicorn
-   HTTPS/SSL
-   Firewall configuration
-   Environment-based configuration
-   Git/GitHub
-   Production deployment
-   CI/CD architecture

------------------------------------------------------------------------

# 🎯 Future Improvements

Potential future improvements include:

-   Automated GitHub Actions deployment
-   More advanced delivery route optimization
-   Real-time delivery tracking using WebSockets
-   Improved vendor analytics
-   Customer recommendation system
-   Personalized food recommendations using machine learning
-   Advanced search and filtering
-   Performance optimization and caching
-   Automated monitoring and alerting
-   Comprehensive automated test coverage
-   API documentation with OpenAPI/Swagger
-   Containerized deployment with Docker

------------------------------------------------------------------------

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

A typical workflow is:

``` bash
git checkout -b feature/your-feature
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

Then open a Pull Request on GitHub.

------------------------------------------------------------------------

# 📄 License

This project currently does not specify an open-source license.

If you intend to allow others to use, modify, or distribute the source
code, consider adding an appropriate license such as MIT.

------------------------------------------------------------------------

# 👨‍💻 Project

**FoodHub --- Multi-Vendor Food Delivery Marketplace**

🌐 **Live:** https://foodhub.net.in

Built with ❤️ using Django, DRF, PostgreSQL, Redis, Celery, JavaScript,
Nginx, and Gunicorn.
