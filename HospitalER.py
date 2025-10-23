import simpy
import random

# Define basic simulation setup
RANDOM_SEED = 42  # for fixed random sequence
ARRIVAL_RATE = 5  # average time between patient arrivals
SERVICE_TIME = 8  # average treatment time
NUM_DOCTORS = 2
SIM_TIME = 60

# Priority mapping
PRIORITY_TYPES = {
    "Critical": 1,
    "Serious": 2,
    "Minor": 3
}

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
    priority_type = random.choices(list(PRIORITY_TYPES.keys()), weights=[1,2,4])[0]
    priority = PRIORITY_TYPES[priority_type]
    arrival_time = env.now

    print(f"{name} ({priority_type}) arrives at {arrival_time:.2f}")

    with doctors.request(priority=priority) as req:
        yield req
        wait = env.now - arrival_time
        print(f"  {name} starts at {env.now:.2f} after waiting {wait:.2f}")
        yield env.timeout(random.expovariate(1.0 / SERVICE_TIME))
        print(f"  {name} ({priority_type}) leaves at {env.now:.2f}")

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
