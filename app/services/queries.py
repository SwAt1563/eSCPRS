from datetime import datetime
from typing import Callable, Dict, List, Tuple

from pymongo import DESCENDING

from schemas.documents import AcquisitionTypeEnum, FiscalYearEnum, Purchase


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
        Purchase.location_lat <= left_lat,
        Purchase.location_lat >= right_lat,
        Purchase.location_long >= left_long,
        Purchase.location_long <= right_long
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
      
        Purchase.acquisition_type == acquisition_type
       
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
        {"$match": {"segment": segment_code}},  # Filter by segment_code
        {"$group": {
            "_id": "$family"  # Group by family_code
        }},
        {"$project": {
            "_id": 0,  # Exclude _id field
            "family": "$_id"  # Include family_code
        }}
    ]

    
    # Run the aggregation pipeline
    result = await Purchase.aggregate(pipeline).to_list(length=None)

    # Extract family codes from the result
    family_codes = [doc['family'] for doc in result]
    
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


async def get_top_item_by_total_price(fiscal_year: FiscalYearEnum) -> Dict:
    """
    Get the item name with the highest total price for a specific fiscal year.

    Args:
        fiscal_year (FiscalYearEnum): The fiscal year to filter by.

    Returns:
        Dict: A dictionary containing the item name and the total price.
    """
    # MongoDB aggregation pipeline
    pipeline = [
        {"$match": {"fiscal_year": fiscal_year}},  # Filter by fiscal year
        {"$group": {
            "_id": "$item_name",  # Group by item_name
            "total_price": {"$sum": "$total_price"}  # Sum the total price for each item
        }},
        {"$sort": {"total_price": -1}},  # Sort by total_price in descending order
        {"$limit": 5},  # Limit to the top item
        {"$project": {
            "_id": 0,  # Exclude the _id field
            "item_name": "$_id",  # Include the item_name
            "total_price": 1  # Include the total price
        }}
    ]
    
    # Run the aggregation pipeline
    result = await Purchase.aggregate(pipeline).to_list(length=5)

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

async def get_top_suppliers_by_purchase_count(top_n: int = 5) -> List[Dict]:
    """
    Get the top suppliers based on the number of purchases across all fiscal years.

    Args:
        top_n (int): The number of top suppliers to return.

    Returns:
        List[Dict]: A list of dictionaries containing supplier name, zip code, and the count of purchases.
    """
    # MongoDB aggregation pipeline
    pipeline = [
        {"$group": {
            "_id": {
                "supplier_name": "$supplier_name",  # Group by supplier_name
                "supplier_zip": "$supplier_zip_code"  # Group by supplier_zip_code
            },
            "purchase_count": {"$sum": 1}  # Count the number of purchases for each supplier
        }},
        {"$sort": {"purchase_count": -1}},  # Sort by purchase_count in descending order
        {"$limit": top_n},  # Limit the result to the top 'n' suppliers
        {"$project": {
            "_id": 0,  # Exclude the _id field
            "supplier_name": "$_id.supplier_name",  # Include supplier_name
            "supplier_zip_code": "$_id.supplier_zip",  # Include supplier_zip_code
            "purchase_count": 1  # Include the count of purchases
        }}
    ]
    
    # Run the aggregation pipeline
    result = await Purchase.aggregate(pipeline).to_list(length=top_n)

    # Return the result
    return result



# Create a dictionary to map function numbers to actual functions
function_map: Dict[int, Callable] = {
    1: count_purchases_in_geographic_area,
    2: count_purchases_in_purchase_date_range,
    3: get_top_spending_items_by_year,
    4: count_records_by_acquisition_type,
    5: get_total_quantity_by_item_name,
    6: get_items_by_purchase_date,
    7: get_family_codes_by_segment_code,
    8: get_top_normalized_UNSPSC,
    9: get_top_item_by_total_price,
    10: get_top_departments,
    11: get_top_suppliers_by_purchase_count
}

# Function to invoke a function based on function number and parameters
async def invoke_function(function_data: dict):
    # Extract function number and parameters
    function_number = function_data.get("function_number")
    parameters = function_data.get("parameters", {})

    # Get the function from the mapping
    function_to_invoke = function_map.get(function_number)

    if function_to_invoke:
        # Dynamically call the function with the parameters
        result = await function_to_invoke(**parameters)
        return {'function_name': function_to_invoke.__name__, 'result': result}
    
    return 'Your query is not clear. Please write vaild question.'