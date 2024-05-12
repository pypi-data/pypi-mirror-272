import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from creating_tables_and_filling_data import Item, Picture, Sales_Outcome, Trend, Search_Frequency
import os

engine_dict = {
    'data_processing': 'sqlite:///../../FashionTrendForecasting/db_file/FashionAnalysis.db',
    'tests': 'sqlite:///../FashionTrendForecasting/db_file/FashionAnalysis.db',
    'utilities': 'sqlite:///../../../FashionTrendForecasting/db_file/FashionAnalysis.db',
    'routers': 'sqlite:///../../../FashionTrendForecasting/db_file/FashionAnalysis.db'
}

def get_engine():
    current_file = os.path.basename(os.getcwd())
    db_path = engine_dict.get(current_file, 'sqlite:///FashionTrendForecasting/db_file/FashionAnalysis.db')  # Default path if file not found
    return create_engine(db_path)

ENGINE = get_engine()

class CRUD:
    def __init__(self):
        self.engine = ENGINE
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_item_with_details(self, item_data: dict) -> bool:
        """
        Add item with details:
        Adds new item to the table
        Args:
            item_data (dict): Dictionary of new column values

        Returns:
            Bool: True or False
        """
        try:
            # Create the main Item record
            new_item = Item(**{key: value for key, value in item_data.items() if key in Item.__table__.columns})
            self.session.add(new_item)
            self.session.flush()  # Flush to assign an ID to new_item without committing the transaction

            # Add Picture, if present
            if 'picture' in item_data:
                new_picture = Picture(**item_data['picture'], items=[new_item])
                self.session.add(new_picture)

            # Add related Sales_Outcome records, if present
            for sale_data in item_data.get('sales_outcomes', []):
                new_sale = Sales_Outcome(**sale_data, item_id=new_item.item_id)
                self.session.add(new_sale)

            # Add related Trend records, if present
            for trend_data in item_data.get('trends', []):
                new_trend = Trend(**trend_data, item_id=new_item.item_id)
                self.session.add(new_trend)

            # Add related Search_Frequency records, if present
            for search_data in item_data.get('search_frequencies', []):
                new_search = Search_Frequency(**search_data, item_id=new_item.item_id)
                self.session.add(new_search)

            self.session.commit()
            crud_obj = CRUD()
            return crud_obj.get_item_by_id(new_item.item_id)
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error adding item: {e}")
            return False

    def get_items(self):
        try:
            return self.session.query(Item).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving items: {e}")
            return []

    def get_item_data_by_id(self, item_id: int) -> list:
        """
        Get item data by id:
        Gives item information from item table by the given id
        
        Args:
            item_id (int): Item id

        Returns:
            list: item information as a list
        """
        res = None
        try:
            # Query the item from the database
            item = self.session.query(Item).filter(Item.item_id == item_id).one_or_none()
            if item:
                # Create a list of item data you want to return
                res = [
                    item.category,
                    item.material,
                    item.predicted_trend_score,
                ]
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error getting item with id {item_id}: {e}")
        return res

    def get_item_by_id(self, item_id):
        """
        Get item data by id:
        Gives object from item table by the given id

        Args:
            item_id (int): Item id

        Returns:
            obj: Object from item table
        """
        res = None
        try:
            res = self.session.query(Item).filter(Item.item_id == item_id).one_or_none()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error getting item with id {item_id}: {e}")
        return res

    def update_item(self, item_id: int, update_data: dict) -> bool:
        """
        update item
        updates item with the given info

        Args:
            item_id (int): Item id
            update_data (dict): Dictionary of nee data

        Returns:
            bool: True or False
        """
        try:
            result = self.session.query(Item).filter(Item.item_id == item_id).update(update_data)
            if result > 0:
                self.session.commit()
                return True
            else:
                self.session.rollback()
                return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error updating item: {e}")
            return False

    def delete_item(self, item_id: int) -> bool:
        """
        Delete item
        Deletes item with the given id

        Args:
            item_id (int): Item id

        Returns:
            bool: True or False
        """
        try:
            item_to_delete = self.session.query(Item).filter(Item.item_id == item_id).one()
            self.session.delete(item_to_delete)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error deleting item: {e}")
            return False


