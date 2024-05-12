from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor

def split_data(data, target_feature):
    y_train = data[target_feature]
    X_train = data.drop(columns=[target_feature])

    return X_train, y_train
    
def train_and_predict_rf(X_train, y_train, new_data, n_estimators, random_state):
    # Determine categorical features
    categorical_features = X_train.select_dtypes(include=['object']).columns.tolist()

    # Create a pipeline to preprocess categorical features
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features)
        ], remainder='passthrough')

    # Create the Random Forest model pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=n_estimators, random_state=random_state))
    ])

    # Train the model
    model.fit(X_train, y_train)

    # Predict on new data
    y_pred = model.predict(new_data)

    return y_pred


def train_and_predict_dt(X_train, y_train, new_data, random_state):
    categorical_features = X_train.select_dtypes(include=['object']).columns.tolist()

    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features)
        ], remainder='passthrough')

    # Create the Decision Tree model pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', DecisionTreeRegressor(random_state=random_state))
    ])

    # Train the model
    model.fit(X_train, y_train)

    # Predict on new data
    y_pred = model.predict(new_data)

    return y_pred

def train_and_predict_gb(X_train, y_train, new_data, random_state):
    categorical_features = X_train.select_dtypes(include=['object']).columns.tolist()

    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features)
        ], remainder='passthrough')

    # Create the Gradient Boosting model pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', GradientBoostingRegressor(random_state=random_state))
    ])

    # Train the model
    model.fit(X_train, y_train)

    # Predict on new data
    y_pred = model.predict(new_data)

    return y_pred
