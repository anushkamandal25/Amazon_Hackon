import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Read the data into a pandas DataFrame
query = "SELECT * FROM chatbot_product"
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Remove non-numeric characters from the 'price' and 'rating' columns and convert to float
df['price'] = df['price'].str.replace('[^\d.]', '', regex=True).astype(float)
df['rating'] = df['rating'].str.extract('(\d+\.?\d*)').astype(float)

# Preprocess the text data for recommendation
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['description'].values.astype('U'))

def extract_info(query):
    # Initialize default values for product name, price, and rating
    product_name = None
    price_max = None
    rating_min = None
    
    # Split the query into words
    words = query.split()
    
    # Extract product name
    for word in words:
        if word.lower() != 'under' and word.lower() != 'rating' and not word.isnumeric():
            product_name = word
    
    # Extract price (if any)
    for i, word in enumerate(words):
        if word.lower() == 'under':
            if i + 1 < len(words) and words[i + 1].isnumeric():
                price_max = float(words[i + 1])
                break
    
    # Extract rating (if any)
    for word in words:
        if word.startswith("rating"):
            try:
                rating_min = float(word.split("rating")[1])
            except ValueError:
                pass
    for i, word in enumerate(words):
        if word.lower() == 'rating':
            if i + 1 < len(words) and words[i + 1].isnumeric():
                rating_min = float(words[i + 1])            
                break
    return product_name, price_max, rating_min

def recommend_products(query, price_max, rating_min, num_recommendations=3):
    product_name, price_max, rating_min = extract_info(query)
    
    if product_name:
        # Filter by category (search for the product name in the 'category' column)
        filtered_products = df[df['category'].str.contains(product_name, case=False)]
        
        if not filtered_products.empty:
            # Filter by price
            if price_max:
                filtered_products = filtered_products[filtered_products['price'] <= price_max]

            # Filter by rating
            if rating_min:
                filtered_products = filtered_products[filtered_products['rating'] >= rating_min]

            # Sort by highest rating
            filtered_products = filtered_products.sort_values(by='rating', ascending=False)

            return filtered_products.head(num_recommendations)
    
    return pd.DataFrame()  # No matching products found

while True:
    user_message = input("Enter your product query (type 'exit' to quit): ")

    if user_message.lower() == 'exit':
        break
    
    if user_message.lower() in ["hi", "hello", "how are you?"]:
        print("Enter the product you are looking for.")
        continue

    recommended_products = recommend_products(user_message, None, None)

    if recommended_products.empty:
        print("No matching products found.")
    else:
        print("Top 3 recommended products:")
        for i, row in recommended_products[['name', 'image_link', 'product_link']].head(3).iterrows():
            print(f"Product Name: {row['name']}")
            print(f"Image Link: {row['image_link']}")
            print(f"Product Link: {row['product_link']}")
            print()
