from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional
import math

app = FastAPI()

# ─────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────

menu = [
    {"id": 1, "name": " veg pizza",         "price": 250, "category": "Pizza",   "is_available": True},
    {"id": 2, "name": " Chicken Pizza",   "price": 350, "category": "Pizza",   "is_available": True},
    {"id": 3, "name": "Classic Burger",    "price": 150, "category": "Burger",  "is_available": True},
    {"id": 4, "name": "Cheese Burger",     "price": 180, "category": "Burger",  "is_available": False},
    {"id": 5, "name": "Mango Shake",       "price": 80,  "category": "Drink",   "is_available": True},
    {"id": 6, "name": "Chocolate Lava Cake","price": 120, "category": "Dessert", "is_available": True},
    {"id": 7, "name": "Cola",              "price": 40,  "category": "Drink",   "is_available": True},
    {"id": 8, "name": "Brownie",           "price": 90,  "category": "Dessert", "is_available": True},
]

orders = []
order_counter = 1

cart = []

menu_counter = 9  # next menu item id


# ─────────────────────────────────────────────
#  PYDANTIC MODELS
# ─────────────────────────────────────────────

class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=20)
    delivery_address: str = Field(..., min_length=10)
    order_type: str = Field(default="delivery")   # Q9


class NewMenuItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    is_available: bool = Field(default=True)


class CheckoutRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    delivery_address: str = Field(..., min_length=10)


# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────

def find_menu_item(item_id: int):
    """Return menu item dict if found, else None."""
    for item in menu:
        if item["id"] == item_id:
            return item
    return None


def calculate_bill(price: int, quantity: int, order_type: str = "delivery") -> int:
    """Return total bill. Adds ₹30 delivery charge for 'delivery' orders."""
    total = price * quantity
    if order_type == "delivery":
        total += 30
    return total


def filter_menu_logic(
    category: Optional[str],
    max_price: Optional[int],
    is_available: Optional[bool],
) -> list:
    """Apply all three optional filters using 'is not None' checks."""
    result = menu.copy()
    if category is not None:
        result = [i for i in result if i["category"].lower() == category.lower()]
    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]
    if is_available is not None:
        result = [i for i in result if i["is_available"] == is_available]
    return result


# ─────────────────────────────────────────────
#  Q1 — GET /  (Day 1)
# ─────────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "Welcome to QuickBite Food Delivery"}


# ─────────────────────────────────────────────
#  Q5 — GET /menu/summary  (Day 1)
#  MUST be above /menu/{item_id}
# ─────────────────────────────────────────────

@app.get("/menu/summary")
def menu_summary():
    available = [i for i in menu if i["is_available"]]
    unavailable = [i for i in menu if not i["is_available"]]
    categories = list({i["category"] for i in menu})
    return {
        "total_items": len(menu),
        "available": len(available),
        "unavailable": len(unavailable),
        "categories": categories,
    }


# ─────────────────────────────────────────────
#  Q10 — GET /menu/filter  (Day 3)
#  MUST be above /menu/{item_id}
# ─────────────────────────────────────────────

@app.get("/menu/filter")
def filter_menu(
    category: Optional[str] = Query(default=None),
    max_price: Optional[int] = Query(default=None),
    is_available: Optional[bool] = Query(default=None),
):
    result = filter_menu_logic(category, max_price, is_available)
    return {"items": result, "count": len(result)}


# ─────────────────────────────────────────────
#  Q16 — GET /menu/search  (Day 6)
# ─────────────────────────────────────────────

@app.get("/menu/search")
def search_menu(keyword: str = Query(...)):
    kw = keyword.lower()
    result = [
        i for i in menu
        if kw in i["name"].lower() or kw in i["category"].lower()
    ]
    if not result:
        return {"message": f"No items found matching '{keyword}'", "total_found": 0}
    return {"items": result, "total_found": len(result)}


# ─────────────────────────────────────────────
#  Q17 — GET /menu/sort  (Day 6)
# ─────────────────────────────────────────────

@app.get("/menu/sort")
def sort_menu(
    sort_by: str = Query(default="price"),
    order: str = Query(default="asc"),
):
    valid_sort = ["price", "name", "category"]
    valid_order = ["asc", "desc"]
    if sort_by not in valid_sort:
        return {"error": f"sort_by must be one of {valid_sort}"}
    if order not in valid_order:
        return {"error": f"order must be one of {valid_order}"}
    reverse = order == "desc"
    sorted_menu = sorted(menu, key=lambda x: x[sort_by], reverse=reverse)
    return {"sort_by": sort_by, "order": order, "items": sorted_menu}


