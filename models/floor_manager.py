class FloorManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_available_slots(self, floor_number):
        query = "SELECT available_slots FROM floors WHERE floor_number = %s"
        result = self.db_manager.execute(query, (floor_number,))
        return result[0]["available_slots"] if result else 0

    def update_slots(self, floor_number, count):
        query = "UPDATE floors SET available_slots = available_slots - %s WHERE floor_number = %s"
        print(f"Updating slots: Reducing {count} slots on floor {floor_number}")
        self.db_manager.execute(query, (count, floor_number))
        self.db_manager.commit()  

    def restore_slots(self, floor_number, count):
        query = "UPDATE floors SET available_slots = available_slots + %s WHERE floor_number = %s"
        print(f"Restoring slots: Increasing {count} slots on floor {floor_number}")
        self.db_manager.execute(query, (count, floor_number))
        self.db_manager.commit()  