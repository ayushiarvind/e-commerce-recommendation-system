# Imports
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from pymongo import MongoClient
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
from flask import Flask, jsonify, request
from flask_cors import CORS

# Enable CORS for all routes
app = Flask(__name__)
CORS(app)  # Allow requests from other domains

### 1. Data Handling
# Sample dataset
raw_data = pd.DataFrame({
    'user_id': [1, 1, 2, 2, 3, 3, 4, 4],
    'item_id': [101, 102, 101, 103, 104, 105, 106, 107],
    'rating': [5, 4, 4, 3, 5, 4, 3, 4]
})

# Preprocess data
scaler = MinMaxScaler()
user_item_matrix = raw_data.pivot(index='user_id', columns='item_id', values='rating').fillna(0)
normalized_matrix = scaler.fit_transform(user_item_matrix)
normalized_df = pd.DataFrame(normalized_matrix, index=user_item_matrix.index, columns=user_item_matrix.columns)

### 2. Database Integration (MongoDB)
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce_recommendations']
collection = db['user_item_data']

# Insert data into MongoDB if not already present
if collection.count_documents({}) == 0:
    raw_data_dict = raw_data.to_dict('records')
    collection.insert_many(raw_data_dict)

# Fetch data from MongoDB
retrieved_data = pd.DataFrame(list(collection.find())).drop('_id', axis=1)
print("Data from MongoDB:", retrieved_data)

### 3. Collaborative Filtering with Surprise
# Prepare data for Surprise
reader = Reader(rating_scale=(1, 5))
surprise_data = Dataset.load_from_df(raw_data[['user_id', 'item_id', 'rating']], reader)
trainset, testset = train_test_split(surprise_data, test_size=0.2)

# Train an SVD model
svd_model = SVD()
svd_model.fit(trainset)

# Generate predictions
predictions = svd_model.test(testset)
print("Predictions:", predictions[:5])

# Recommendation for a specific user
user_id = 1
items = raw_data['item_id'].unique()
unrated_items = [item for item in items if raw_data.loc[(raw_data['user_id'] == user_id) & (raw_data['item_id'] == item)].empty]

user_recommendations = [(item, svd_model.predict(user_id, item).est) for item in unrated_items]
user_recommendations.sort(key=lambda x: x[1], reverse=True)
print(f"Top recommendations for user {user_id}:", user_recommendations[:5])

### 4. Evaluation
# Evaluate model accuracy
mae = accuracy.mae(predictions)
rmse = accuracy.rmse(predictions)
print(f"Mean Absolute Error: {mae}\nRoot Mean Square Error: {rmse}")

### 5. Real-Time Integration
# Flask API for real-time recommendations
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the E-Commerce Recommendation System API. Use the /recommend endpoint to get recommendations."})

@app.route('/recommend', methods=['GET'])
def recommend():
    try:
        user_id = int(request.args.get('user_id'))
        top_n = int(request.args.get('top_n', 5))

        # Generate recommendations for the user
        unrated_items = [item for item in items if raw_data.loc[(raw_data['user_id'] == user_id) & (raw_data['item_id'] == item)].empty]
        user_recommendations = [(item, svd_model.predict(user_id, item).est) for item in unrated_items]
        
        # Sort recommendations by predicted rating in descending order
        user_recommendations.sort(key=lambda x: x[1], reverse=True)

        # Convert to JSON-serializable format (standard Python types)
        recommendations = [
            [int(item), float(rating)] for item, rating in user_recommendations[:top_n]
        ]
        
        return jsonify({
            'user_id': user_id,
            'recommendations': recommendations
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
