# 🍕 QuickBite — Food Delivery API

---

## 📖 Project Overview

QuickBite is a backend REST API for a food delivery platform built with **FastAPI** and **Python**. It handles everything from browsing the menu to placing orders and checking out a cart all testable through Swagger UI.

This project was built as a final project for a FastAPI internship program, covering 6 days of concepts including GET/POST routes, Pydantic validation, CRUD operations, cart workflows, and advanced search/sort/pagination.

---

## 🚀 Key Features

- Menu management — Add, Update, and Delete food items
- View all food items and get a single item by ID
- Filter menu by category, price, and availability
- Search food items using keywords across name and category
- Sort menu by price, name, or category
- Pagination support for large data sets
- Smart browse endpoint combining search, sort, and pagination
- Cart system — Add, Update, and Remove items
- Order system — Checkout and view all orders
- Input validation using Pydantic models
- API testing using Swagger UI

---

## 🛠️ Technologies Used

- **Python 3** — Core programming language
- **FastAPI** — Web framework for building REST APIs
- **Pydantic** — Data validation and request body modeling
- **Uvicorn** — ASGI server to run the application

---

## ⚙️ How to Run the Project

**1. Install Dependencies**
```bash
pip install -r requirements.txt
```

**2. Run the Server**
```bash
uvicorn main:app --reload
```

**3. Open in Browser**
```
http://127.0.0.1:8000/docs
```

All endpoints can be tested directly from the Swagger UI interface.

---

## 📂 Project Structure

```
fastapi-food-delivery/
├── main.py
├── requirements.txt
├── README.md
└── screenshots/
```

---

## 🔗 API Endpoints

**Menu APIs**

| Method | Endpoint | Description |
|---|---|---|
| GET | `/menu` | Get all menu items |
| GET | `/menu/summary` | Menu stats and categories |
| GET | `/menu/{item_id}` | Get item by ID |
| POST | `/menu` | Add a new item |
| PUT | `/menu/{item_id}` | Update item |
| DELETE | `/menu/{item_id}` | Delete item |

**Advanced Menu APIs**

| Method | Endpoint | Description |
|---|---|---|
| GET | `/menu/filter` | Filter by category, price, availability |
| GET | `/menu/search` | Search by keyword |
| GET | `/menu/sort` | Sort by price, name, or category |
| GET | `/menu/page` | Paginate menu items |
| GET | `/menu/browse` | Search + sort + pagination combined |

**Cart APIs**

| Method | Endpoint | Description |
|---|---|---|
| POST | `/cart/add` | Add item to cart |
| GET | `/cart` | View cart and grand total |
| DELETE | `/cart/{item_id}` | Remove item from cart |
| POST | `/cart/checkout` | Checkout all cart items |

**Order APIs**

| Method | Endpoint | Description |
|---|---|---|
| GET | `/orders` | View all orders |
| GET | `/orders/search` | Search orders by customer name |
| GET | `/orders/sort` | Sort orders by total price |
| POST | `/orders` | Place a single order |

---

## 🔄 Workflow

1. User browses the menu
2. Adds items to the cart
3. Updates or removes items as needed
4. Proceeds to checkout
5. Orders are created and stored

---

## 📸 Screenshots

All API outputs tested in Swagger UI are available in the `Output_Screenshot` folder.

---

## 🎯 Learning Outcomes

- Understanding the FastAPI framework
- Building RESTful APIs with Python
- Implementing full CRUD operations
- Designing real-world backend workflows
- Validating data using Pydantic
- Testing APIs using Swagger UI

---

## 👨‍💻 Author

**Your Name** — Korivi Pavani
