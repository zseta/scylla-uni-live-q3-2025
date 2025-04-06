import streamlit as st
import requests
import pandas as pd


USER_ID = "3b647bc3-e7cd-4f6a-8951-01c93035eeab"


def fetch_products():
    response = requests.get(f"http://localhost:8000/products?limit=10")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Product not found.")
        return None


def fetch_cart(user_id):
    response = requests.get(f"http://localhost:8000/cart/{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Cart is empty.")
        return None


def fetch_product(product_id):
    response = requests.get(f"http://localhost:8000/products/{product_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Product not found.")


def add_to_cart(user_id, product_id, quantity):
    response = requests.post(
        f"http://localhost:8000/cart/{user_id}",
        json={"product_id": product_id, "quantity": quantity},
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to add product to cart.")
        return None
    
def remove_from_cart(user_id, product_id, quantity):
    response = requests.delete(
        f"http://localhost:8000/cart/{user_id}",
        json={"product_id": product_id, "quantity": quantity},
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to remove product from cart.")
        
def checkout_cart(user_id):
    response = requests.post(
        f"http://localhost:8000/cart/{user_id}/checkout",
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to checkout cart.")
        return None
    
def products_layout(product_list):
    cols = st.columns((3, 3, 2))
    cols[0].write("**Product Name**")
    cols[1].write("**Price**")
    for product in product_list:
        cols = st.columns((3, 3, 2))  # Adjust column widths

        cols[0].write(product["name"])
        cols[1].write(product["price"])

        if cols[2].button(f"Add to cart", key=f"add_{product['id']}"):
            add_to_cart(USER_ID, product["id"], 1)
            st.rerun()

def cart_items_layout(cart_items):
    cols = st.columns((3, 3, 2))
    cols[0].write("**Cart ID**")
    cols[1].write("**Product ID**")
    for cart_item in cart_items:
        cols = st.columns((3, 3, 2))  # Adjust column widths

        cols[0].write(cart_item["cart_id"])
        cols[1].write(cart_item["product_id"])

        if cols[2].button(f"Remove from cart", key=f"remove_{cart_item['product_id']}"):
            remove_from_cart(USER_ID, cart_item["product_id"], 1)
            st.rerun()

st.title("ScyllaDB shopping cart example")

st.write("## Products")
products = fetch_products()
st.table(products)

st.write("## Get product by id")
product_id = st.text_input("Enter product id")
if product_id:
    st.write("Query:\n", f"`SELECT * FROM product WHERE id = {product_id};`")
    st.table(fetch_product(product_id))

st.write("## Cart items")
st.write(
    "Query:\n",
    f"`SELECT * FROM cart_items WHERE user_id = {USER_ID} AND cart_id = <active-cart>;`",
)
cart_items = fetch_cart(USER_ID)

if cart_items:
    cart_items_layout(cart_items)


st.write("## Add to cart")
st.write(
    "Query:\n",
    f"`SELECT * FROM cart_items WHERE user_id = {USER_ID} AND cart_id = %s;`",
)
        
products_layout(products)


st.write("## Checkout")
checkout = st.button("Checkout", key="checkout")
st.write(
    "Query:\n",
    f"`UPDATE cart SET is_active = false WHERE user_id = {USER_ID} AND cart_id = <active-cart>`",
)
if checkout:
    response = checkout_cart(USER_ID)
    st.rerun()
    