from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List, Tuple, Dict
from beanie import Document
from enum import Enum

from schemas.documents import Purchase, FiscalYearEnum, AcquisitionTypeEnum
from pymongo import DESCENDING


async def count_purchases_in_geographic_area(
    top_left: Tuple[float, float],
    bottom_right: Tuple[float, float]
) -> int:
    """
    Count the number of Purchase records within the specified rectangular geographic area.

    Args:
        top_left (Tuple[float, float]): The (latitude, longitude) of the top-left corner.
        bottom_right (Tuple[float, float]): The (latitude, longitude) of the bottom-right corner.

    Returns:
        int: Number of records within the specified area.
    """
    # Define the rectangular box for querying
    left_lat, left_long = top_left
    right_lat, right_long = bottom_right

    
    count = await Purchase.find(
        {
            Purchase.location_lat <= left_lat,
            Purchase.location_lat >= right_lat,
            Purchase.location_long >= left_long,
            Purchase.location_long <= right_long
        }
    ).count()
    
    return count


async def count_purchases_in_purchase_date_range(start_date: str, end_date: str) -> int:
    """
    Count the number of Purchase records created within a specific date range.

    Args:
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        int: Number of Purchase records within the specified date range.
    """
    # Convert the input strings to datetime objects
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    # Perform the query to count records within the date range
    count = await Purchase.find(
        {
            "purchase_date": {
                "$gte": start_dt,
                "$lte": end_dt
            }
        }
    ).count()
    
    return count



async def get_top_spending_items_by_year(year: int, limit: int = 10) -> List[dict]:
    """
    Get the item names with the highest total spending for a specific year based on purchase_date.

    Args:
        year (int): The year to filter by (e.g., 2023).
        limit (int): The number of top items to return (default is 10).

    Returns:
        List[dict]: A list of dictionaries with item names and their total spending, sorted by highest spending.
    """
    pipeline = [
        {
            "$match": {
                "purchase_date": {
                    "$gte": datetime(year, 1, 1),
                    "$lt": datetime(year + 1, 1, 1)
                }
            }
        },
        {"$group": {"_id": "$item_name", "total_spending": {"$sum": "$total_price"}}},
        {"$sort": {"total_spending": DESCENDING}},
        {"$limit": limit},
        {"$project": {"_id": 0, "item_name": "$_id", "total_spending": 1}}
    ]
    
    # Run the aggregation pipeline
    results = await Purchase.aggregate(pipeline).to_list(length=limit)
    
    return results


async def count_records_by_acquisition_type(acquisition_type: AcquisitionTypeEnum) -> int:
    """
    Count the number of Purchase records based on the specified AcquisitionTypeEnum.

    Args:
        acquisition_type (AcquisitionTypeEnum): The acquisition type to filter by.

    Returns:
        int: Number of records with the specified acquisition type.
    """
    count = await Purchase.find(
        {
            Purchase.acquisition_type == acquisition_type
        }
    ).count()
    
    return count


async def get_total_quantity_by_item_name(item_name: str) -> float:
    """
    Get the total quantity sold for a specific item by its name.

    Args:
        item_name (str): The name of the item.

    Returns:
        float: The total quantity sold for the specified item.
    """
    # MongoDB aggregation pipeline
    pipeline = [
        {"$match": {"item_name": item_name}},  # Filter by item_name
        {"$group": {
            "_id": "$item_name",  # Group by item_name
            "total_quantities": {"$sum": "$quantity"}  # Sum the quantities
        }},
        {"$project": {
            "_id": 0,  # Exclude _id field
            "total_quantities": 1  # Include total_quantities
        }}
    ]
    
    # Run the aggregation pipeline
    result = await Purchase.aggregate(pipeline).to_list(length=1)

    # If no records found, return 0
    if result:
        return result[0]['total_quantities']
    return 0.0


