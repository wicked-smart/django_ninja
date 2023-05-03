from ninja import NinjaAPI, ModelSchema
from testing_api.models import * 
from typing import List, Dict

api = NinjaAPI()


class AirportSchema(ModelSchema):
    
    class Config:
        model = Airport
        model_fields = "__all__"
    

class FlightSchema(ModelSchema):
    origin: Dict[str, str]
    destination: Dict[str,str]

    class Config:
        model = Flight
        model_fields = "__all__"
    

    @staticmethod
    def resolve_origin(obj):
        return {"city": obj.origin.city,
            "code": obj.origin.code
         }

    @staticmethod
    def resolve_destination(obj):
        return {"city": obj.destination.city,
            "code": obj.destination.code
         }
    

class PassengerSchema(ModelSchema):
    flight: List[Dict[str,str]] = []

    class Config:
        model = Passenger
        model_fields = "__all__"  
        arbitrary_types_allowed = True
    
    @staticmethod
    def resolve_flight(obj):
        return [{"origin": flight.origin.city, "destination": flight.destination.city} for flight in obj.flight.all()]



@api.get("/airports", response=List[AirportSchema])
def airports(request ):
    return Airport.objects.all()


@api.get("flights", response=List[FlightSchema])
def flights(request):
    flights = Flight.objects.select_related('origin').all()
    return flights

@api.get("passengers", response=List[PassengerSchema])
def passengers(request):
    passengers = Passenger.objects.all()
    return passengers