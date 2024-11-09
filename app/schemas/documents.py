from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from typing import Optional, List
from beanie import Document
from enum import Enum
import pymongo

# Define an Enum for Fiscal Year
class FiscalYearEnum(str, Enum):
    FY_2012_2013 = "2012-2013"
    FY_2013_2014 = "2013-2014"
    FY_2014_2015 = "2014-2015"

# Define an Enum for Acquisition Type
class AcquisitionTypeEnum(str, Enum):
    IT_Goods = "IT Goods"
    NON_IT_Goods = "NON-IT Goods"
    IT_Services = "IT Services"
    NON_IT_Services = "NON-IT Services"
    IT_Telecommunications = "IT Telecommunications"


class Purchase(Document):
    creation_date: datetime = Field(..., title="Creation Date")
    purchase_date: Optional[datetime] = Field(None, title="Purchase Date")
    fiscal_year: FiscalYearEnum = Field(..., title="Fiscal Year")
    lpa_number: Optional[str] = Field(None, title="LPA Number")
    purchase_order_number: str = Field(..., title="Purchase Order Number")
    requisition_number: Optional[str] = Field(None, title="Requisition Number")
    acquisition_type: AcquisitionTypeEnum = Field(..., title="Acquisition Type")
    sub_acquisition_type: Optional[str] = Field(None, title="Sub-Acquisition Type")
    acquisition_method: str = Field(..., title="Acquisition Method")
    sub_acquisition_method: Optional[str] = Field(None, title="Sub-Acquisition Method")
    department_name: str = Field(..., title="Department Name")
    supplier_code: Optional[int] = Field(None, title="Supplier Code")
    supplier_name: Optional[str] = Field(None, title="Supplier Name")
    supplier_qualifications: Optional[List[str]] = Field(None, title="Supplier Qualifications")
    supplier_zip_code: Optional[str] = Field(None, title="Supplier Zip Code")
    cal_card: bool = Field(..., title="Cal Card Used")
    item_name: Optional[str] = Field(None, title="Item Name")
    item_description: Optional[str] = Field(None, title="Item Description")
    quantity: Optional[float] = Field(None, title="Quantity") # the data has fractional parts
    unit_price: Optional[float] = Field(None, title="Unit Price")
    total_price: Optional[float] = Field(None, title="Total Price")
    classification_codes: Optional[List[int]] = Field(..., title="Classification Codes")
    normalized_UNSPSC: Optional[int] = Field(None, title="Normalized UNSPSC Code")
    commodity_title: Optional[str] = Field(None, title="Commodity Title")
    class_code: Optional[int] = Field(None, alias="class", title="Class Code") # we make alias to don't raise error
    class_title: Optional[str] = Field(None, title="Class Title")
    family_code: Optional[int] = Field(None, alias="family", title="Family Code")
    family_title: Optional[str] = Field(None, title="Family Title")
    segment_code: Optional[int] = Field(None, alias="segment", title="Segment Code")
    segment_title: Optional[str] = Field(None, title="Segment Title")
    location_zip: Optional[str] = Field(None, title="Location Zip Code")
    location_lat: Optional[float] = Field(None, title="Location Latitude")
    location_long: Optional[float] = Field(None, title="Location Longitude")

    class Settings:
        name = "purchases"
        use_cache = True
        cache_expiration_time = timedelta(seconds=30)
        cache_capacity = 5
        indexes = [
            'fiscal_year',
            'acquisition_type',
            'item_name',
            'purchase_date',
            'segment_code',
            pymongo.IndexModel(
                [("supplier_name", pymongo.ASCENDING), ("supplier_zip_code", pymongo.ASCENDING)],
                name="supplier_name_supplier_zip_code_index",
            ),
            pymongo.IndexModel(
                [("location_lat", pymongo.ASCENDING), ("location_long", pymongo.ASCENDING)],
                name="location_lat_location_long_index",
            ),
        ]
