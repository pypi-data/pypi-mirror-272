from crewai_tools import BaseTool
from aic_tools_alpaca import TradingClientSingleton


class CheckIfTradingBlocked(BaseTool):
    name: str = "Answer on: is trading prohibited?"
    description: str = """Answers the question whether trading is blocked for this account.
    If true, the account does not allow placing orders.
    If false, the account allows placing orders."""

    def _run(self) -> bool:
        # Your tool's logic here
        return TradingClientSingleton.get_instance().get_account().trading_blocked


class GetTotalBuyingPower(BaseTool):
    name: str = "Accountant total purchasing power."
    description: str = """Returns a string with the number of dollars as the purchasing power of the accountant.
    Current available cash buying power. If multiplier = 2 then buying_power = max(equity-initial_margin(0) * 2).
    If multiplier = 1 then buying_power = cash."""

    def _run(self) -> str:
        return f"{TradingClientSingleton.get_instance().get_account().buying_power}$"


class GetNonMarginableBuyingPower(BaseTool):
    name: str = "Accountant purchasing power without margin."
    description: str = "Returns a string with the number of dollars as the non marginable buying power for the account."

    def _run(self) -> str:
        return f"{TradingClientSingleton.get_instance().get_account().non_marginable_buying_power}$"


class GetAccountEquity(BaseTool):
    name: str = "Answer on: what is portfolio value?"
    description: str = """Returns a string with the numbers of dollars that tell us the account equity.
    This value is cash + long_market_value + short_market_value.
    This value isn’t calculated in the SDK it is computed on the server and we return the raw value here.
    """

    def _run(self) -> str:
        return f"{TradingClientSingleton.get_instance().get_account().equity}$"
