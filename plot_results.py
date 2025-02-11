import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np
import os

plt.style.use('default')

def get_args(argv):
    parser = argparse.ArgumentParser(description="Program for plotting simulator results")
    parser.add_argument('-i', '--input-file', required=True, help="Path to the input data file")
    parser.add_argument('-o', '--output-file', required=True, help="Path to save the output plot")
    parser.add_argument('-t', '--title', required=False, help="Title for the plot")
    parser.add_argument('--normalize', action='store_true', help="Normalize data for better visualization")
    parser.add_argument('--zoom', type=int, help="Number of events to zoom into")
    parser.add_argument('--debug', action='store_true', help="Print debug information")
    parser.add_argument('--variable-rate', action='store_true', help="Show variable rate change points")
    return parser.parse_args()

def plot_data(event_seq_points, queue_len_points, dropped_count_points, args, zoom=False):
    if args.debug:
        print("\nPlotting Debug Info:")
        print(f"Number of points: {len(event_seq_points)}")
        print(f"Queue length range: {min(queue_len_points)} to {max(queue_len_points)}")
        print(f"Dropped packets range: {min(dropped_count_points)} to {max(dropped_count_points)}")
        
    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('white')
    
    # Convert to numpy arrays
    event_seq_points = np.array(event_seq_points)
    queue_len_points = np.array(queue_len_points)
    dropped_count_points = np.array(dropped_count_points)
    
    # Apply zoom if requested
    if zoom and args.zoom:
        mask = event_seq_points <= args.zoom
        event_seq_points = event_seq_points[mask]
        queue_len_points = queue_len_points[mask]
        dropped_count_points = dropped_count_points[mask]
        if args.debug:
            print(f"\nZoomed view stats (first {args.zoom} events):")
            print(f"Queue length range: {min(queue_len_points)} to {max(queue_len_points)}")
            print(f"Dropped packets range: {min(dropped_count_points)} to {max(dropped_count_points)}")
    
    # Sample the data for better visualization (only if not zoomed)
    if not zoom and len(event_seq_points) > 10000:
        indices = np.linspace(0, len(event_seq_points)-1, 10000, dtype=int)
        event_seq_points = event_seq_points[indices]
        queue_len_points = queue_len_points[indices]
        dropped_count_points = dropped_count_points[indices]
    
    # Plot queue length as points with larger size and less transparency
    ax1.scatter(event_seq_points, queue_len_points, 
                label="Queue Length (pkt_in_q)", 
                color="blue",
                s=5 if zoom else 1,  # increase point size from 2 to 5 for zoom
                alpha=0.5 if zoom else 0.1,  # increase opacity
                rasterized=True)
    
    ax1.set_xlabel("Event Number")
    ax1.set_ylabel("Queue Length (pkt_in_q)", color="blue")
    ax1.tick_params(axis='y', labelcolor="blue")
    ax1.grid(True, linestyle='--', alpha=0.3)

    ax2 = ax1.twinx()
    
    # Plot dropped packets
    line2, = ax2.plot(event_seq_points, dropped_count_points, 
             label="Dropped Packets (pkt_dropped)", 
             color="orange", 
             linewidth=1.5,
             linestyle='--')
    
    # Add variable rate change indicators if requested
    if args.variable_rate:
        events = [0.1, 0.7, 0.8, 0.9, 1.0]
        rates = [70, 200, 130, 120, 70]
        max_events = max(event_seq_points)
        for i, (e, r) in enumerate(zip(events, rates)):
            ax1.axvline(x=e * max_events, color='gray', linestyle=':', alpha=0.5)
            ax1.text(e * max_events, ax1.get_ylim()[1], f'λ={r}', 
                    rotation=90, verticalalignment='bottom')
    
    ax2.set_ylabel("Dropped Packets", color="orange")
    ax2.tick_params(axis='y', labelcolor="orange")
    
    if args.normalize:
        ax1.set_ylim(-0.1, 1.1)
        ax2.set_ylim(-0.1, 1.1)
    else:
        ax1.set_ylim(bottom=0)
        ax2.set_ylim(bottom=0)
    
    ax1.set_axisbelow(True)
    ax1.legend(loc='upper left', framealpha=0.8)
    ax2.legend(loc='upper right', framealpha=0.8)
    
    title = args.title if args.title else "Simulation Results"
    if zoom:
        title = f"First {args.zoom} Events - {title}"
    if args.normalize:
        title += " (Normalized)"
    plt.title(title)
    
    plt.tight_layout()
    
    # Save with modified filename for zoom plots
    output_file = args.output_file
    if zoom:
        base, ext = os.path.splitext(output_file)
        output_file = f"{base}_zoom{ext}"
    plt.savefig(output_file, dpi=300)
    if args.debug:
        print(f"\nPlot saved to: {output_file}")

    # Add annotations for key events
    if zoom:
        # Find first non-zero queue length
        first_queue = next((i for i, q in enumerate(queue_len_points) if q > 0), None)
        if first_queue is not None:
            ax1.annotate('First queue build-up',
                        xy=(event_seq_points[first_queue], queue_len_points[first_queue]),
                        xytext=(10, 10), textcoords='offset points',
                        arrowprops=dict(arrowstyle='->'))

