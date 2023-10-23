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

# Preprocess the text data for recommendation
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['description'].values.astype('U'))

def recommend_products(query, num_recommendations=3):
    # Transform the user query into a TF-IDF vector
    query_vector = tfidf_vectorizer.transform([query])

    # Compute the cosine similarity between the query and product descriptions
    cosine_sim = linear_kernel(query_vector, tfidf_matrix)

    # Get the indices of the top N similar products
    product_indices = cosine_sim[0].argsort()[::-1][:num_recommendations]

    # Retrieve and return the top N recommended products
    recommended_products = df.iloc[product_indices]
    return recommended_products

while True:
    user_input = input("Enter your product query (type 'exit' to quit): ")
    
    if user_input.lower() == 'exit':
        break

    recommended_products = recommend_products(user_input)
    
    if recommended_products.empty:
        print("No matching products found.")
    else:
        print("Top 3 recommended products:")
        for i, row in recommended_products[['name', 'image_link', 'product_link']][:3].iterrows():
            print(f"Product Name: {row['name']}")
            print(f"Image Link: {row['image_link']}")
            print(f"Product Link: {row['product_link']}")
            print()
