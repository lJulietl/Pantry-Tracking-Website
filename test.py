import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import os

PRODUCT_CATEGORIES = ["Produce", "Meat", 
"Dairy", "Canned/Jarred Foods", "Dry/Baking Goods", "Personal Care"]

# CSS for consistent styling
background_image_css = """
<style>
    /* Background for the app */
    [data-testid="stAppViewContainer"] {
        background-image: url('https://thepantry.ucdavis.edu/sites/g/files/dgvnsk13406/files/logo-white-transparentbg.png'), 
                          url('https://static.vecteezy.com/system/resources/previews/009/003/028/non_2x/organic-food-and-fruit-shopping-background-free-vector.jpg');
        background-size: 265px, cover;
        background-position: 820px 96%, center;
        background-repeat: no-repeat, no-repeat;
        background-attachment: fixed, fixed;
    }

    /* Product grid layout */
    .product-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        justify-content: center;
        align-items: center;
    }

    .product-item {
        text-align: center;
        padding: 10px;
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        border-radius: 12px;
        transition: transform 0.3s ease-in-out;
    }

    .product-item:hover {
        transform: scale(1.05);
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
    }

    .product-img {
        width: 150px;
        height: 150px;
        object-fit: cover;
        border-radius: 8px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        margin: 0 auto;
        display: block;
    }

    .product-item p {
        font-weight: bold;
        font-size: 14px;
        margin-top: 10px;
    }

    .product-item input,
    .product-item label {
        margin-top: 10px;
    }

    .stButton > button {
        width: 100%;
        padding: 12px;
        font-size: 16px;
        border-radius: 8px;
        margin-top: 10px;
    }
    
    .st-emotion-cache-1b0udgb {
        color: rgb(49, 51, 63);
    }
</style>
"""
st.markdown(background_image_css, unsafe_allow_html=True)

# Resize images to ensure consistency
def resize_image(image_path, size=(150, 150)):
    try:
        img = Image.open(image_path)
        img = img.resize(size, Image.Resampling.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
        return img
    except Exception as e:
        st.warning(f"Error loading image {image_path}: {e}")
        return None

# Function to list products
def list_products_in_rows(products, dir_path):
    rows = [products[i:i + 3] for i in range(0, len(products), 3)]  # Group products into rows of 3
    for row in rows:
        cols = st.columns(3)  # Create three columns for each row
        for col, product in zip(cols, row):
            image_path = f"{dir_path}/{product}"
            product_name = os.path.splitext(product)[0]

            with col:
                # Resize and display the image
                resized_img = resize_image(image_path)
                if resized_img:
                    st.image(resized_img, caption=product_name, use_column_width=True)
                else:
                    st.warning(f"Image not available for {product_name}")
                
                # Add input fields and checkbox
                st.number_input(f"Enter Quantity for {product_name}", min_value=1, step=1, key=f"quantity_{product_name}")
                st.number_input(f"Quantity left for {product_name} at the end of the day", min_value=1, step=1, key=f"quantity_end_{product_name}")
                st.checkbox(f"Check if {product_name} is logged and on the shelf", key=f"checkbox_{product_name}")

st.title("Shelf Stock Tracking System")

# Create tabs
tabs = st.tabs(["Add New Product Entry"] + PRODUCT_CATEGORIES + ["Data Overview"])

# Tab 1: Add New Product Entry
with tabs[0]:
    st.header("Add New Product Entry")
    with st.form("product_form"):
        category = st.selectbox("Select Category", options=["Menstrual Product", "Produces"])
        product_name = st.text_input("Enter Product Name")
        initial_quantity = st.number_input("Enter Initial Quantity", min_value=1, step=1)
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        st.success(f"Data submitted successfully for {product_name} in {category} category.")

# Tabs for each category
for index, category in enumerate(PRODUCT_CATEGORIES):
    with tabs[index + 1]:
        dir_path = f"Product_Categories/{category}"
        st.header(category)

        if not os.path.exists(dir_path):
            st.info(f"No products available in {category}.")
            continue

        products = os.listdir(dir_path)
        list_products_in_rows(products, dir_path)  # Call the function to display products in rows of 3

# Tab for Data Overview
with tabs[-1]:
    st.header("Data Overview")
    if st.checkbox("Show Menstrual Product Data"):
        st.dataframe(pd.DataFrame({
            "Timeframe": ["2024-11-01", "2024-11-02"],
            "Product Name": ["Tampon", "Pad"],
            "Quantity": [50, 30]
        }))
    if st.checkbox("Show Produces Data"):
        st.dataframe(pd.DataFrame({
            "Timeframe": ["2024-11-01", "2024-11-02"],
            "Product Name": ["Apple", "Banana"],
            "Quantity": [100, 150]
        }))
