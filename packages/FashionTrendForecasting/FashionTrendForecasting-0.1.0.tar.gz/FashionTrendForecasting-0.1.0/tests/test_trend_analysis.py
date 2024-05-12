from FashionTrendForecasting.trend_analysis.Simple_Model import *

from FashionTrendForecasting.data_processing.sql_interactions import Interactions

interactions = Interactions()
df = interactions.get_sales_volume()
rf_model, rf_mse = train_random_forest(df, 0.2, 42)

# Print the mean squared error
print("Mean Squared Error:", rf_mse)

dt_model, dt_mse = train_decision_tree(df, 0.2, 42)
print("Mean Squared Error:", dt_mse)
gb_model, gb_mse = train_gradient_boosting(df, 0.2, 42)
print("Mean Squared Error:",gb_mse)
