from models.history import ParkingHistory  # Import ParkingHistory class
from datetime import datetime

class ParkingSystem:
    def __init__(self, db, floor_manager):
        self.db = db
        self.floor_manager = floor_manager

    def park_vehicle(self, user_id, vehicle):
        # Get police number from user
        police_number = input("Enter the police number (license plate) of the vehicle: ").strip()

        # Determine the floor based on the vehicle type
        if vehicle.vehicle_type == "bike":
            floor_number = 1
        elif vehicle.vehicle_type == "car":
            floor_number = 2
        elif vehicle.vehicle_type == "bus":
            # Check available slots for both the 2nd and 3rd floors
            available_slots_2nd = self.floor_manager.get_available_slots(2)
            available_slots_3rd = self.floor_manager.get_available_slots(3)

            # Calculate used slots
            used_slots_2nd = 5 - available_slots_2nd  # Assuming total slots are 5
            used_slots_3rd = 5 - available_slots_3rd  # Assuming total slots are 5

            # Debugging print statements
            print(f"Used slots on 2nd floor: {used_slots_2nd}")
            print(f"Used slots on 3rd floor: {used_slots_3rd}")

            # Decision logic for parking the bus
            if used_slots_2nd < 5 and available_slots_2nd >= vehicle.size:
                floor_number = 2
            elif used_slots_3rd < 5 and available_slots_3rd >= vehicle.size:
                floor_number = 3
            else:
                print("No available slots for the bus.")
                return False
        else:
            print("Invalid vehicle type!")
            return False

        # Check available slots for the determined floor
        available_slots = self.floor_manager.get_available_slots(floor_number)
        required_slots = vehicle.size  # Assuming vehicle.size is defined

        # Debugging print statements
        print(f"Available slots on floor {floor_number}: {available_slots}")
        print(f"Required slots for {vehicle.vehicle_type}: {required_slots}")

        if available_slots >= required_slots:
            # Update the slots and log the parking in the database
            self.floor_manager.update_slots(floor_number, required_slots)
            query = """
                INSERT INTO ongoing_parking (user_id, police_number, vehicle_type, floor, slot_count, start_time)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """
            self.db.execute(query, (user_id, police_number, vehicle.vehicle_type, floor_number, required_slots))
            print(f"{vehicle.vehicle_type.capitalize()} with police number {police_number} parked successfully on floor {floor_number}!")
            return True
        else:
            print(f"Not enough available slots on floor {floor_number} for a {vehicle.vehicle_type}.")
            return False

    def unpark_vehicle(self, police_number):
        # Retrieve the ongoing parking record by police number
        query = "SELECT * FROM ongoing_parking WHERE police_number = %s"
        record = self.db.execute(query, (police_number,))

        if not record:
            print("No vehicle found with this police number.")
            return None

        record = record[0]
        floor_number = record["floor"]
        slot_count = record["slot_count"]
        vehicle_type = record["vehicle_type"]
        start_time = record["start_time"]

        # Calculate fee
        end_time = datetime.now()
        fee = ParkingHistory.calculate_fee(vehicle_type, start_time, end_time)  # Using the imported class

        # Log history and delete from ongoing parking
        ParkingHistory.log_parking(
            self.db, record["user_id"], vehicle_type, floor_number, slot_count, start_time, end_time, fee, record["police_number"]
        )
        self.floor_manager.restore_slots(floor_number, slot_count)
        query = "DELETE FROM ongoing_parking WHERE police_number = %s"
        self.db.execute(query, (police_number,))
        print(f"Vehicle with police number {police_number} unparked successfully! Total fee: Rp. {fee:.2f}")
        return fee