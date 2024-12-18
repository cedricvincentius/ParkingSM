from db.database_manager import DatabaseManager
from models.user import User
from models.vehicle import Vehicle
from models.floor_manager import FloorManager
from services.parking_system import ParkingSystem
import os
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    db_manager = DatabaseManager()
    floor_manager = FloorManager(db_manager)
    parking_system = ParkingSystem(db_manager, floor_manager)

    while True:
        clear_screen()
        print("Welcome to the Parking System!")
        print("1. Login")  
        print("2. Exit")
        
        choice = input("Please select an option (1/2): ").strip()

        if choice == '1':
            user_role = input("Enter role (admin/user): ")
            if user_role in ['admin', 'a']:
                user_role = 'admin'
            elif user_role in ['user', 'u']:
                user_role = 'user'
            else:
                print("Invalid role. Please enter 'admin' or 'user' (or 'a'/'u').")
                continue

            user_name = input("Enter username: ")
            user_password = input("Enter password: ")
            if User.login_user(user_name, user_role, user_password):
                if user_role == "admin":
                    while True:
                        print("\nAdmin Menu:")
                        print("1. View All Users")
                        print("2. View Ongoing Parking Records")
                        print("3. View Parking History")
                        print("4. Delete Parking History Record")
                        print("5. View Total Income")
                        print("6. Logout")

                        choice = input("Enter your choice: ").strip()
                        if choice == "1":
                            users = User.fetch_users(db_manager)
                            print("\nUsers:")
                            for user in users:
                                print(f"Name: {user['name']}, Role: {user['role']}, Login Time: {user['login_time']}")
                        elif choice == "2":
                            query = "SELECT police_number, vehicle_type, floor, start_time FROM ongoing_parking"
                            ongoing_records = db_manager.execute(query)
                            
                            print("\nOngoing Parking Records:")
                            if not ongoing_records:
                                print("No ongoing parking records found.")
                            else:
                                for record in ongoing_records:
                                    start_time = record['start_time']
                                    formatted_date = start_time.strftime("%d-%m-%Y")  # Format date as dd-mm-yyyy
                                    formatted_time = start_time.strftime("%H:%M:%S")  # Format time as hh:mm:ss

                                    print(f"Police Number: {record['police_number']}, Vehicle Type: {record['vehicle_type']}, Floor: {record['floor']}, Date: {formatted_date}, Time: {formatted_time}")
                        elif choice == "3":
                            query = "SELECT id, police_number, vehicle_type, fee, start_time, end_time FROM parking_history"
                            history_records = db_manager.execute(query)
                            
                            print("\nParking History:")
                            if not history_records:
                                print("No parking history found.")
                            else:
                                for record in history_records:
                                    start_time = record['start_time']
                                    end_time = record['end_time']
                                    formatted_start_date = start_time.strftime("%d-%m-%Y")
                                    formatted_start_time = start_time.strftime("%H:%M:%S")
                                    formatted_end_date = end_time.strftime("%d-%m-%Y")
                                    formatted_end_time = end_time.strftime("%H:%M:%S")
                                    formatted_fee = f"RP {int(record['fee'])}"
                                    
                                    print(f"ID: {record['id']}, Police Number: {record['police_number']}, Vehicle Type: {record['vehicle_type']}, Fee: { formatted_fee}, Entry Time: {formatted_start_date} {formatted_start_time}, Exit Time: {formatted_end_date} {formatted_end_time}") 

                        elif choice == "4":
                            record_id = int(input("Enter the ID of the record to delete: ").strip())
                            query = "DELETE FROM parking_history WHERE id = %s"
                            db_manager.execute(query, (record_id,))
                            print("Record deleted successfully.")

                        elif choice == "5":
                            query = "SELECT SUM(fee) AS total_income FROM parking_history"
                            total_income = db_manager.execute(query)
                            print(f"Total Income: Rp. {total_income[0]['total_income']}")

                        elif choice == "6":
                            print("Logging out...")
                            break

                        else:
                            print("Invalid choice. Please try again.")

                else: 
                    while True:
                        print("\nUser  Menu:")
                        print("1. Park Vehicle")
                        print("2. View Available Parking Slots")
                        print("3. Unpark Vehicle") 
                        print("4. Logout")

                        choice = input("Enter your choice: ").strip()
                        if choice == "1":
                            police_number = input("Enter your vehicle's police number: ").strip()
                            vehicle_type = input("Enter your vehicle type (bike/car/bus): ").strip()
                            
                            vehicle = Vehicle(vehicle_type)

                            if parking_system.park_vehicle(user_name, vehicle, police_number):
                                print("Vehicle parked successfully.")
                            else:
                                print("Failed to park the vehicle.")

                        elif choice == "2":
                            print("\nAvailable Parking Slots:")
                            for floor in range(1, 4):
                                available_slots = floor_manager.get_available_slots(floor)  # Get available slots for the floor
                                print(f"Floor {floor}: {available_slots} available slots")

                        elif choice == "3":
                            police_number = input("Enter your vehicle's police number to unpark: ").strip()
                            fee = parking_system.unpark_vehicle(police_number)  # Call the unpark method
                            if fee is not None:
                                print(f"Vehicle unparked successfully! Total fee: Rp. {fee:.2f}")
                            else:
                                print("Failed to unpark the vehicle.")

                        elif choice == "4":
                            print("Logging out...")
                            break
                        else:
                            print("Invalid choice. Please try again.")
        elif choice == '2':
            print("Exiting the system. Goodbye!")
            break

if __name__ == "__main__":
    main()