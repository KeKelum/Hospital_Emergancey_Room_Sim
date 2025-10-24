import simpy
import random
import statistics
import matplotlib.pyplot as plt


# GLOBAL DEFAULT PARAMETERS
RANDOM_SEED = 42
DEFAULT_ARRIVAL_RATE = 5       # average time between patient arrivals
DEFAULT_SERVICE_TIME = 10      # average treatment time
DEFAULT_NUM_DOCTORS = 2
DEFAULT_SIM_TIME = 200

# Priority levels: lower number = higher priority
PRIORITY_TYPES = {"Critical": 1, "Serious": 2, "Minor": 3}


# -----------------------------
# Patient Process
# arrival -> waiting -> treatment -> departure 
# -----------------------------
def patient(env, name, doctors, service_time, wait_times, busy_time_ref):
    priority_type = random.choices(list(PRIORITY_TYPES.keys()), weights=[1, 2, 4])[0]
    priority = PRIORITY_TYPES[priority_type]
    arrival_time = env.now

    # Request a doctor according to priority
    with doctors.request(priority=priority) as req:
        yield req

        # Record waiting time
        wait = env.now - arrival_time
        wait_times[priority_type].append(wait)

        # Treatment (service time follows exponential distribution)
        start = env.now
        yield env.timeout(random.expovariate(1.0 / service_time))
        busy_time_ref[0] += env.now - start


# -----------------------------
# Patient Arrival Generator
# Continuously creates new patient processes
# -----------------------------
def patient_arrival(env, doctors, arrival_rate, service_time, wait_times, busy_time_ref):
    """Generates patient arrivals at random intervals."""
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / arrival_rate))
        i += 1
        env.process(patient(env, f"Patient {i}", doctors, service_time, wait_times, busy_time_ref))


# -----------------------------
# RUN SINGLE SIMULATION
# -----------------------------
def run_simulation(num_doctors, arrival_rate, service_time, sim_time):
    """Run the ER simulation once and return performance metrics."""
    random.seed(RANDOM_SEED)

    # Setup environment
    env = simpy.Environment()
    doctors = simpy.PriorityResource(env, capacity=num_doctors)
    wait_times = {k: [] for k in PRIORITY_TYPES.keys()}
    busy_time_ref = [0]  # use list for mutability in nested scope

    # Start processes
    env.process(patient_arrival(env, doctors, arrival_rate, service_time, wait_times, busy_time_ref))
    env.run(until=sim_time)

    # Compute results
    avg_waits = {k: (statistics.mean(v) if v else 0) for k, v in wait_times.items()}
    total_time = num_doctors * sim_time
    utilization = busy_time_ref[0] / total_time * 100

    return avg_waits, utilization, busy_time_ref[0]


# -----------------------------
# INTERACTIVE SIMULATION
# -----------------------------
def interactive_simulation():
    """Prompt user for parameters, run the simulation, and show results + charts."""
    print("Hospital ER Simulation")
    print("Press Enter to use defaults.\n")

    # User inputs
    try:
        num_doctors = int(input(f"Number of doctors [default={DEFAULT_NUM_DOCTORS}]: ") or DEFAULT_NUM_DOCTORS)
        arrival_rate = float(input(f"Average arrival interval (minutes) [default={DEFAULT_ARRIVAL_RATE}]: ") or DEFAULT_ARRIVAL_RATE)
        service_time = float(input(f"Average service time per patient (minutes) [default={DEFAULT_SERVICE_TIME}]: ") or DEFAULT_SERVICE_TIME)
        sim_time = int(input(f"Total simulation time (minutes) [default={DEFAULT_SIM_TIME}]: ") or DEFAULT_SIM_TIME)
    except ValueError:
        print("Invalid input. Using default parameters.")
        num_doctors, arrival_rate, service_time, sim_time = DEFAULT_NUM_DOCTORS, DEFAULT_ARRIVAL_RATE, DEFAULT_SERVICE_TIME, DEFAULT_SIM_TIME

    print("\nRunning simulation... please wait...\n")

    # Run simulation
    avg_waits, utilization, busy_time = run_simulation(num_doctors, arrival_rate, service_time, sim_time)

    # Display results
    print("=== Simulation Results ===")
    for k, avg in avg_waits.items():
        print(f"{k} average wait: {avg:.2f} minutes")
    print(f"Doctor utilization: {utilization:.2f}%")
    print(f"Total doctor busy time: {busy_time:.2f} minutes\n")

    # Visualize
    visualize_results(avg_waits)


# -----------------------------
# VISUALIZATION
# -----------------------------
def visualize_results(avg_waits):
    """Generate visualizations for waiting times and utilization."""
    # Bar chart - average waiting times
    plt.figure(figsize=(8, 5))
    plt.bar(avg_waits.keys(), avg_waits.values(), color=['red', 'orange', 'green'])
    plt.title("Average Waiting Time per Patient Category")
    plt.xlabel("Patient Type")
    plt.ylabel("Average Wait (minutes)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


# -----------------------------
# SCENARIO COMPARISON
# -----------------------------
def scenario_analysis(priority_type, arrival_rate_plot=DEFAULT_ARRIVAL_RATE):
    """Run multiple simulations for different numbers of doctors and compare results."""
    scenarios = [2, 3, 4]
    avg_waits_all = []

    for d in scenarios:
        avg_waits, _, _ = run_simulation(num_doctors=d,
                                         arrival_rate=arrival_rate_plot,
                                         service_time=DEFAULT_SERVICE_TIME,
                                         sim_time=DEFAULT_SIM_TIME)
        avg_waits_all.append(avg_waits[priority_type])

    # Plot comparison
    plt.plot(scenarios, avg_waits_all, marker='o', color='purple')
    plt.title(f"Effect of Number of Doctors on {priority_type} Case Wait Times")
    plt.xlabel("Number of Doctors")
    plt.ylabel("Average Wait (minutes)")
    plt.grid(True)
    plt.show()


# -----------------------------
# Interactive mode
interactive_simulation()

# scenario comparison
# scenario_analysis("Critical")
# scenario_analysis("Serious")
# scenario_analysis("Minor")
# scenario_analysis("Critical",10)
