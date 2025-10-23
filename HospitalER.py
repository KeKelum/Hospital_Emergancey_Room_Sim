import simpy
import random

RANDOM_SEED = 42
ARRIVAL_RATE = 5
SERVICE_TIME = 8  # average treatment time
NUM_DOCTORS = 2
SIM_TIME = 60

def patient(env, name, doctors):
    """Patient process: request a doctor, get treated, then leave."""
    arrival_time = env.now
    print(f"{name} arrives at {arrival_time:.2f}")

    with doctors.request() as req:
        yield req
        wait = env.now - arrival_time
        print(f"{name} starts treatment at {env.now:.2f} after waiting {wait:.2f}")
        yield env.timeout(random.expovariate(1.0 / SERVICE_TIME))
        print(f"{name} leaves at {env.now:.2f}")

def patient_arrival(env, doctors):
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / ARRIVAL_RATE))
        i += 1
        env.process(patient(env, f"Patient {i}", doctors))

random.seed(RANDOM_SEED)
env = simpy.Environment()
doctors = simpy.Resource(env, capacity=NUM_DOCTORS)
env.process(patient_arrival(env, doctors))
env.run(until=SIM_TIME)
