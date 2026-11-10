# Mobile Shopee — Python E-commerce Demo

A responsive mobile-phone and accessories storefront built with **Python Flask**, HTML templates, CSS and JavaScript.

## Features
- Responsive professional storefront
- Product listing and detail pages
- Search by product name or brand
- Category filtering
- Session-based shopping cart (add, update, remove)
- Demo checkout form and order confirmation
- Sample product catalogue in `products.py`

## Run on Windows
1. Install Python 3.10 or newer.
2. Extract the ZIP folder.
3. Open Command Prompt in the extracted `mobile_shopee_python` folder.
4. Install dependencies:
   ```bash
   py -m pip install -r requirements.txt
   ```
5. Start the website:
   ```bash
   py app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser.

## Run on macOS / Linux
```bash
python3 -m pip install -r requirements.txt
python3 app.py
```
Then open `http://127.0.0.1:5000`.

## Customise
- Edit products and prices in `products.py`.
- Edit design in `static/css/style.css`.
- Edit page layouts in `templates/`.

## Important
This is a learning/demo project. Checkout creates a sample order only; it does not process payments, save orders to a database, send emails, or ship products. Before public deployment, set a strong secret key using an environment variable, disable Flask debug mode, add a database, real authentication, payment gateway integration and production security settings. Product images load from Unsplash and require an internet connection.
