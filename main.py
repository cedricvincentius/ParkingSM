from db.database_manager import DatabaseManager
from models.user import User
from models.vehicle import Vehicle
from models.floor_manager import FloorManager
from services.parking_system import ParkingSystem
from gui.gui import ParkingGUI

def main():
    # Initialize the database and floor manager
    db_manager = DatabaseManager()
    floor_manager = FloorManager(db_manager)

    # Initialize the parking system facade
    parking_system = ParkingSystem(db_manager, floor_manager)

    print("Welcome to the Parking System!")
    role = input("Are you an 'admin' or a 'user'? ").strip().lower()

    # Login or create a user
    name = input("Enter your name: ").strip()
    user = User(db_manager, name, role)
    user_id = user.create_user()[0]["id"]
    print(f"Hello, {name}! Your role is {role}.")

    if role == "admin":
        while True:
            print("\nAdmin Menu:")
            print("1. View All Users")
            print("2. View Ongoing Parking Records")
            print("3. View Parking History")
            print("4. Delete Parking History Record")
            print("5. View Total Income")
            print("0. Exit")

            choice = input("Enter your choice: ").strip()
            if choice == "1":
                users = User.fetch_users(db_manager)
                print("\nUsers:")
                for user in users:
                    print(user)
            elif choice == "2":
                query = "SELECT * FROM ongoing_parking"
                ongoing_records = db_manager.execute(query)
                print("\nOngoing Parking Records:")
                for record in ongoing_records:
                    print(record)
            elif choice == "3":
                query = "SELECT * FROM parking_history"
                history = db_manager.execute(query)
                print("\nParking History:")
                for record in history:
                    print(record)
            elif choice == "4":
                record_id = int(input("Enter the ID of the record to delete: ").strip())
                query = "DELETE FROM parking_history WHERE id = %s"
                db_manager.execute(query, (record_id,))
                print("Record deleted successfully.")
            elif choice == "5":
                # Calculate total income for the day
                query = """
                    SELECT SUM(fee) AS total_income
                    FROM parking_history
                    WHERE DATE(start_time) = CURRENT_DATE
                """
                result = db_manager.execute(query)
                total_income = result[0]["total_income"] if result and result[0]["total_income"] else 0
                print(f"\nTotal Income for Today: Rp. {total_income:,}")
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    elif role == "user":
        while True:
            print("\nUser Menu:")
            print("1. Park a Vehicle")
            print("2. Unpark a Vehicle")
            print("3. View Available Slots")
            print("0. Exit")

            choice = input("Enter your choice: ").strip()
            if choice == "1":
                vehicle_type = input("Enter vehicle type (bike/car/bus): ").strip().lower()
                vehicle = Vehicle(vehicle_type)
                success = parking_system.park_vehicle(user_id, vehicle)
                if success:
                    print(f"{vehicle_type.capitalize()} parked successfully!")
                else:
                    print("No available slots for this vehicle.")
            elif choice == "2":
                vehicle_type = input("Enter vehicle type (bike/car/bus): ").strip().lower()
                vehicle = Vehicle(vehicle_type)
                floor = int(input("Enter floor number: ").strip())
                police_number = input("Enter the police number (license plate) of the vehicle to unpark: ").strip()
                fee = parking_system.unpark_vehicle(police_number)
                print(f"Vehicle unparked! Total fee: Rp. {fee:.2f}")
            elif choice == "3":
                for floor in range(1, 4):
                    slots = floor_manager.get_available_slots(floor)
                    print(f"Floor {floor}: {slots} slots available")
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    else:
        print("Invalid role. Exiting the system.")

if __name__ == "__main__":
    main()
