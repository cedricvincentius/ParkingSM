from datetime import datetime

class ParkingSystem:
    def __init__(self, db, floor_manager):
        self.db = db
        self.floor_manager = floor_manager

    def park_vehicle(self, user_id, vehicle):
        # Get police number from user
        police_number = input("Enter the police number (license plate) of the vehicle: ").strip()

        # Determine the floor based on the vehicle type
        floor = 1 if vehicle.vehicle_type == "bike" else (2 if vehicle.vehicle_type in ["car", "bus"] else None)
        
        if floor is None:
            print("Invalid vehicle type!")
            return False

        available_slots = self.floor_manager.get_available_slots(floor)
        required_slots = vehicle.size

        if available_slots >= required_slots:
            # Update the slots and log the parking in the database
            self.floor_manager.update_slots(floor, required_slots)
            query = """
                INSERT INTO ongoing_parking (user_id, police_number, vehicle_type, floor, slot_count, start_time)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """
            self.db.execute(query, (user_id, police_number, vehicle.vehicle_type, floor, required_slots))
            print(f"{vehicle.vehicle_type.capitalize()} with police number {police_number} parked successfully!")
            return True
        else:
            print(f"Not enough available slots on floor {floor} for a {vehicle.vehicle_type}.")
            return False


def unpark_vehicle(self, police_number):
        # Retrieve the ongoing parking record by police number
        query = "SELECT * FROM ongoing_parking WHERE police_number = %s"
        record = self.db.execute(query, (police_number,))
        
        if not record:
            print("No vehicle found with this police number.")
            return None

        record = record[0]
        floor = record["floor"]
        slot_count = record["slot_count"]
        vehicle_type = record["vehicle_type"]
        start_time = record["start_time"]

        # Calculate fee
        end_time = datetime.now()
        fee = ParkingHistory.calculate_fee(vehicle_type, start_time, end_time)

        # Log history and delete from ongoing parking
        ParkingHistory.log_parking(
            self.db, record["user_id"], vehicle_type, floor, slot_count, start_time, end_time, fee, record["police_number"]
        )
        self.floor_manager.restore_slots(floor, slot_count)
        query = "DELETE FROM ongoing_parking WHERE police_number = %s"
        self.db.execute(query, (police_number,))
        print(f"Vehicle with police number {police_number} unparked successfully! Total fee: Rp. {fee:.2f}")
        return fee
