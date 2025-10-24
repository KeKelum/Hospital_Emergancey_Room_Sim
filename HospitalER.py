import simpy
import random
import statistics

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

random.seed(RANDOM_SEED)
env = simpy.Environment()
doctors = simpy.PriorityResource(env, capacity=NUM_DOCTORS)
env.process(patient_arrival(env, doctors))
env.run(until=SIM_TIME)

print("\n=== Simulation Results ===")
for k, times in wait_times.items():
    if times:
        print(f"{k} average wait: {statistics.mean(times):.2f} minutes")
total_time = NUM_DOCTORS * SIM_TIME
print(f"Doctor utilization: {busy_time / total_time * 100:.2f}%")

