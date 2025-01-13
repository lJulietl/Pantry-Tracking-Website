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

# CSV file to store data (you can change the path if necessary)
csv_file = "product_data.csv"

# CSS for styling
background_image_css = """
<style>
    [data-testid="stAppViewContainer"] {
        background-image: url('https://thepantry.ucdavis.edu/sites/g/files/dgvnsk13406/files/logo-white-transparentbg.png'), 
                          url('https://static.vecteezy.com/system/resources/previews/009/003/028/non_2x/organic-food-and-fruit-shopping-background-free-vector.jpg');
        background-size: 165px, cover;
        background-position: 85% 20%; /* Move logo slightly left and down */
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

# Initialize session state for category, product, and quantity if not already set
if 'category' not in st.session_state:
    st.session_state['category'] = list(categories.keys())[0]
if 'product' not in st.session_state:
    st.session_state['product'] = categories[st.session_state['category']][0]
if 'quantity' not in st.session_state:
    st.session_state['quantity'] = 0

# Function to handle fraction input
def handle_fraction_input(quantity_input):
    try:
        # Try converting the input to a fraction
        return float(Fraction(quantity_input))
    except:
        # If conversion fails, return the input as a number
        return float(quantity_input)

# Tab 1: Add New Product Entry
with tab1:
    st.markdown("""
    ### Instructions for Adding Products
    1. **Select a Category** from the dropdown
    2. **Select a Product** from the list of items in the selected category. You can also enter a custom product by selecting "Other (Custom Product)".
    3. **Enter the Quantity Distributed**: You can enter whole numbers for dry products or products that are easier to count. You may use fractions (e.g., `2` or `3/4`) to indicate how full the crates are for products that are harder to count like produce.
    4. Once you've entered the information, click **Submit** to save the data.
    """)
    
    # Select a category
    category = st.selectbox(
        "Select Category", 
        options=list(categories.keys()), 
        index=list(categories.keys()).index(st.session_state['category'])
    )
    
    # If category has changed, reset the product to the first one of the new category
    if category != st.session_state['category']:
        st.session_state['category'] = category
        st.session_state['product'] = categories[category][0]  # Reset product to the first one in new category

    # Update list of products based on the selected category
    products = categories[category]

    # Select product
    selected_product = st.selectbox(
        f"Select a product from {category} or enter a custom product", 
        options=products + ["Other (Custom Product)"],
        index=products.index(st.session_state['product']) if st.session_state['product'] in products else 0,
        key="product_select"
    )

    # Check if custom product is selected
    if selected_product == "Other (Custom Product)":
        custom_product_name = st.text_input("Enter custom product name:")
    else:
        custom_product_name = selected_product
        st.session_state['product'] = custom_product_name  # Update the product in session state

    # Input quantity (allowing fractions)
    initial_quantity_input = st.text_input("Quantity Distributed (You can enter fractions, e.g. 2.5 or 3/4):")
    if initial_quantity_input:
        initial_quantity = handle_fraction_input(initial_quantity_input)
    else:
        initial_quantity = 0

    # Submit button
    submit_button = st.button("Submit")

    # Handle submission
    if submit_button:
        # Save data to session state
        st.session_state['product'] = custom_product_name
        st.session_state['quantity'] = initial_quantity
        st.success(f"Product '{custom_product_name}' in category '{category}' added with initial quantity: {initial_quantity}")

        # Save data to CSV file
        today = datetime.today().strftime('%Y-%m-%d')  # Get today's date
        data = {
            "Date": today,
            "Category": category,
            "Product": custom_product_name,
            "Total Distributed": initial_quantity  # Update to "Total Distributed"
        }
        
        # Convert to DataFrame
        new_entry = pd.DataFrame([data])
        
        # If CSV file exists, append new data, otherwise create a new CSV file
        try:
            existing_data = pd.read_csv(csv_file)
        except FileNotFoundError:
            # If the file doesn't exist, create a new one
            existing_data = pd.DataFrame(columns=["Date", "Category", "Product", "Total Distributed"])

        # Concatenate new data with the existing data
        updated_data = pd.concat([existing_data, new_entry], ignore_index=True)
        # Group by 'Date', 'Category', and 'Product', and sum the 'Total Distributed' column
        grouped_data = updated_data.groupby(["Date", "Category", "Product"], as_index=False).sum()

        # Save the grouped data to CSV
        grouped_data.to_csv(csv_file, index=False)

# Tab 2: Data Overview
with tab2:
    st.markdown("""
    ### Instructions for Updating Products Left at the End of the Day
    1. **Select a Category**: Choose the category of the product you want to update from the dropdown.
    2. **Select a Product**: After selecting a category, pick a product from the list of available items.
    3. **Enter the Remaining Quantity**: Input the quantity of the selected product that is left at the end of the day. Like tab 1, you can enter both whole numbers or fractions (e.g., `2` or `3/4`) for products distributed in crates.
    4. Once you've entered the remaining quantity, click **Update Quantities** to save the data.
    5. The total quantity distributed will automatically update, reflecting the total products distributed per day.
    6. **Note**: If the products left exceed the total quantity distributed, an error will be shown.
    """)

    # Load existing data from CSV
    try:
        data = pd.read_csv(csv_file)

        # Select category and product for updating remaining quantity
        category_tab2 = st.selectbox(
            "Select Category for Products Left",
            options=list(categories.keys())
        )
        
        # Update list of products based on selected category
        products_tab2 = categories[category_tab2]
        
        selected_product_tab2 = st.selectbox(
            f"Select a product from {category_tab2} to update the remaining quantity:",
            options=products_tab2
        )

        # Input the "Products Left" quantity (fractions allowed)
        products_left_input = st.text_input(
            f"Enter the number of '{selected_product_tab2}' left at the end of the day (fractions allowed):"
        )
        if products_left_input:
            products_left = handle_fraction_input(products_left_input)
        else:
            products_left = 0

        # Submit button for updating the quantities
        update_button = st.button("Update Quantities")

        if update_button:
            # Get today's date
            today_date = datetime.today().strftime('%Y-%m-%d')

            # Filter data for today's selected product and category
            product_data = data[
                (data["Category"] == category_tab2) & 
                (data["Product"] == selected_product_tab2) & 
                (data["Date"] == today_date)
            ]
            
            if not product_data.empty:
                # If the product already exists for today, update the total distributed quantity
                total_distributed = product_data["Total Distributed"].values[0]
                total_left = products_left
                
                # Ensure that the "remaining quantity" doesn't exceed the "distributed quantity"
                if total_left > total_distributed:
                    st.error(f"The remaining quantity cannot exceed the distributed quantity for '{selected_product_tab2}'.")
                else:
                    # Subtract the remaining quantity from the distributed quantity
                    total_quantity = total_distributed - total_left
                    
                    # Update the value in the DataFrame
                    data.loc[
                        (data["Category"] == category_tab2) &
                        (data["Product"] == selected_product_tab2) &
                        (data["Date"] == today_date), "Total Distributed"
                    ] = total_quantity
                    
                    # Save the updated data back to the CSV file
                    data.to_csv(csv_file, index=False)
                    
                    # Show success message
                    st.success(f"Quantity for '{selected_product_tab2}' updated successfully!")

                    # Only display the updated dataset
                    st.markdown("### Updated Data:")
                    st.dataframe(data.sort_values(by='Date', ascending=False))

            else:
                st.warning(f"No product data found for '{selected_product_tab2}' today. Please add the product first.")
    except FileNotFoundError:
        st.warning("No data available.")
