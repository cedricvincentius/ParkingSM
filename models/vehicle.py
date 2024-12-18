class Vehicle:
    VEHICLE_SIZES = {
        "bike": 1, 
        "car": 1,  
        "bus": 4 
    }
    FEES_PER_HOUR = {
        "bike": 2000,
        "car": 4000,
        "bus": 6000
    }

    def __init__(self, vehicle_type):
        self.vehicle_type = vehicle_type
        self.size = self.VEHICLE_SIZES[vehicle_type]
        self.fee_per_hour = self.FEES_PER_HOUR[vehicle_type]
