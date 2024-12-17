class Vehicle:
    VEHICLE_SIZES = {
        "bike": 0.25,  # 4 bikes per slot
        "car": 1,      # 1 car per slot
        "bus": 4       # 1 bus takes 4 slots
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
