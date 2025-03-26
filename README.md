# Ecommerce
This project demonstrates a modern microservices-based e-commerce backend
# E-Commerce Microservices Platform

A scalable, modular online shopping system built with Python, Flask, MongoDB, RabbitMQ, and Docker.

## 📌 Overview
This project demonstrates a modern microservices-based e-commerce backend, where independent services handle user authentication, product catalog, orders, and notifications.

### Key Features:
- **JWT authentication** for secure user access.
- **Decoupled services** communicating via REST APIs (synchronous) and RabbitMQ (asynchronous).
- **Containerized** with Docker for easy deployment.
- **MongoDB** for flexible NoSQL data storage.

## 🛠️ Tech Stack

| Component         | Technology          |
|------------------|--------------------|
| Backend Framework | Flask (Python)     |
| Database         | MongoDB (NoSQL)    |
| Authentication   | JWT (JSON Web Tokens) |
| Messaging       | RabbitMQ (for async notifications) |
| Containerization | Docker + Docker Compose |
| API Communication | REST (HTTP/JSON) |

## 📂 Project Structure
```
ecommerce-microservices/  
├── product-service/      # Manages product catalog and inventory  
├── user-service/         # Handles user registration/auth (JWT)  
├── order-service/        # Processes orders and publishes events  
├── notification-service/ # Listens to events (e.g., sends emails)  
├── docker-compose.yml    # Orchestrates all services + dependencies  
└── .gitignore            # Excludes venv, IDE files, etc.  
```

## 🚀 Key Features

### User Authentication
- Secure JWT-based login/registration.
- Protected API endpoints using `@jwt_required`.

### Product Management
- CRUD operations for products (name, price, stock).
- Real-time stock updates when orders are placed.

### Order Processing
- Orders deduct product stock synchronously via REST API.
- Publishes `order_created` events to RabbitMQ for async processing.

### Notifications
- Notification service listens to RabbitMQ events.
- Simulates email/SMS alerts for order confirmations.

### Scalability
- Each service runs in isolated Docker containers.
- Easy to scale horizontally (e.g., add more `order-service` instances).

## 🔧 How It Works

### 1. User Places an Order
```
sequenceDiagram  
    User->>Order-Service: POST /orders (JWT)  
    Order-Service->>Product-Service: Check stock (REST)  
    Product-Service-->>Order-Service: Stock status  
    Order-Service->>MongoDB: Save order  
    Order-Service->>RabbitMQ: Publish "order_created"  
    RabbitMQ->>Notification-Service: Send notification  
```

### 2. Services Communication
- **Synchronous:** REST APIs (e.g., `order-service` → `product-service`).
- **Asynchronous:** RabbitMQ events (e.g., `order-service` → `notification-service`).

## 🛠️ Setup & Run

### Prerequisites:
- Docker + Docker Compose installed.

### Steps:
```bash
git clone https://github.com/your-repo/ecommerce-microservices.git  
cd ecommerce-microservices  
docker-compose up --build  
```

### Access Services:
- **User Service:** http://localhost:5002
- **Product Service:** http://localhost:5001
- **RabbitMQ Dashboard:** http://localhost:15672 (guest/guest)

## 🔍 Why This Architecture?
- **Modularity:** Services can be developed/deployed independently.
- **Resilience:** Failure in one service (e.g., notifications) doesn’t crash the entire system.
- **Performance:** Async messaging (RabbitMQ) offloads slow tasks (e.g., sending emails).

## 📜 License
MIT

## 🎯 Ideal For
- Learning microservices, Docker, and async communication.
- Building a scalable e-commerce backend.
- Experimenting with Flask + MongoDB + RabbitMQ.

