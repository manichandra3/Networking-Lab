import random

SLOT_TIME = 51.2


def csma_cd_simulation(num_stations, total_slots):
    # (0 - idle, 1 - transmitting, 2 - in backoff)
    station_states = [0] * num_stations
    successful_transmissions = [-1] * num_stations

    for slot in range(total_slots):
        transmitting_stations = []

        for station in range(num_stations):
            if station_states[station] == 0:
                if random.random() < 0.1:
                    transmitting_stations.append(station)
            elif station_states[station] == 2:
                station_states[station] = 0

        if len(transmitting_stations) == 1:
            station = transmitting_stations[0]
            if successful_transmissions[station] == -1:
                successful_transmissions[station] = slot
            station_states[station] = 1
        elif len(transmitting_stations) > 1:
            print(f"Collision detected at slot {slot} by stations {transmitting_stations}")
            for station in transmitting_stations:
                station_states[station] = 2

    print("\nSuccessful Transmission Times:")
    for station, time in enumerate(successful_transmissions):
        if time != -1:
            print(f"Station {station + 1} successfully transmitted at slot {time}")
        else:
            print(f"Station {station + 1} did not successfully transmit.")


N = int(input("Enter number of stations (N): "))
total_time_slots = int(input("Enter total number of time slots to simulate: "))

csma_cd_simulation(N, total_time_slots)
