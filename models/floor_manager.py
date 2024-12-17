class FloorManager:
    def __init__(self, db):
        self.db = db
        self.slots_per_floor = {1: 8, 2: 8, 3: 8}

    def get_available_slots(self, floor):
        return self.slots_per_floor[floor]

    def update_slots(self, floor, slots_used):
        self.slots_per_floor[floor] -= slots_used

    def restore_slots(self, floor, slots_freed):
        self.slots_per_floor[floor] += slots_freed
