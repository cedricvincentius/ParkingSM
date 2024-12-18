from db.database_manager import DatabaseManager
from models.user import User
from models.vehicle import Vehicle
from models.floor_manager import FloorManager
from services.parking_system import ParkingSystem
import os
from datetime import datetime

def clear_screen():
    # Clear the console screen
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Initialize the database and floor manager once
    db_manager = DatabaseManager()
    floor_manager = FloorManager(db_manager)  # Create a single instance of FloorManager
    parking_system = ParkingSystem(db_manager, floor_manager)

    while True:
        clear_screen()  # Clear the screen at the start of the loop
        print("Welcome to the Parking System!")
        print("1. Login")  
        print("2. Exit")
        
        choice = input("Please select an option (1/2): ").strip()

        if choice == '1':
            user_role = input("Enter role (admin/user): ")
            if user_role in ['admin', 'a']:
                user_role = 'admin'  # Normalize to full role name
            elif user_role in ['user', 'u']:
                user_role = 'user'  # Normalize to full role name
            else:
                print("Invalid role. Please enter 'admin' or 'user' (or 'a'/'u').")
                continue  # Skip to the next iteration of the loop

            user_name = input("Enter username: ")
            user_password = input("Enter password: ")
            if User.login_user(user_name, user_role, user_password):
                # After successful login, show the appropriate menu based on the role
                if user_role == "admin":
                    while True:
                        print("\nAdmin Menu:")
                        print("1. View All Users")
                        print("2. View Ongoing Parking Records")
                        print("3. View Parking History")
                        print("4. Delete Parking History Record")
                        print("5. View Total Income")
                        print("6. Logout")  # Logout option

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
                                    # Format the start_time to the desired format
                                    start_time = record['start_time']
                                    formatted_date = start_time.strftime("%d-%m-%Y")  # Format date as dd-mm-yyyy
                                    formatted_time = start_time.strftime("%H:%M:%S")  # Format time as hh:mm:ss
                                    
                                    # Print the formatted output
                                    print(f"Police Number: {record['police_number']}, Vehicle Type: {record['vehicle_type']}, Floor: {record['floor']}, Date: {formatted_date}, Time: {formatted_time}")
                        elif choice == "3":
                            query = "SELECT id, police_number, vehicle_type, fee, start_time, end_time FROM parking_history"
                            history_records = db_manager.execute(query)
                            
                            print("\nParking History:")
                            if not history_records:
                                print("No parking history found.")
                            else:
                                for record in history_records:
                                    # Format the start_time and end_time to the desired format
                                    start_time = record['start_time']
                                    end_time = record['end_time']
                                    formatted_start_date = start_time.strftime("%d-%m-%Y")  # Format date as dd-mm-yyyy
                                    formatted_start_time = start_time.strftime("%H:%M:%S")  # Format time as hh:mm:ss
                                    formatted_end_date = end_time.strftime("%d-%m-%Y")  # Format date as dd-mm-yyyy
                                    formatted_end_time = end_time.strftime("%H:%M:%S")  # Format time as hh:mm:ss
                                    
                                    # Format fee to RP currency without decimals
                                    formatted_fee = f"RP {int(record['fee'])}"  # Convert fee to integer to remove decimals
                                    
                                    # Print the formatted output including the ID, entry time, and exit time
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
                            break  # Exit the admin menu
                        else:
                            print("Invalid choice. Please try again.")

                else:  # For regular users
                    while True:
                        print("\nUser  Menu:")
                        print("1. Park Vehicle")
                        print("2. View Available Parking Slots")
                        print("3. Unpark Vehicle")  # New option for unparking
                        print("4. Logout")  # Logout option

                        choice = input("Enter your choice: ").strip()
                        if choice == "1":
                            police_number = input("Enter your vehicle's police number: ").strip()
                            vehicle_type = input("Enter your vehicle type (bike/car/bus): ").strip()
                            
                            # Create a Vehicle instance
                            vehicle = Vehicle(vehicle_type)  # Assuming Vehicle class takes vehicle_type as an argument

                            # Call park_vehicle with user_name, Vehicle instance, and police_number
                            if parking_system.park_vehicle(user_name, vehicle, police_number):
                                print("Vehicle parked successfully.")
                            else:
                                print("Failed to park the vehicle.")

                        elif choice == "2":
                            print("\nAvailable Parking Slots:")
                            # Assuming you have 3 floors: 1 for bikes, 2 for cars, and 3 for buses
                            for floor in range(1, 4):
                                available_slots = floor_manager.get_available_slots(floor)  # Get available slots for the floor
                                print(f"Floor {floor}: {available_slots} available slots")

                        elif choice == "3":  # Unpark vehicle option
                            police_number = input("Enter your vehicle's police number to unpark: ").strip()
                            fee = parking_system.unpark_vehicle(police_number)  # Call the unpark method
                            if fee is not None:
                                print(f"Vehicle unparked successfully! Total fee: Rp. {fee:.2f}")
                            else:
                                print("Failed to unpark the vehicle.")

                        elif choice == "4":
                            print("Logging out...")
                            break  # Exit the user menu
                        else:
                            print("Invalid choice. Please try again.")
        elif choice == '2':
            print("Exiting the system. Goodbye!")
            break  # Exit the main loop

if __name__ == "__main__":
    main()