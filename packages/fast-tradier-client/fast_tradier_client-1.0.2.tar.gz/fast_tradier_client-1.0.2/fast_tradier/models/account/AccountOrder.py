import json
from dataclasses import dataclass
from typing import Dict, Mapping, Optional, List, Any
from pydantic import Field, ConfigDict
from fast_tradier.models.DataClassModelBase import DataClassModelBase
from fast_tradier.models.ModelBase import NewModelBase

class Leg(NewModelBase):
    id: int
    type: str
    symbol: str
    side: str
    quantity: float
    status: str
    duration: str
    price: float
    avg_fill_price: float
    exec_quantity: float
    last_fill_price: float
    last_fill_quantity: float
    remaining_quantity: float
    create_date: str
    transaction_date: str
    # class: str
    class_: Optional[str] = Field(..., alias="class")
    option_symbol: Optional[str] = None
    model_config = ConfigDict(populate_by_name=True)
    
    def to_json(self) -> Mapping[str, Any]:
        result = self.model_dump(by_alias=True)
        return result

class AccountOrder(NewModelBase):
    id: int
    # type: str
    type_: str = Field(..., alias="type")
    symbol: str
    side: str
    quantity: float
    status: str
    duration: str
    price: Optional[float] = None
    avg_fill_price: float
    exec_quantity: float
    last_fill_price: float
    last_fill_quantity: float
    remaining_quantity: float
    create_date: str
    transaction_date: str
    # class_type: str
    class_: Optional[str] = Field(..., alias="class")
    num_legs: Optional[int] = None
    strategy: Optional[str] = None
    leg: Optional[List[Leg]] = []
    model_config = ConfigDict(populate_by_name=True)

    def to_json(self) -> Mapping[str, Any]:
        result = self.model_dump(by_alias=True)
        return result