async def get_items_by_purchase_date(date: str) -> List[str]:
    """
    Get the names of items purchased on a specific date.

    Args:
        date (str): The date in 'YYYY-MM-DD' format.

    Returns:
        List[str]: A list of item names purchased on the specified date.
    """
    # Convert the input string date to a datetime object for comparison
    purchase_date = datetime.strptime(date, "%Y-%m-%d")

    # MongoDB aggregation pipeline
    pipeline = [
        {"$match": {"purchase_date": {"$gte": purchase_date, "$lt": purchase_date.replace(hour=23, minute=59, second=59)}}},  # Match the specific date range
        {"$project": {
            "_id": 0,  # Exclude _id field
            "item_name": 1  # Include item_name field
        }},
        {"$group": {
            "_id": "$item_name"  # Group by item_name to avoid duplicates
        }},
        {"$project": {
            "_id": 0,  # Exclude _id field
            "item_name": "$_id"  # Include item_name
        }}
    ]
    
    # Run the aggregation pipeline
    result = await Purchase.aggregate(pipeline).to_list(length=None)

    # Extract item names from the result
    item_names = [doc['item_name'] for doc in result]
    
    return item_names


async def get_family_codes_by_segment_code(segment_code: int) -> List[int]:
    """
    Get all unique family codes for a specific segment code.

    Args:
        segment_code (int): The segment code to filter by.

    Returns:
        List[int]: A list of unique family codes for the specified segment code.
    """
    # MongoDB aggregation pipeline
    pipeline = [
        {"$match": {"segment_code": segment_code}},  # Filter by segment_code
        {"$group": {
            "_id": "$family_code"  # Group by family_code
        }},
        {"$project": {
            "_id": 0,  # Exclude _id field
            "family_code": "$_id"  # Include family_code
        }}
    ]
    
    # Run the aggregation pipeline
    result = await Purchase.aggregate(pipeline).to_list(length=None)

    # Extract family codes from the result
    family_codes = [doc['family_code'] for doc in result]
    
    return family_codes



async def get_top_normalized_UNSPSC() -> List[Dict]:
    pipeline = [
        {"$group": {
            "_id": "$normalized_UNSPSC",  # Group by normalized_UNSPSC
            "count": {"$sum": 1}  # Count the number of occurrences
        }},
        {"$sort": {"count": DESCENDING}},  # Sort by count in descending order
        {"$limit": 10},  # Limit to the top 10 results
        {"$project": {
            "_id": 0,  # Exclude the _id field
            "UNSPSC": "$_id",  # Include normalized_UNSPSC as UNSPSC
            "Count": "$count"  # Include the count of occurrences
        }}
    ]
    
    result = await Purchase.aggregate(pipeline).to_list(length=10)  # Assuming you're using Beanie
    return result


async def get_items_by_unit_price(price: float, less_than: bool = True) -> List[Dict]:
    """
    Get the item names where the unit price is either less than or greater than a specified price.

    Args:
        price (float): The price to compare against.
        less_than (bool): If True, return items with unit price less than the specified price. If False, return items with unit price greater than the specified price.

    Returns:
        List[Dict]: A list of dictionaries with item names and their respective unit prices.
    """
    # Determine the price condition for the match stage
    price_condition = {"$lt": price} if less_than else {"$gt": price}

    # MongoDB aggregation pipeline
    pipeline = [
        {"$match": {"unit_price": price_condition}},  # Filter items based on unit price condition
        {"$group": {
            "_id": "$item_name",  # Group by item_name
            "unit_price": {"$first": "$unit_price"}  # Get the unit price of the item
        }},
        {"$project": {
            "_id": 0,  # Exclude the _id field
            "item_name": "$_id",  # Include the item_name
            "unit_price": 1  # Include the unit price
        }}
    ]
    
    # Run the aggregation pipeline
    result = await Purchase.aggregate(pipeline).to_list()  # Assuming you're using Beanie
    return result


async def get_top_departments() -> List[Dict]:
    """
    Get the top 10 departments with the most orders.

    Returns:
        List[Dict]: A list of dictionaries containing department names and their order counts.
    """
    # MongoDB aggregation pipeline
    pipeline = [
        {"$group": {
            "_id": "$department_name",  # Group by department_name
            "order_count": {"$sum": 1}  # Count the number of orders per department
        }},
        {"$sort": {"order_count": DESCENDING}},  # Sort by order_count in descending order
        {"$limit": 10},  # Limit the result to the top 10
        {"$project": {
            "_id": 0,  # Exclude the _id field
            "department_name": "$_id",  # Include department_name
            "order_count": 1  # Include order_count
        }}
    ]
    
    # Run the aggregation pipeline
    result = await Purchase.aggregate(pipeline).to_list(length=10)  # Assuming you're using Beanie
    return result