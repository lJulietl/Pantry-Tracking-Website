import streamlit as st
import pandas as pd
from datetime import datetime
from fractions import Fraction

# Define categories and their corresponding items
categories = {
    "Produce": ["Apples", "Bananas", "Oranges", "Persimmons",
                "Tomatoes", "Potatoes", "Eggplants", "Onions",
                "Zucchinis", "Carrots"],
    "Meat": ["Chicken", "Beef", "Eggs", "Fish (General)"],
    "Dairy": ["Milk", "Cheese", "Yogurt"],
    "Canned/Jarred Foods": ["Tomato Sauce", "Canned Beans", "Jam"],
    "Dry/Baking Goods": ["Flour", "Sugar", "Pasta", "Rice", "Baking Soda"],
    "Personal Care": ["Condoms", "Pads", "Tampons", "Menstrual Cups",
                      "Floss"]
}

# Sort items in each category
for category, items in categories.items():
    categories[category] = sorted(items)

# CSV file to store data
csv_file = "product_data.csv"

# CSS for styling
background_image_css = """
<style>
    [data-testid="stAppViewContainer"] {
        background-image: url('https://thepantry.ucdavis.edu/sites/g/files/dgvnsk13406/files/logo-white-transparentbg.png'), 
                          url('https://static.vecteezy.com/system/resources/previews/009/003/028/non_2x/organic-food-and-fruit-shopping-background-free-vector.jpg');
        background-size: 165px, cover;
        background-position: 85% 20%;
        background-repeat: no-repeat, no-repeat;
        background-attachment: fixed, fixed;
    }
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
</style>
"""
st.markdown(background_image_css, unsafe_allow_html=True)

# Title
st.title("Shelf Stock Tracking System")

# Tabs
tab1, tab2 = st.tabs(["Products Distributed", "Products Left At End Of Day/Data Overview"])

# Function to handle fraction input
def handle_fraction_input(quantity_input):
    try:
        return float(Fraction(quantity_input))
    except:
        return float(quantity_input)

# Helper function to save data to CSV
def save_to_csv(data):
    try:
        existing_data = pd.read_csv(csv_file)
    except FileNotFoundError:
        existing_data = pd.DataFrame(columns=["Date", "Category", "Product", "Total Distributed"])
    updated_data = pd.concat([existing_data, data], ignore_index=True)
    grouped_data = updated_data.groupby(["Date", "Category", "Product"], as_index=False).sum()
    grouped_data.to_csv(csv_file, index=False)
    return grouped_data

# Tab 1: Add New Product Entry
with tab1:
    st.markdown("""
    ### Instructions for Adding Products
    1. **Select a Category** from the dropdown.
    2. **Select a Product** or enter a custom product name.
    3. **Enter the Quantity Distributed**. Fractions are supported (e.g., `2.5` or `3/4`).
    """)

    # Select a category
    category = st.selectbox("Select Category", options=list(categories.keys()))

    # Select product or custom product
    products = categories[category]
    selected_product = st.selectbox("Select Product or Add Custom", options=products + ["Other (Custom Product)"])
    custom_product_name = st.text_input("Enter custom product name:") if selected_product == "Other (Custom Product)" else selected_product

    # Input quantity
    initial_quantity_input = st.text_input("Quantity Distributed (e.g., 2.5 or 3/4):")
    initial_quantity = handle_fraction_input(initial_quantity_input) if initial_quantity_input else 0

    # Automatically save on change
    if custom_product_name and initial_quantity:
        today = datetime.today().strftime('%Y-%m-%d')
        new_data = pd.DataFrame([{
            "Date": today,
            "Category": category,
            "Product": custom_product_name,
            "Total Distributed": initial_quantity
        }])
        save_to_csv(new_data)
        st.success(f"Product '{custom_product_name}' added with quantity {initial_quantity}.")

# Tab 2: Data Overview
with tab2:
    st.markdown("""
    ### Data Overview
    View or update remaining quantities of products.
    """)
    try:
        data = pd.read_csv(csv_file)
        st.dataframe(data)

        # Provide a download link for the CSV
        csv_data = data.to_csv(index=False)
        st.markdown(
            f'<a href="data:file/csv;base64,{st.session_state.base64_csv}" download="{csv_file}">Download Updated Data</a>',
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("No data available.")
