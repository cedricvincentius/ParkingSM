from models.history import ParkingHistory  # Import ParkingHistory class
from datetime import datetime

class ParkingSystem:
    def __init__(self, db, floor_manager):
        self.db = db
        self.floor_manager = floor_manager

    def park_vehicle(self, user_name, vehicle, police_number):
        try:
            # Fetch user_id from the database based on user_name
            query = "SELECT id FROM users WHERE name = %s"
            user_record = self.db.execute(query, (user_name,))
            
            if not user_record:
                print("User  not found.")
                return False
            
            user_id = user_record[0]['id']  # Assuming 'id' is the column name for user ID

            # Determine the floor based on the vehicle type
            if vehicle.vehicle_type == "bike":
                floor_number = 1
            elif vehicle.vehicle_type == "car":
                # Check available slots for both the 2nd and 3rd floors
                available_slots_2nd = self.floor_manager.get_available_slots(2)
                available_slots_3rd = self.floor_manager.get_available_slots(3)

                # Debugging print statements
                print(f"Available slots on 2nd floor: {available_slots_2nd}")
                print(f"Available slots on 3rd floor: {available_slots_3rd}")

                # Decision logic for parking the car
                if available_slots_2nd >= vehicle.size:
                    floor_number = 2
                elif available_slots_3rd >= vehicle.size:
                    floor_number = 3
                else:
                    print("No available slots for the car.")
                    return False
            elif vehicle.vehicle_type == "bus":
                # Check available slots for both the 2nd and 3rd floors
                available_slots_2nd = self.floor_manager.get_available_slots(2)
                available_slots_3rd = self.floor_manager.get_available_slots(3)

                # Debugging print statements
                print(f"Available slots on 2nd floor: {available_slots_2nd}")
                print(f"Available slots on 3rd floor: {available_slots_3rd}")

                # Decision logic for parking the bus
                if available_slots_2nd >= vehicle.size:
                    floor_number = 2
                elif available_slots_3rd >= vehicle.size:
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
                # Debugging print statement to check the values being inserted
                print(f"Inserting into ongoing_parking: user_id={user_id}, police_number={police_number}, vehicle_type={vehicle.vehicle_type}, floor={floor_number}, slot_count={required_slots}")
                self.db.execute(query, (user_id, police_number, vehicle.vehicle_type, floor_number, required_slots))
                print(f"{vehicle.vehicle_type.capitalize()} with police number {police_number} parked successfully on floor {floor_number}!")
                return True
            else:
                print(f"Not enough available slots on floor {floor_number} for a {vehicle.vehicle_type}.")
                return False
        except Exception as e:
            print(f"Error while parking vehicle: {e}")
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
        end_time = datetime.now()  # This is the exit time
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