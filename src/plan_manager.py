import os
from datetime import datetime, timedelta

class PlanManager:
    def __init__(self):
        self.file_path = "../logs/current_plan.txt"
        self.current_number = self._read_number_from_file()
        self.last_update_date = self._read_last_update_date()

    def _read_number_from_file(self):
        try:
            with open(self.file_path, 'r') as file:
                number = int(file.read().strip())
            return number
        except FileNotFoundError:
            return 0

    def _read_last_update_date(self):
        try:
            with open("../logs/days/last_update.txt", "r") as file:
                last_update_date_str = file.read().strip()
                return datetime.strptime(last_update_date_str, "%Y-%m-%d").date()
        except FileNotFoundError:
            return datetime.now().date() - timedelta(days=1)

    def _write_number_to_file(self):
        with open(self.file_path, 'w') as file:
            file.write(str(self.current_number))

    def _write_last_update_date(self):
        with open("../logs/last_update.txt", "w") as file:
            file.write(datetime.now().date().strftime("%Y-%m-%d"))

    def increment_number_for_new_day(self):
        today = datetime.now().date()

        if today > self.last_update_date:
            self.current_number += 1
            self._write_number_to_file()
            self._write_last_update_date()
            print("Day incremented for a new plan.")
        else:
            print("It's not a new day. Plan remains unchanged.")
            

if __name__ == "__main__":
    pm = PlanManager("../logs/current_plan.txt")
    print(pm.current_number)
    pm.increment_number_for_new_day()
    print(pm.current_number)    
    