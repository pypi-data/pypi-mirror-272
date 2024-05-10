from typing import Dict, List, Optional, Mapping, Any

from fast_tradier.models.trading.TOSTradierConverter import TOSTradierConverter
from fast_tradier.models.ModelBase import ModelBase
from fast_tradier.models.trading.Sides import OptionOrderSide
from fast_tradier.models.trading.PriceTypes import OptionPriceType
from fast_tradier.models.trading.Duration import Duration
from fast_tradier.models.trading.OrderBase import OrderBase
from fast_tradier.models.ModelBase import NewModelBase
from pydantic import BaseModel, ConfigDict

class OptionLeg(NewModelBase):
    model_config = ConfigDict(use_enum_values=True)
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
    model_config = ConfigDict(use_enum_values=True)
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
        return cloned_legs
    
    def to_json(self) -> Mapping[str, Any]:
        """
        Override to_json so that the format complies to Tradier API.
        Returns:
            Mapping[str, Any]: _description_
        """
        result: Dict[str, Any] = {
            "id": self.id,
            "status": self.status,
            "symbol": self.ticker,
            "duration": self.duration,
            "price": self.price,
            "type": self.price_type,
            "class": self.order_class,
        }

        if len(self.option_legs) == 1:
            result["option_symbol"] = self.option_legs[0].option_symbol
            result["side"] = self.option_legs[0].side
            result["quantity"] = self.option_legs[0].quantity
        elif len(self.option_legs) > 1:
            for i in range(len(self.option_legs)):
                opt_item = self.option_legs[i]
                symbol_key = f"option_symbol[{i}]"
                result[symbol_key] = opt_item.option_symbol
                side_key = f"side[{i}]"
                result[side_key] = f"{opt_item.side}"
                quant_key = f"quantity[{i}]"
                result[quant_key] = f"{opt_item.quantity}"

        return result