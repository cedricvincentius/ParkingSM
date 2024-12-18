from datetime import datetime

class ParkingHistory:
    @staticmethod
    def calculate_fee(vehicle_type, start_time, end_time):
        duration = (end_time - start_time).total_seconds() / 3600 
        rates = {"bike": 2000, "car": 4000, "bus": 6000}
        rate = rates.get(vehicle_type, 0)

        if duration <= 1:
            hours_to_charge = 1
        else:
            hours_to_charge = int(duration) + (1 if duration % 1 > 0 else 0)  # Round up to the next hour if there's a fraction

        return round(rate * hours_to_charge)

    @staticmethod
    def log_parking(db, user_id, vehicle_type, floor, slot_count, start_time, end_time, fee, police_number):
        query = """
            INSERT INTO parking_history (user_id, police_number, vehicle_type, floor, slot_count, start_time, end_time, fee)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        db.execute(query, (user_id, police_number, vehicle_type, floor, slot_count, start_time, end_time, fee))
