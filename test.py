import streamlit as st
import pandas as pd
from datetime import datetime 
from PIL import Image
import os

PRODUCT_CATEGORIES = ["Produce", "Meat", 
"Dairy", "Canned/Jarred Foods", "Dry/Baking Goods", "Personal Care"]

def list_product(image, product_name, col):
    with col:
        # Display the Carrots image on the left column with a width of 150 pixels
        st.image(image, caption=product_name, width=150)
        # Enter quantity for Carrots
        quantity = st.number_input("Enter Quantity for " + product_name, min_value=1, step=1)

# CSS for enhanced styling
background_image_css = """
<style>
    /* Center align content */
    .main {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding-top: 50px;
    }
    
    /* Background for the app */
    [data-testid="stAppViewContainer"] {
        background-image: url('https://thepantry.ucdavis.edu/sites/g/files/dgvnsk13406/files/logo-white-transparentbg.png'), 
                          url('https://static.vecteezy.com/system/resources/previews/009/003/028/non_2x/organic-food-and-fruit-shopping-background-free-vector.jpg');
        background-size: 265px, cover; /* Set the sizes for each image */
        background-position: 820px 96%, center; /* Position of each background */
        background-repeat: no-repeat, no-repeat;
        background-attachment: fixed, fixed;
    }
    
    /* Transparent header */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    
    /* Wrapper for content with styling */
    .content-wrapper {
        background-color: rgba(255, 255, 255, 0.9); /* White with transparency */
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
        max-width: 500px;
        width: 100%;
        text-align: center;
        margin-top: 20px;
    }

    /* Style the submit and undo buttons */
    .stButton>button {
        width: 100%;
        padding: 12px;
        font-size: 16px;
        border-radius: 8px;
        margin-top: 10px;
    }
    
    /* Submit button styling */
    .stButton>button:first-child {
        background-color: #4CAF50; /* Green color */
        color: white;
    }

    /* Undo button styling */
    .stButton>button:last-child {
        background-color: #FF6F61; /* Coral color for Undo button */
        color: white;
    }
</style>
"""

# Inject CSS for styling
st.markdown(background_image_css, unsafe_allow_html=True)

# Sample data (replace with real data loading if needed)
df_menstrual = pd.DataFrame({
    "Timeframe": ["2024-11-01", "2024-11-02"],
    "Product Name": ["Tampon", "Pad"],
    "Quantity": [50, 30]
})

df_produces = pd.DataFrame({
    "Timeframe": ["2024-11-01", "2024-11-02"],
    "Product Name": ["Apple", "Banana"],
    "Quantity": [100, 150]
})

st.title("Shelf Stock Tracking System")

# Create tabs
tabs = st.tabs(["Add New Product Entry"] + PRODUCT_CATEGORIES +
["Data Overview"])

# Tab 1: Add New Product Entry
with tabs[0]:
    st.header("Add New Product Entry")
    with st.form("product_form"):
        category = st.selectbox("Select Category", options=["Menstrual Product", "Produces"])
        product_name = st.text_input("Enter Product Name")
        initial_quantity = st.number_input("Enter Initial Quantity", min_value=1, step=1)
        submit_button = st.form_submit_button("Submit")

    # Handle submission
    if submit_button:
        # Record start time
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        new_row = [
            datetime.today().strftime("%Y-%m-%d"), product_name, initial_quantity
        ]
        
        st.success(f"Data submitted successfully for {product_name} in {category} category.")
        st.info(f"Initial stock: {initial_quantity}, Start time: {start_time}")


for index, catagory in enumerate(PRODUCT_CATEGORIES):
    with tabs[index + 1]:
        dir_path = "Product_Categories/" + catagory
        st.header(catagory)

        if (not os.path.exists(dir_path)):
            continue

        products = os.listdir(dir_path)

        images = []
        for product in products:
            images.append(Image.open(dir_path+"/"+product))

        type_of_diff_products = len(products)
        products_in_row = 3
        index = 0
        while index < type_of_diff_products :
            cols = st.columns(min(type_of_diff_products - index, products_in_row))
            for col in cols:
                with col:
                    if index < type_of_diff_products:
                        list_product(images[index], products[index].split(".")[0], col)
                        st.number_input(f"Quantity left for {product_name} at the end of the day",min_value=1,step=1,key=f"quantity_{col}")
                        st.checkbox(f"Check if {product_name} is logged and on the shelf",key=f"checkbox_{col}")
                        index += 1

# Tab 3: Data Overview
with tabs[7]:
    st.header("Data Overview")
    if st.checkbox("Show Menstrual Product Data"):
        st.dataframe(df_menstrual)
    if st.checkbox("Show Produces Data"):
        st.dataframe(df_produces)
