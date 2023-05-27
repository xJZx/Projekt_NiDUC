import csv
import random
import matplotlib.pyplot as plt


class RepairSystem:
    def __init__(self, parts_capacity, parts_stock, workers_amount):
        self.num_requests = 5
        self.parts_capacity = parts_capacity
        self.parts_stock = parts_stock
        self.workers_amount = workers_amount
        self.orders = 0
        self.parts_cost = 0
        self.completed_repairs = 0
        self.time = 0
        self.total_repair_time = 0
        self.repair_times = []
        # zapisuje w ktorym czasie dzialania systemu wystapila awaria
        # liczba pracownikow zalezy od pory dnia
        # time % 24 -> (0 - 6 i 22 - 0 -> noc) (6 - 22 -> dzień)
        self.repair_time_occurrences = []  # czas symulacji w ktorym usterka wystapila
        self.repair_time_by_id = [0] * 5  # poszczegolne id usterek - ile w sumie trwala ich naprawa
        self.repairs_by_id = [1] * 5  # ile napraw danego typu wystapilo

    def start_repair(self):
        repair_time = 0
        repair_id = random.randint(0, 100)

        if 6 <= self.time % 24 < 22:  # symulacja zmiany dziennej
            print("Day repair")
            if 0 <= repair_id < 50:  # 50%
                repair_time += random.uniform((1 / self.workers_amount), (5 / self.workers_amount))
                self.repair_time_by_id[0] += repair_time
                self.parts_stock -= 1
                self.parts_cost += random.randint(50, 100)
                self.repairs_by_id[0] += 1

            elif 50 <= repair_id < 70:  # 20%
                repair_time += random.uniform((5 / self.workers_amount), (10 / self.workers_amount))
                self.repair_time_by_id[1] += repair_time
                self.parts_stock -= 2
                self.parts_cost += random.randint(100, 200)
                self.repairs_by_id[1] += 1

            elif 70 <= repair_id < 85:  # 15%
                repair_time += random.uniform((10 / self.workers_amount), (15 / self.workers_amount))
                self.repair_time_by_id[2] += repair_time
                self.parts_stock -= 3
                self.parts_cost += random.randint(200, 400)
                self.repairs_by_id[2] += 1

            elif 85 <= repair_id < 95:  # 10%
                repair_time += random.uniform((15 / self.workers_amount), (20 / self.workers_amount))
                self.repair_time_by_id[3] += repair_time
                self.parts_stock -= 4
                self.parts_cost += random.randint(400, 800)
                self.repairs_by_id[3] += 1

            elif 95 <= repair_id < 100:  # 5%
                repair_time += random.uniform((20 / self.workers_amount), (25 / self.workers_amount))
                self.repair_time_by_id[4] += repair_time
                self.parts_stock -= 5
                self.parts_cost += random.randint(800, 1600)
                self.repairs_by_id[4] += 1

        else:  # symulacja zmiany nocnej
            print("Night repair")
            if 0 <= repair_id < 50:  # 50%
                repair_time += random.uniform((3 / (self.workers_amount * 0.6)), (6 / (self.workers_amount * 0.6)))
                self.repair_time_by_id[0] += repair_time
                self.parts_stock -= 1
                self.parts_cost += random.randint(50, 100)
                self.repairs_by_id[0] += 1

            elif 50 <= repair_id < 70:  # 20%
                repair_time += random.uniform((6 / (self.workers_amount * 0.6)), (12 / (self.workers_amount * 0.6)))
                self.repair_time_by_id[1] += repair_time
                self.parts_stock -= 2
                self.parts_cost += random.randint(100, 200)
                self.repairs_by_id[1] += 1

            elif 70 <= repair_id < 85:  # 15%
                repair_time += random.uniform((12 / (self.workers_amount * 0.6)), (24 / (self.workers_amount * 0.6)))
                self.repair_time_by_id[2] += repair_time
                self.parts_stock -= 3
                self.parts_cost += random.randint(200, 400)
                self.repairs_by_id[2] += 1

            elif 85 <= repair_id < 95:  # 10%
                repair_time += random.uniform((24 / (self.workers_amount * 0.6)), (48 / (self.workers_amount * 0.6)))
                self.repair_time_by_id[3] += repair_time
                self.parts_stock -= 4
                self.parts_cost += random.randint(400, 800)
                self.repairs_by_id[3] += 1

            elif 95 <= repair_id < 100:  # 5%
                repair_time += random.uniform((48 / (self.workers_amount * 0.6)), (96 / (self.workers_amount * 0.6)))
                self.repair_time_by_id[4] += repair_time
                self.parts_stock -= 5
                self.parts_cost += random.randint(800, 1600)
                self.repairs_by_id[4] += 1

        return repair_time

    def complete_repair(self, repair_time):
        self.completed_repairs += 1
        while self.parts_stock <= 0:
            repair_time += self.check_parts_stock(repair_time)
        self.total_repair_time += repair_time
        self.repair_times.append(repair_time)

        return repair_time

    def check_parts_stock(self, repair_time):
        if self.parts_stock <= 0:
            # czas jesli brakuje czesci
            repair_time += random.randint(5, 10)
            self.orders += 1
            self.parts_stock += self.parts_capacity
            print("Ordering more parts, current stock:", self.parts_stock)
            return repair_time

        return 0

    def run_simulation(self):
        i = 0
        broken = False
        while i < self.num_requests * 2:
            if not broken:
                self.time += random.randint(120, 168)  # 4-7 dzień
                broken = True
            else:
                self.repair_time_occurrences.append(self.time)
                repair_time = self.start_repair()
                repair_time = self.complete_repair(repair_time)
                self.time += repair_time
                print("Repair completed, time taken:", repair_time)
                broken = False
            i += 1

        print("Time of the whole simulation:", self.time)
        print("Time of all repairs:", self.total_repair_time)
        print("System availability:", (1 - self.total_repair_time / self.time) * 100, "%")  # round()
        print("Total repairs completed:", self.completed_repairs)
        print("Average repair time:", self.total_repair_time / self.completed_repairs)
        print("Total parts orders placed:", self.orders)
        print("Total costs of the repairs:", self.parts_cost)
        self.csv_conversion()

    def csv_conversion(self):
        # konkretne przedzialy w jakich dane sie znajduja zaleza od ilosci napraw
        data = [[self.num_requests] + [self.time] + [self.total_repair_time]
                + self.repair_times + self.repair_time_occurrences]
        with open('data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def plot_results(self):
        fig, axs = plt.subplots(2, 2, figsize=(20, 10))
        axs[0, 0].hist(self.repair_times, bins=self.completed_repairs)
        axs[0, 0].set_xlabel("Repair time")
        axs[0, 0].set_ylabel("Frequency")
        axs[0, 0].set_title("Distribution of repair times")

        axs[0, 1].bar(["Completed repairs", "Parts orders"], [self.completed_repairs, self.orders])
        axs[0, 1].set_xlabel("Event")
        axs[0, 1].set_ylabel("Count")
        axs[0, 1].set_title("System events")

        axs[1, 0].bar(["Repair #1", "Repair #2", "Repair #3", "Repair #4", "Repair #5"],
                      [self.repair_time_by_id[0] / self.repairs_by_id[0],
                       self.repair_time_by_id[1] / self.repairs_by_id[1],
                       self.repair_time_by_id[2] / self.repairs_by_id[2],
                       self.repair_time_by_id[3] / self.repairs_by_id[3],
                       self.repair_time_by_id[4] / self.repairs_by_id[4]])
        axs[1, 0].set_xlabel("Repair ID")
        axs[1, 0].set_ylabel("Average time of the repair")
        axs[1, 0].set_title("Average repair time by repair ID")

        axs[1, 1].bar(["Repair #1", "Repair #2", "Repair #3", "Repair #4", "Repair #5"],
                      [self.repairs_by_id[0],
                       self.repairs_by_id[1],
                       self.repairs_by_id[2],
                       self.repairs_by_id[3],
                       self.repairs_by_id[4]])
        axs[1, 1].set_xlabel("Repair ID")
        axs[1, 1].set_ylabel("Amount of occurances of the repair")
        axs[1, 1].set_title("Occurances by repair ID")
        plt.show()


# Example usage
repair_system = RepairSystem(parts_capacity=10, parts_stock=10, workers_amount=10)
repair_system.run_simulation()
repair_system.plot_results()
