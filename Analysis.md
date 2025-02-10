# Router Queue Simulation Analysis
#### TELCOM 2310 - Project 1
#### Ethan He (eth69@pitt.edu)

## 1. Implementation Description

### 1.1 Event Simulator
The simulator implements a discrete event system that models packet arrivals and departures in a router queue. Key components:

- **Probability Calculation**: 
  - Arrival probability: P(arrival) = λ/(λ+μ)
  - Departure probability: P(departure) = μ/(λ+μ)

- **Queue Management**:
  - Tracks current queue length (pkt_in_q)
  - Enforces buffer size limit (n)
  - Counts dropped packets when queue is full

- **Variable Rate Support**:
  - Dynamically adjusts λ based on event progression
  - Implements rate changes according to Table 2

## 2. Results Analysis

### 2.1 Constant Rate Scenarios

#### 2.1.1 Case: λ=80, μ=50, n=50
[Insert plot]
- **Queue Behavior**:
  - Queue fills rapidly due to λ > μ
  - Maintains high occupancy (~100%)
  - Shows fluctuations from departures
- **Packet Drops**:
  - Linear increase in dropped packets
  - Expected due to arrival rate exceeding service rate
  - Drop rate ≈ λ - μ = 30 packets/sec

[Continue with other combinations from Table 1...]

### 2.2 Variable Rate Scenario (μ=120, n=100)
[Insert plot]

Analysis by phase:
1. **0-10% (λ=70)**:
   - Stable queue length
   - No packet drops (λ < μ)

2. **10-70% (λ=200)**:
   - Queue fills rapidly
   - High drop rate (λ > μ)

3. **70-80% (λ=130)**:
   - Slight decrease in queue occupancy
   - Continued but slower packet drops

4. **80-90% (λ=120)**:
   - Queue stabilizes
   - Minimal additional drops

5. **90-100% (λ=70)**:
   - Queue length decreases
   - No new packet drops

## 3. Observations and Conclusions

### 3.1 Impact of Parameters
- **Buffer Size (n)**:
  - Larger buffers delay onset of packet drops
  - Trade-off between drop prevention and latency

- **Arrival Rate (λ)**:
  - When λ > μ: Queue fills, packets drop
  - When λ < μ: Queue stable, no drops
  - When λ ≈ μ: Queue fluctuates near capacity

- **Service Rate (μ)**:
  - Higher μ reduces queue occupancy
  - Critical for preventing packet drops

### 3.2 System Behavior
- Queue fills faster when λ significantly exceeds μ
- Linear drop rate once queue is full
- System shows clear transitions in variable rate scenario

### 3.3 Performance Implications
- Buffer sizing affects both packet loss and latency
- Service rate must match or exceed arrival rate for stability
- Variable rates demonstrate system adaptability
