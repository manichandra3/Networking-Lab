import threading
import random
import time


class Channel:
    lock = threading.Lock()
    is_busy = False


class Station(threading.Thread):
    SLOT_TIME = 0.0000512

    def __init__(self, id, total_slots):
        super().__init__()
        self.id = id
        self.total_slots = total_slots
        self.transmission_times = []

    def run(self):
        for slot in range(self.total_slots):
            with Channel.lock:
                if not Channel.is_busy:
                    self.transmit(slot)
                else:
                    time.sleep(self.SLOT_TIME)

    def transmit(self, slot):
        print(f"Station {self.id} is ready to transmit at slot {slot}.")

        Channel.is_busy = True
        time.sleep(self.SLOT_TIME)

        if random.choice([True, False]):
            print(f"Collision detected by Station {self.id} at slot {slot}!")
            Channel.is_busy = False

            backoff_time = random.uniform(0, self.SLOT_TIME)
            print(f"Station {self.id} waiting for {backoff_time:.6f} seconds before retrying.")
            time.sleep(backoff_time)
        else:
            print(f"Station {self.id} successfully transmitted at slot {slot}.")
            self.transmission_times.append(slot)
            Channel.is_busy = False


def main():
    N = int(input("Enter the number of stations (N): "))
    total_slots = int(input("Enter the total number of time slots to simulate: "))

    stations = [Station(i + 1, total_slots) for i in range(N)]

    for station in stations:
        station.start()

    for station in stations:
        station.join()

    print("\nTransmission times for each station:")
    for station in stations:
        print(f"Station {station.id}: Transmitted at slots {station.transmission_times}")


if __name__ == "__main__":
    main()