# ─────────────────────────────────────────────
#  Q18 — GET /menu/page  (Day 6)
# ─────────────────────────────────────────────

@app.get("/menu/page")
def paginate_menu(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=3, ge=1, le=10),
):
    start = (page - 1) * limit
    items = menu[start: start + limit]
    total = len(menu)
    total_pages = math.ceil(total / limit)
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "items": items,
    }


# ─────────────────────────────────────────────
#  Q20 — GET /menu/browse  (Day 6 + Day 3)
# ─────────────────────────────────────────────

@app.get("/menu/browse")
def browse_menu(
    keyword: Optional[str] = Query(default=None),
    sort_by: str = Query(default="price"),
    order: str = Query(default="asc"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=4, ge=1, le=10),
):
    # Step 1: Filter
    result = menu.copy()
    if keyword is not None:
        kw = keyword.lower()
        result = [i for i in result if kw in i["name"].lower() or kw in i["category"].lower()]

    # Step 2: Sort
    valid_sort = ["price", "name", "category"]
    valid_order = ["asc", "desc"]
    if sort_by not in valid_sort:
        return {"error": f"sort_by must be one of {valid_sort}"}
    if order not in valid_order:
        return {"error": f"order must be one of {valid_order}"}
    reverse = order == "desc"
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # Step 3: Paginate
    total = len(result)
    total_pages = math.ceil(total / limit) if total > 0 else 1
    start = (page - 1) * limit
    page_items = result[start: start + limit]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "items": page_items,
    }


# ─────────────────────────────────────────────
#  Q2 — GET /menu  (Day 1)
# ─────────────────────────────────────────────

@app.get("/menu")
def get_menu():
    return {"items": menu, "total": len(menu)}


# ─────────────────────────────────────────────
#  Q11 — POST /menu  (Day 4)
# ─────────────────────────────────────────────

@app.post("/menu")
def add_menu_item(item: NewMenuItem, response=None):
    global menu_counter
    # Check duplicate name (case-insensitive)
    for existing in menu:
        if existing["name"].lower() == item.name.lower():
            return {"error": f"Item '{item.name}' already exists in the menu"}
    new_item = {
        "id": menu_counter,
        "name": item.name,
        "price": item.price,
        "category": item.category,
        "is_available": item.is_available,
    }
    menu.append(new_item)
    menu_counter += 1
    from fastapi.responses import JSONResponse
    return JSONResponse(content=new_item, status_code=201)


# ─────────────────────────────────────────────
#  Q3 — GET /menu/{item_id}  (Day 1)
# ─────────────────────────────────────────────

@app.get("/menu/{item_id}")
def get_menu_item(item_id: int):
    item = find_menu_item(item_id)
    if item is None:
        return {"error": "Item not found"}
    return item


# ─────────────────────────────────────────────
#  Q12 — PUT /menu/{item_id}  (Day 4)
# ─────────────────────────────────────────────

@app.put("/menu/{item_id}")
def update_menu_item(
    item_id: int,
    price: Optional[int] = Query(default=None),
    is_available: Optional[bool] = Query(default=None),
):
    item = find_menu_item(item_id)
    if item is None:
        return {"error": "Item not found"}
    if price is not None:
        item["price"] = price
    if is_available is not None:
        item["is_available"] = is_available
    return {"message": "Item updated", "item": item}


# ─────────────────────────────────────────────
#  Q13 — DELETE /menu/{item_id}  (Day 4)
# ─────────────────────────────────────────────

@app.delete("/menu/{item_id}")
def delete_menu_item(item_id: int):
    item = find_menu_item(item_id)
    if item is None:
        return {"error": "Item not found"}
    menu.remove(item)
    return {"message": f"'{item['name']}' has been removed from the menu"}


# ─────────────────────────────────────────────
#  Q4 — GET /orders  (Day 1)
# ─────────────────────────────────────────────

@app.get("/orders")
def get_orders():
    return {"orders": orders, "total_orders": len(orders)}


# ─────────────────────────────────────────────
#  Q19 — GET /orders/search  (Day 6)
#  MUST be above /orders/{id}
# ─────────────────────────────────────────────

@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):
    result = [o for o in orders if customer_name.lower() in o["customer_name"].lower()]
    return {"orders": result, "total": len(result)}


# ─────────────────────────────────────────────
#  Q19 — GET /orders/sort  (Day 6)
# ─────────────────────────────────────────────

