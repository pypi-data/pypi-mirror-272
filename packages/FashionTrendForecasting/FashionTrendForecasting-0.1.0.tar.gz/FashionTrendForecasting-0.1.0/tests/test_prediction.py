import pandas as pd
from FashionTrendForecasting.trend_analysis.model import *
from FashionTrendForecasting.data_processing.sql_interactions import Interactions, CRUD

# Define new data as a DataFrame
new_data = pd.DataFrame({
    'category': ['dresses', 'tops', 'pants'],
    'material': ['cotton', 'polyester', 'wool'],
    'style': ['casual', 'formal', 'sporty'],
    'color': ['blue', 'black', 'red'],
    'sales_volume': [200, 150, 100],
    'max_search_count': [500, 450, 400],
    'total_sales_volume': [1000, 800, 600],
})

# Database interaction setup
crud = CRUD()
interactions = Interactions()

# Retrieve and prepare training data
df = interactions.get_sales_volume()
X_train, y_train = split_data(df, 'trend_score')

# Model training and prediction
y_pred_rf = train_and_predict_rf(X_train, y_train, new_data, 100, 42)
print(y_pred_rf)

y_pred_dt = train_and_predict_dt(X_train, y_train, new_data, 42)
print(y_pred_dt)

y_pred_gb = train_and_predict_dt(X_train, y_train, new_data, 41)
print(y_pred_gb)

# Adding items to the database and updating with predicted trend scores
items = new_data.to_dict(orient='records')
predicted_scores = [128.0686, 125.225, 110.0611]

for item_id in range(101, 104):
    for item, score in zip(items, predicted_scores):
        crud.add_item_with_details(item)
        crud.update_item(item_id, {"predicted_trend_score": float(score)})

# Fetching updated items from the database
for item_id in range(101, 104):
    print(crud.get_item_data_by_id(item_id))
