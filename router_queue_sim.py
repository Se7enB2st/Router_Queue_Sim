import argparse
import random

def simulate_events(arrival_rate, departure_rate, buffer_size, total_events, output_file):
    # Initialize state variables
    pkt_in_q = 0  # Packets in queue
    pkt_dropped = 0  # Packets dropped

    # Open file to write simulation results
    with open(output_file, 'w') as f:
        # Simulate events
        for event_number in range(1, total_events + 1):
            # Calculate probabilities for arrival and departure
            prob_arrival = arrival_rate / (arrival_rate + departure_rate)
            prob_departure = 1 - prob_arrival

            # Generate a random number to decide event type
            rand_num = random.random()
            if rand_num < prob_arrival:  # Arrival event
                if pkt_in_q < buffer_size:
                    pkt_in_q += 1
                else:
                    pkt_dropped += 1
            else:  # Departure event
                if pkt_in_q > 0:
                    pkt_in_q -= 1

            # Write the state to the file
            f.write(f"{event_number} {pkt_in_q} {pkt_dropped}\n")

def main():
    parser = argparse.ArgumentParser(description="Simulate packet events at a router.")
    parser.add_argument('-a', '--arrival-rate', type=float, required=True, help="Packet arrival rate (λ) in packets/sec.")
    parser.add_argument('-d', '--departure-rate', type=float, required=True, help="Packet departure rate (μ) in packets/sec.")
    parser.add_argument('-b', '--buffer-size', type=int, required=True, help="Size of the buffer in packets.")
    parser.add_argument('-e', '--events', type=int, default=1000000, help="Total number of events to simulate (default: 1,000,000).")
    parser.add_argument('-o', '--output-file', type=str, required=True, help="Output file to write simulation results.")

    args = parser.parse_args()

    simulate_events(
        arrival_rate=args.arrival_rate,
        departure_rate=args.departure_rate,
        buffer_size=args.buffer_size,
        total_events=args.events,
        output_file=args.output_file
    )

if __name__ == "__main__":
    main()
