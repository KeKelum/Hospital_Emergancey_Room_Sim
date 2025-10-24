## Hospital Emergency Room (ER) Simulation

This project simulates the operation of a **hospital emergency room (ER)** using the **SimPy** discrete-event simulation library in Python.
It models how patients with different priority levels (Critical, Serious, Minor) are treated by a limited number of doctors, and measures performance metrics like waiting times and doctor utilization.

##  **System Components**

- **Patients**: Arrive randomly and are assigned one of three priorities:
    - _Critical_ (highest priority)
    - Serious_        
    - _Minor_ (lowest priority)        
- **Doctors**: Shared resources that treat patients one at a time.    
- **Simulation Logic**: Uses random arrival and service times to mimic real-world unpredictability.    
- **Metrics Tracked**:    
    - Average wait time per patient type        
    - Total doctor busy time        
    - Doctor utilization (%)

**Key Python Libraries**
|Library|Purpose|
|---|---|
|`simpy`|Event-based simulation framework|
|`random`|Generates random arrival and service intervals|
|`statistics`|Calculates mean wait times|
|`matplotlib`|Generates plots for results visualization|

Install them (if not already installed):

```bash
pip install simpy matplotlib
```
## **How to Run the Simulation**

### **1️ Interactive Mode**

This mode lets you enter your own simulation parameters directly in the terminal.
```bash
HospitalER.py
```
Example inputs:
```
Hospital ER Simulation
Press Enter to use defaults.

Number of doctors [default=2]: 2
Average arrival interval (minutes) [default=5]: 3
Average service time per patient (minutes) [default=10]: 8
Total simulation time (minutes) [default=200]: 200
```
The program will then run and print:
```
Running simulation... please wait...

=== Simulation Results ===
Critical average wait: 4.48 minutes
Serious average wait: 23.02 minutes
Minor average wait: 37.10 minutes
Doctor utilization: 94.23%
Total doctor busy time: 376.90 minutes
```
<img width="800" height="500" alt="Figure_1" src="https://github.com/user-attachments/assets/ab4cd97f-38bb-4267-9302-1017c26435a3" /> <br>

### **Scenario Testing**
You can also run predefined experiments to study the impact of different configurations (Number of doctors):
Example scenarios are given in the bottom of the code 
#### Sample output
<img width="640" height="480" alt="Figure_7" src="https://github.com/user-attachments/assets/2c1d3f0e-3269-451e-afab-7c05e60ef27c" />


