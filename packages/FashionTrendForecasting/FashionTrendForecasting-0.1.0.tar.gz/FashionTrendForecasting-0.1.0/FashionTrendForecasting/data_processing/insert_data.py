from datetime import date

item_record = {
    "name": "Elegant Dress",
    "category": "dresses",
    "material": "wool",
    "style": "casual",
    "color": "Brown",
    "picture": {
        "date_taken": date(2024, 4, 9),
    },
    "sales_outcomes": [
        {
            "sales_volume": 150.0,
            "sales_date": date(2024, 3, 31),
        },
        {
            "sales_volume": 200.0,
            "sales_date": date(2024, 4, 1),
        }
    ],
    "trends": [
        {
            "trend_score": 8.5,
            "trend_date": date(2024, 4, 5),
            "season": "Spring",
        }
    ],
    "search_frequencies": [
        {
            "date_recorded": date(2024, 4, 7),
            "search_count": 500,
        }
    ]
}