class Interactions:
    def __init__(self):
        self.engine = ENGINE
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.connect = self.engine.connect()

    def select_all_as_df(self, table_name: str) -> pd.DataFrame:
        """
        Select All Table:
        Returns all rows and columns of the given table.

        Args:
            table_name (str): The table for which to fetch data.

        Returns:
            pd.DataFrame: A DataFrame containing all rows and columns of the table.
        """

        df = pd.read_sql(f"SELECT * FROM {table_name}", self.connect)
        return df

    def get_seasonal_trend_items_top_n_offset_k(self, season: str, n: int, k: int) -> list:
        """
        Seasonal Trend Items:
        Extracts the top n popular items for a specified season based on trend scores.

        Args:
            season (str): The season for which to fetch trend data.
            n (int): The number of top items to return.
            k (int): The number of rows for offset

        Returns:
            list: nested list of the given n items material, category and sum of trend_score.
        """

        query = f"""
        SELECT i.category, i.material, SUM(t.trend_score) as total_trend_score
        FROM Trend t
        JOIN Item i ON t.item_id = i.item_id
        WHERE t.season = '{season}'
        GROUP BY t.item_id
        ORDER BY total_trend_score DESC
        LIMIT {n}
        OFFSET {k}
        """
        df = pd.read_sql(query, self.connect)
        return df.values.tolist()

    def get_popularity_metrics(self) -> pd.DataFrame:
        '''
        Popularity Metrics:
        Functionality: Use the Search_Frequency entity to identify items with the highest search_count, indicating current consumer interest.

        Returns:
            pd.DataFrame: A DataFrame containing item category and material with the max search count.
        '''

        query = """
        SELECT i.category, i.material, MAX(sf.search_count) as max_search_count
        FROM Search_Frequency sf
        JOIN Item i ON sf.item_id = i.item_id
        GROUP BY sf.item_id
        ORDER BY max_search_count DESC
        """
        df = pd.read_sql(query, self.connect)
        return df

    def get_sales_performance(self) -> pd.DataFrame:
        '''
        Sales Performance:
        Functionality: Sales_Outcome to determine which items have the highest sales_volume.

        Returns:
            pd.DataFrame: A DataFrame containing item category and material with total sales volume.
        '''

        query = """
        SELECT i.category, i.material, SUM(so.sales_volume) as total_sales_volume
        FROM Sales_Outcome so
        JOIN Item i ON so.item_id = i.item_id
        GROUP BY so.item_id
        ORDER BY total_sales_volume DESC
        """
        df = pd.read_sql(query, self.connect)
        return df

    def get_detailed_item_trends(self) -> pd.DataFrame:
        '''
        Detailed Item Trends:
        Functionality: Returns detailed attributes of items along with their trend score.

        Returns:
            pd.DataFrame: A DataFrame containing item category, material, style and color with total trend score.
        '''

        query = """
        SELECT i.category, i.material, i.style, i.color, SUM(t.trend_score) as trend_score
        FROM Item i
        JOIN Trend t ON i.item_id = t.item_id
        GROUP BY i.item_id
        ORDER BY trend_score DESC
        """
        df = pd.read_sql(query, self.connect)
        return df

    def get_sales_volume(self) -> pd.DataFrame:
        '''
        Items by Sales Volume:
        Functionality: Returns detailed attributes of items along with their sales volume.

        Returns:
            pd.DataFrame: A DataFrame containing item category, material, style and color with total sales volume and total trend score.
        '''

        query = """
        SELECT i.category, i.material, i.style, i.color, SUM(s.sales_volume) as sales_volume, SUM(t.trend_score) as trend_score
        FROM Item i
        JOIN Trend t ON i.item_id = t.item_id
        JOIN Sales_Outcome s ON i.item_id = s.item_id
        GROUP BY i.item_id
        ORDER BY sales_volume DESC
        """
        df = pd.read_sql(query, self.connect)
        return df

    def get_top_n_items_with_highest_sales(self, season: str, n: int) -> pd.DataFrame:
        '''
        Get item with the highest trend score for a given season.

        Args:
            season (str): The season for which to fetch trend data.
            n (int): The number of top items to return.

        Returns:
            pd.DataFrame: A DataFrame containing the top n items of that season with their name, categories, materials, and total trend scores.
        '''

        query = f"""
        SELECT i.name, i.material, i.category, SUM(t.trend_score) as total_trend_score
        FROM Item i
        JOIN Trend t ON i.item_id = t.item_id
        WHERE t.season = '{season}'
        GROUP BY i.item_id
        ORDER BY SUM(t.trend_score) DESC
        LIMIT {n}
        """
        df = pd.read_sql(query, self.connect)
        return df
