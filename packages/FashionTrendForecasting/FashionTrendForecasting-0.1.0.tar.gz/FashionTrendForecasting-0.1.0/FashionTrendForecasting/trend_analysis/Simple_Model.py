from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def train_random_forest(df, test_size, random_state):
    X = df[['category', 'material', 'style', 'color']]
    y = df['trend_score']

    # Create a pipeline to preprocess categorical features
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features)
        ], remainder='passthrough')

    # Preprocess features
    X = preprocessor.fit_transform(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Train RandomForestRegressor
    rf = RandomForestRegressor(n_estimators=100, random_state=random_state)
    rf.fit(X_train, y_train)

    # Predict on test data
    y_pred = rf.predict(X_test)

    # Calculate MSE
    mse = mean_squared_error(y_test, y_pred)

    return rf, mse


def train_decision_tree(df, test_size, random_state):
    X = df[['category', 'material', 'style', 'color']]
    y = df['trend_score']

    # Create a pipeline to preprocess categorical features
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features)
        ], remainder='passthrough')

    # Preprocess features
    X = preprocessor.fit_transform(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Train DecisionTreeRegressor
    dt = DecisionTreeRegressor(random_state=random_state)
    dt.fit(X_train, y_train)

    # Predict on test data
    y_pred = dt.predict(X_test)

    # Calculate MSE
    mse = mean_squared_error(y_test, y_pred)

    return dt, mse


def train_gradient_boosting(df, test_size, random_state):
    X = df[['category', 'material', 'style', 'color']]
    y = df['trend_score']

    # Create a pipeline to preprocess categorical features
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features)
        ], remainder='passthrough')

    # Preprocess features
    X = preprocessor.fit_transform(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Train GradientBoostingRegressor
    gb = GradientBoostingRegressor(random_state=random_state)
    gb.fit(X_train, y_train)

    # Predict on test data
    y_pred = gb.predict(X_test)

    # Calculate MSE
    mse = mean_squared_error(y_test, y_pred)

    return gb, mse