def main(argv):
    args = get_args(argv)
    
    if args.debug:
        print(f"\nReading data from: {args.input_file}")
    
    event_seq_points = []
    queue_len_points = []
    dropped_count_points = []

    # Read data from file
    with open(args.input_file, 'r') as f:
        for line in f:
            parts = line.split()
            event_seq_points.append(int(parts[0]))
            queue_len_points.append(int(parts[1]))
            dropped_count_points.append(int(parts[2]))
    
    if args.debug:
        print("\nData Summary:")
        print(f"Total events read: {len(event_seq_points)}")
        print(f"Initial queue length: {queue_len_points[0]}")
        print(f"Final queue length: {queue_len_points[-1]}")
        print(f"Initial dropped packets: {dropped_count_points[0]}")
        print(f"Final dropped packets: {dropped_count_points[-1]}")

    # Debug prints for dropped packets
    print("\nAnalyzing dropped packets:")
    print(f"First 20 points: {dropped_count_points[:20]}")
    
    # Find first non-zero dropped packet
    first_drop = next((i for i, x in enumerate(dropped_count_points) if x > 0), None)
    if first_drop is not None:
        print(f"\nFirst packet drop occurs at event {event_seq_points[first_drop]}")
        print(f"Data at that point:")
        print(f"Event: {event_seq_points[first_drop]}")
        print(f"Queue Length: {queue_len_points[first_drop]}")
        print(f"Dropped Packets: {dropped_count_points[first_drop]}")
    
    # Print some statistics
    print(f"\nDropped packets statistics:")
    print(f"Total number of drops: {dropped_count_points[-1]}")
    print(f"Max queue length: {max(queue_len_points)}")

    if args.normalize:
        max_queue_len = max(queue_len_points) if queue_len_points else 1
        max_dropped = max(dropped_count_points) if dropped_count_points else 1
        if args.debug:
            print(f"\nNormalization factors:")
            print(f"Max queue length: {max_queue_len}")
            print(f"Max dropped packets: {max_dropped}")
        
        queue_len_points = [q / max_queue_len if max_queue_len > 0 else 0 for q in queue_len_points]
        dropped_count_points = [d / max_dropped if max_dropped > 0 else 0 for d in dropped_count_points]

    # Debug prints before normalization
    print("Before normalization:")
    print(f"Queue length first 20 points: {queue_len_points[:20]}")
    print(f"Queue length max: {max(queue_len_points)}")

    # Debug prints after normalization
    print("\nAfter normalization:")
    print(f"Queue length first 20 points: {queue_len_points[:20]}")
    print(f"Dropped packets first 20 points: {dropped_count_points[:20]}")

    # Create plots
    plot_data(event_seq_points, queue_len_points, dropped_count_points, args)
    if args.zoom:
        plot_data(event_seq_points, queue_len_points, dropped_count_points, args, zoom=True)

if __name__ == "__main__":
    main(sys.argv[1:])


