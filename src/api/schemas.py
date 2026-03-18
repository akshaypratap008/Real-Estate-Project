from pydantic import BaseModel, Field
from typing import Literal, Annotated, Dict

class UserInput(BaseModel):

    property_type : Annotated[Literal['flat', 'house'], Field(..., description="Type of property", examples=['flat', 'house'])]
    sector: Annotated[str, Field(..., description='Which sector in Gurgaon the property is located in?', examples=['sector 1', 'sector 2'])]
    bedroom: Annotated[int, Field(..., gt=0, description='Number of bedrooms user want in the property')]
    bathroom: Annotated[int, Field(..., gt=0, description='Number of bathrooms user want in the property')]
    balcony: Annotated[Literal['1', '2', '3+'], Field(..., description='Number of balconies user want in the property')]
    agePossession: Annotated[str, Field(..., description='Age of the property', examples=['relatively new', 'new', 'old'])]
    built_up_area: Annotated[int, Field(..., description='Built up area of the property in Sqft')]
    servant_room: Annotated[bool, Field(..., description='Does the user want servant room in the property?')]
    store_room: Annotated[bool, Field(..., description='Does the user want store room property?')]
    furnishing_type: Annotated[Literal['unfurnished', 'semifurnished', 'furnished'], Field(..., description='What type of furnishing does the user want?')]
    luxury_category: Annotated[Literal['budget', 'luxury'], Field(..., description='What type of luxury does the user want')]
    floor_category: Annotated[Literal['low-rise', 'medium-rise', 'high-rise'], Field(..., description='Which floor does the user want the property? low-rise: 0-3, medium-rise: 4-10, high-rise: 10 above')]

class PredictionResponse(BaseModel):

    predicted_price: float = Field(..., description="Price predicted by the model")
    price_unit: Literal['Lakhs', 'Crores'] = Field(..., description='Unit of the predicted price(lakhs or crores). If predicted price less than 1, it is converted into lakhs')
    message : str 

class ExplainationResponse(BaseModel):

    predicted_price: float = Field(..., description="Price predicted by the model")
    feature_contributions: Dict[str, float]