import simpy
import random
import statistics
import matplotlib.pyplot as plt

# Define basic simulation setup
RANDOM_SEED = 42  # for fixed random sequence
ARRIVAL_RATE = 5  # average time between patient arrivals
SERVICE_TIME = 10  # average treatment time
NUM_DOCTORS = 2
SIM_TIME = 200

# Priority mapping
PRIORITY_TYPES = {
    "Critical": 1,
    "Serious": 2,
    "Minor": 3
}

wait_times = {}
for k in PRIORITY_TYPES.keys():
    wait_times[k] = []
busy_time = 0 # Total doctor working time

""" 
Patient Process
arrival -> waiting -> treatment -> departure 
"""
def patient(env, name, doctors):
    """
    Patient with a priority requests treatment.
    Weights [1, 2, 4] mean:
    mostly minor cases, a few serious ones, and rare criticals.
    """
    global busy_time
    priority_type = random.choices(list(PRIORITY_TYPES.keys()), weights=[1,2,4])[0]
    priority = PRIORITY_TYPES[priority_type]
    arrival_time = env.now

    with doctors.request(priority=priority) as req:
        yield req
        wait = env.now - arrival_time
        wait_times[priority_type].append(wait)
        start = env.now
        yield env.timeout(random.expovariate(1.0 / SERVICE_TIME))
        busy_time += env.now - start

""" 
Patient Arrival Generator
Continuously creates new patient processes
"""
def patient_arrival(env, doctors):
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / ARRIVAL_RATE))
        i += 1
        env.process(patient(env, f"Patient {i}", doctors))

# random.seed(RANDOM_SEED)
# env = simpy.Environment()
# doctors = simpy.PriorityResource(env, capacity=NUM_DOCTORS)
# env.process(patient_arrival(env, doctors))
# env.run(until=SIM_TIME)

# print("\n=== Simulation Results ===")
# for k, times in wait_times.items():
#     if times:
#         print(f"{k} average wait: {statistics.mean(times):.2f} minutes")
# total_time = NUM_DOCTORS * SIM_TIME
# print(f"Doctor utilization: {busy_time / total_time * 100:.2f}%")

def interactive_er_simulation():
    """Prompt the user for parameters and run the ER simulation."""
    print("🏥 Hospital ER Simulation (Interactive Mode)")
    print("Enter values below (press Enter to use defaults).")

    # Collect user inputs
    try:
        num_doctors = int(input("Number of doctors [default=2]: ") or 2)
        arrival_rate = float(input("Average arrival interval (minutes) [default=4]: ") or 4)
        service_time = float(input("Average service time per patient (minutes) [default=10]: ") or 10)
        sim_time = int(input("Total simulation time (minutes) [default=200]: ") or 200)
    except ValueError:
        print("Invalid input. Using defaults.")
        num_doctors, arrival_rate, service_time, sim_time = 2, 4, 10, 200

    print("\n⏳ Running simulation... please wait...\n")

    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    doctors = simpy.PriorityResource(env, capacity=num_doctors)
    env.process(patient_arrival(env, doctors))
    env.run(until=sim_time)

    print("\n=== Simulation Results ===")
    for k, times in wait_times.items():
        if times:
            print(f"{k} average wait: {statistics.mean(times):.2f} minutes")
    total_time = num_doctors * sim_time
    print(f"Doctor utilization: {busy_time / total_time * 100:.2f}%")
    print(f"Total Doctor Busy time: {busy_time}")

    # Compute results
    avg_waits = {}
    for k, v in wait_times.items():
        if v:
            avg_waits[k] = statistics.mean(v)
        else:
            avg_waits[k] = 0

    total_time = num_doctors * sim_time
    utilization = busy_time / total_time * 100

    # Bar chart - average waiting times
    plt.figure(figsize=(8, 5))
    plt.bar(avg_waits.keys(), avg_waits.values(), color=['red', 'orange', 'green'])
    plt.title("Average Waiting Time per Patient Category")
    plt.xlabel("Patient Type")
    plt.ylabel("Average Wait (minutes)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # bar for doctor utilization
    plt.figure(figsize=(6, 1.5))
    plt.barh(["Doctor Utilization"], [utilization], color='skyblue')
    plt.xlim(0, 100)
    plt.title("Doctor Utilization (%)")
    plt.xlabel("Percentage")
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.show()


interactive_er_simulation()
