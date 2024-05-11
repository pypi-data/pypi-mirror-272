from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from calculator_api.src.calculator_utils import make_addition

app = FastAPI()


class CalculatorItems(BaseModel):  # type: ignore
    """BaseModel for addition inputs."""

    first_element: Union[int, float]
    second_element: Union[int, float]


@app.put("/calculator_items/")  # type: ignore
async def apply_addition(calculator_items: CalculatorItems) -> dict[str, Union[int, float]]:
    """Endpoint using make_addition function

    Args:
        calculator_items (CalculatorItems): Pydantic BaseModel for addition inputs.

    Returns:
        dict[str, Union[int, float]]: Dictionary containing result.
    """
    result = make_addition(calculator_items.first_element, calculator_items.second_element)

    return {"Result of the addition is : ": result}
