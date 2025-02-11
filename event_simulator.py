import random
import argparse

def get_lambda(event_num, total_events):
    """ Returns the appropriate λ based on event percentage (for variable λ case). """
    percentage = (event_num / total_events) * 100

    if percentage <= 10:
        return 70
    elif percentage <= 70:
        return 200
    elif percentage <= 80:
        return 130
    elif percentage <= 90:
        return 120
    else:
        return 70

def simulate_packets(lambda_rate, mu_rate, buffer_size, num_events, output_file, variable_lambda, debug=False):
    pkt_in_q = 0  # Number of packets in queue
    pkt_dropped = 0  # Dropped packets counter
    last_debug_print = 0  # Track last debug print event

    print(f"\nSimulation Parameters:")
    print(f"λ (arrival rate): {lambda_rate if not variable_lambda else 'variable'} packets/sec")
    print(f"μ (departure rate): {mu_rate} packets/sec")
    print(f"n (buffer size): {buffer_size} packets")
    print(f"Total events: {num_events}\n")

    with open(output_file, "w") as f:
        for event_num in range(1, num_events + 1):
            # Get λ dynamically if variable input rate is enabled
            current_lambda = get_lambda(event_num, num_events) if variable_lambda else lambda_rate
            
            # Probability of arrival
            P_arrival = current_lambda / (mu_rate + current_lambda)
            y = random.random()  # Random number in [0,1)

            if debug and (event_num <= 20 or event_num % 100 == 0):  # Debug first 20 events and every 100th after
                print(f"\nEvent {event_num}:")
                print(f"Current λ: {current_lambda}")
                print(f"P_arrival: {P_arrival:.3f}")
                print(f"Random y: {y:.3f}")
                print(f"Queue before: {pkt_in_q}")

            if y < P_arrival:  # Arrival event
                if pkt_in_q < buffer_size:
                    pkt_in_q += 1
                    if debug and (event_num <= 20 or event_num % 100 == 0):
                        print(f"ARRIVAL: Queue increased to {pkt_in_q}")
                else:
                    pkt_dropped += 1
                    if debug and (event_num <= 20 or event_num % 100 == 0):
                        print(f"ARRIVAL: Packet dropped (queue full) - Total drops: {pkt_dropped}")
            else:  # Departure event
                if pkt_in_q > 0:
                    pkt_in_q -= 1
                    if debug and (event_num <= 20 or event_num % 100 == 0):
                        print(f"DEPARTURE: Queue decreased to {pkt_in_q}")
                elif debug and (event_num <= 20 or event_num % 100 == 0):
                    print("DEPARTURE: No packets to depart")

            # Write event state to file
            f.write(f"{event_num} {pkt_in_q} {pkt_dropped}\n")

            # Print periodic statistics
            if debug and event_num % 1000 == 0 and event_num != last_debug_print:
                print(f"\nStatus at event {event_num}:")
                print(f"Queue length: {pkt_in_q}")
                print(f"Total drops: {pkt_dropped}")
                last_debug_print = event_num

    print(f"\nSimulation complete:")
    print(f"Final queue length: {pkt_in_q}")
    print(f"Total packets dropped: {pkt_dropped}")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Packet queue simulator")
    parser.add_argument('-l', '--lambda_rate', type=int, required=False, help="Arrival rate (λ) in packets/sec")
    parser.add_argument('-m', '--mu_rate', type=int, required=True, help="Departure rate (µ) in packets/sec")
    parser.add_argument('-n', '--buffer_size', type=int, required=True, help="Queue buffer size (n)")
    parser.add_argument('-x', '--num_events', type=int, default=1000000, help="Total number of events (default: 1,000,000)")
    parser.add_argument('-o', '--output_file', type=str, default="output.txt", help="Output file for results")
    parser.add_argument('--variable_lambda', action='store_true', help="Enable variable arrival rate λ (Table 2)")
    parser.add_argument('--debug', action='store_true', help="Enable debug output")

    args = parser.parse_args()

    if args.variable_lambda and args.lambda_rate:
        parser.error("Cannot use both fixed and variable lambda at the same time.")

    lambda_rate = args.lambda_rate if args.lambda_rate else 70  # Default if not provided

    simulate_packets(lambda_rate, args.mu_rate, args.buffer_size, args.num_events, 
                    args.output_file, args.variable_lambda, args.debug)