@app.get("/orders/sort")
def sort_orders(order: str = Query(default="asc")):
    if order not in ["asc", "desc"]:
        return {"error": "order must be 'asc' or 'desc'"}
    reverse = order == "desc"
    sorted_orders = sorted(orders, key=lambda x: x["total_price"], reverse=reverse)
    return {"order": order, "orders": sorted_orders}


# ─────────────────────────────────────────────
#  Q8 + Q9 — POST /orders  (Day 2 + Day 3)
# ─────────────────────────────────────────────

@app.post("/orders")
def place_order(order_req: OrderRequest):
    global order_counter
    item = find_menu_item(order_req.item_id)
    if item is None:
        return {"error": "Item not found"}
    if not item["is_available"]:
        return {"error": f"'{item['name']}' is currently unavailable"}
    if order_req.order_type not in ["delivery", "pickup"]:
        return {"error": "order_type must be 'delivery' or 'pickup'"}

    total = calculate_bill(item["price"], order_req.quantity, order_req.order_type)
    new_order = {
        "order_id": order_counter,
        "customer_name": order_req.customer_name,
        "item_name": item["name"],
        "item_id": item["id"],
        "quantity": order_req.quantity,
        "delivery_address": order_req.delivery_address,
        "order_type": order_req.order_type,
        "total_price": total,
        "status": "confirmed",
    }
    orders.append(new_order)
    order_counter += 1
    return new_order


# ─────────────────────────────────────────────
#  Q14 — POST /cart/add  (Day 5)
#  MUST be above /cart/{item_id}
# ─────────────────────────────────────────────

@app.post("/cart/add")
def add_to_cart(item_id: int = Query(...), quantity: int = Query(default=1)):
    item = find_menu_item(item_id)
    if item is None:
        return {"error": "Item not found"}
    if not item["is_available"]:
        return {"error": f"'{item['name']}' is currently unavailable"}
    # If item already in cart, update quantity
    for cart_item in cart:
        if cart_item["item_id"] == item_id:
            cart_item["quantity"] += quantity
            cart_item["subtotal"] = item["price"] * cart_item["quantity"]
            return {"message": "Cart updated", "cart_item": cart_item}
    # Else add new entry
    cart_entry = {
        "item_id": item_id,
        "name": item["name"],
        "price": item["price"],
        "quantity": quantity,
        "subtotal": item["price"] * quantity,
    }
    cart.append(cart_entry)
    return {"message": "Item added to cart", "cart_item": cart_entry}


# ─────────────────────────────────────────────
#  Q14 — GET /cart  (Day 5)
# ─────────────────────────────────────────────

@app.get("/cart")
def get_cart():
    grand_total = sum(i["subtotal"] for i in cart)
    return {"cart": cart, "grand_total": grand_total}


# ─────────────────────────────────────────────
#  Q15 — POST /cart/checkout  (Day 5)
#  MUST be above /cart/{item_id}
# ─────────────────────────────────────────────

@app.post("/cart/checkout")
def checkout(req: CheckoutRequest):
    global order_counter
    if not cart:
        return {"error": "Cart is empty. Add items before checking out."}

    placed_orders = []
    grand_total = 0

    for cart_item in cart:
        item = find_menu_item(cart_item["item_id"])
        total = calculate_bill(item["price"], cart_item["quantity"], "delivery")
        new_order = {
            "order_id": order_counter,
            "customer_name": req.customer_name,
            "item_name": item["name"],
            "item_id": item["id"],
            "quantity": cart_item["quantity"],
            "delivery_address": req.delivery_address,
            "order_type": "delivery",
            "total_price": total,
            "status": "confirmed",
        }
        orders.append(new_order)
        placed_orders.append(new_order)
        order_counter += 1
        grand_total += total

    cart.clear()

    from fastapi.responses import JSONResponse
    return JSONResponse(
        content={
            "message": "Checkout successful!",
            "orders_placed": placed_orders,
            "grand_total": grand_total,
        },
        status_code=201,
    )


# ─────────────────────────────────────────────
#  Q15 — DELETE /cart/{item_id}  (Day 5)
# ─────────────────────────────────────────────

@app.delete("/cart/{item_id}")
def remove_from_cart(item_id: int):
    for cart_item in cart:
        if cart_item["item_id"] == item_id:
            cart.remove(cart_item)
            return {"message": f"'{cart_item['name']}' removed from cart"}
    return {"error": "Item not in cart"}