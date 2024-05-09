from typing import Dict, List, Optional, Mapping, Any

from fast_tradier.models.trading.TOSTradierConverter import TOSTradierConverter
from fast_tradier.models.ModelBase import ModelBase
from fast_tradier.models.trading.Sides import OptionOrderSide
from fast_tradier.models.trading.PriceTypes import OptionPriceType
from fast_tradier.models.trading.Duration import Duration
from fast_tradier.models.trading.OrderBase import OrderBase
from pydantic import BaseModel, ConfigDict

class NewModelBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    def to_json(self) -> Mapping[str, Any]:
        return self.model_dump()

class OptionLeg(NewModelBase):
    underlying_symbol: str
    option_symbol: str
    quantity: int
    side: OptionOrderSide
    
    def reverse_side(self) -> None:
        if self.side == OptionOrderSide.SellToOpen or self.side == OptionOrderSide.SellToOpen.value:
            setattr(self, "side", OptionOrderSide.BuyToClose)
        elif self.side == OptionOrderSide.BuyToOpen or self.side == OptionOrderSide.BuyToOpen.value:
            setattr(self, "side", OptionOrderSide.SellToClose)

class OptionOrder(NewModelBase):
    ticker: str
    price: float
    price_type: OptionPriceType
    duration: Duration
    option_legs: List[OptionLeg]
    status: str = "pending"
    order_class: str = "multileg" # could be "option"
    id: Optional[int] = None

    def set_price(self, new_price: float) -> None:
        setattr(self, "price", new_price)

    def set_status(self, new_staus: str) -> None:
        setattr(self, "status", new_staus)

    def set_ticker(self, ticker_name: str) -> None:
        setattr(self, "ticker", ticker_name)
    
    def set_id(self, new_id: int) -> None:
        setattr(self, "id", new_id)

    def clone_option_legs(self, reverse_side: bool = False) -> List[OptionLeg]:
        '''deep clone option_legs'''
        cloned_legs = []
        for opt_leg in self.option_legs:
            leg = OptionLeg(**(opt_leg.to_json()))
            if reverse_side:
                leg.reverse_side()

            cloned_legs.append(leg)