import random
import logging


class HarmonySearch:
    def __init__(self, nurses, days, shifts, min_head_nurses_per_shift, harmony_memory_size, max_iterations, harmony_memory_consideration_rate, pitch_adjustment_rate):
        self.nurses = nurses
        self.days = days
        self.shifts = shifts
        self.min_head_nurses_per_shift = min_head_nurses_per_shift
        self.harmony_memory_size = harmony_memory_size
        self.max_iterations = max_iterations
        self.harmony_memory_consideration_rate = harmony_memory_consideration_rate
        self.pitch_adjustment_rate = pitch_adjustment_rate
        self.harmony_memory = []

    def initialize_harmony_memory(self):
        for _ in range(self.harmony_memory_size):
            schedule = self.generate_random_schedule()
            self.harmony_memory.append(schedule)

    def generate_random_schedule(self):
        schedule = {}
        for day in self.days:
            schedule[day] = {}
            for shift in self.shifts:
                head_nurses = random.sample(
                    self.nurses["Head Nurse"], k=self.min_head_nurses_per_shift)
                junior_nurses = random.sample(self.nurses["Junior Nurse"], k=random.randint(
                    1, len(self.nurses["Junior Nurse"])))
                schedule[day][shift] = {
                    "Head Nurse": head_nurses, "Junior Nurse": junior_nurses}
        return schedule

    def improvisation(self):
        new_schedule = {}
        for day in self.days:
            new_schedule[day] = {}
            for shift in self.shifts:
                if random.random() < self.harmony_memory_consideration_rate:
                    random_harmony = random.choice(self.harmony_memory)
                    new_schedule[day][shift] = random_harmony[day][shift]
                else:
                    new_schedule[day][shift] = self.generate_random_schedule()[
                        day][shift]

                if random.random() < self.pitch_adjustment_rate:
                    new_schedule[day][shift]["Junior Nurse"] = random.sample(
                        self.nurses["Junior Nurse"], k=random.randint(1, len(self.nurses["Junior Nurse"])))

        return new_schedule

    def evaluate_schedule(self, schedule):
        score = 0
        for day in schedule:
            for shift in schedule[day]:
                if len(schedule[day][shift]["Head Nurse"]) >= self.min_head_nurses_per_shift:
                    score += 1
        return score

    def update_harmony_memory(self, new_schedule):
        new_schedule_score = self.evaluate_schedule(new_schedule)
        worst_schedule = min(self.harmony_memory,
                             key=lambda s: self.evaluate_schedule(s))
        worst_schedule_score = self.evaluate_schedule(worst_schedule)

        if new_schedule_score > worst_schedule_score:
            self.harmony_memory.remove(worst_schedule)
            self.harmony_memory.append(new_schedule)

    def run(self):
        self.initialize_harmony_memory()
        for iteration in range(self.max_iterations):
            new_schedule = self.improvisation()
            self.update_harmony_memory(new_schedule)

        best_schedule = max(self.harmony_memory,
                            key=lambda s: self.evaluate_schedule(s))
        return best_schedule
