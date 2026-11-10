from flask import Flask, render_template, request, redirect, url_for, session, flash
from products import PRODUCTS

app = Flask(__name__)
app.secret_key = "change-this-secret-key-before-deployment"

def get_product(product_id):
    return next((p for p in PRODUCTS if p["id"] == int(product_id)), None)

def cart_details():
    cart = session.get("cart", {})
    items, total, count = [], 0, 0
    for product_id, quantity in cart.items():
        product = get_product(product_id)
        if product and quantity > 0:
            subtotal = product["price"] * quantity
            items.append({"product": product, "quantity": quantity, "subtotal": subtotal})
            total += subtotal
            count += quantity
    return items, total, count

@app.context_processor
def inject_cart_count():
    return {"cart_count": cart_details()[2]}

@app.route("/")
def home():
    query = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "All")
    products = [
        p for p in PRODUCTS
        if (category == "All" or p["category"] == category)
        and (not query or query in p["name"].lower() or query in p["brand"].lower())
    ]
    categories = sorted({p["category"] for p in PRODUCTS})
    return render_template("index.html", products=products, categories=categories,
                           selected_category=category, query=request.args.get("q", ""))

@app.route("/product/<int:product_id>")
def product(product_id):
    item = get_product(product_id)
    if not item:
        flash("That product could not be found.", "error")
        return redirect(url_for("home"))
    return render_template("product.html", product=item)

@app.route("/cart")
def cart():
    items, total, _ = cart_details()
    return render_template("cart.html", items=items, total=total)

@app.post("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    product = get_product(product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("home"))
    quantity = max(1, min(10, int(request.form.get("quantity", 1))))
    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = min(10, cart.get(key, 0) + quantity)
    session["cart"] = cart
    flash(f"{product['name']} added to your bag.", "success")
    return redirect(request.referrer or url_for("home"))

@app.post("/cart/update")
def update_cart():
    cart = session.get("cart", {})
    for product_id in list(cart):
        try:
            quantity = int(request.form.get(f"quantity_{product_id}", cart[product_id]))
        except ValueError:
            quantity = 0
        if quantity <= 0:
            cart.pop(product_id, None)
        else:
            cart[product_id] = min(10, quantity)
    session["cart"] = cart
    flash("Your bag has been updated.", "success")
    return redirect(url_for("cart"))

@app.post("/cart/remove/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    flash("Item removed from your bag.", "success")
    return redirect(url_for("cart"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total, _ = cart_details()
    if not items:
        return redirect(url_for("cart"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        if len(name) < 2 or "@" not in email or len(phone) < 10 or len(address) < 10:
            flash("Please complete all delivery details correctly.", "error")
            return render_template("checkout.html", items=items, total=total)
        import secrets
        order_number = "MS" + secrets.token_hex(3).upper()
        session["last_order"] = {"number": order_number, "name": name, "total": total}
        session["cart"] = {}
        return redirect(url_for("success"))
    return render_template("checkout.html", items=items, total=total)

@app.route("/order-success")
def success():
    order = session.pop("last_order", None)
    if not order:
        return redirect(url_for("home"))
    return render_template("success.html", order=order)

if __name__ == "__main__":
    app.run(debug=True)
