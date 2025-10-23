import simpy
import random

# Step 1: Define basic simulation setup
RANDOM_SEED = 42
ARRIVAL_RATE = 5  # average time between patient arrivals (minutes)
SIM_TIME = 60     # total simulation time in minutes

def patient_arrival(env):
    """Generate patients arriving randomly."""
    patient_id = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / ARRIVAL_RATE))
        patient_id += 1
        print(f"Time {env.now:.2f}: Patient {patient_id} arrived")

# Initialize environment
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start process
env.process(patient_arrival(env))

# Run simulation
env.run(until=SIM_TIME)
