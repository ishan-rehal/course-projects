import math
import random
import copy
from circuit import Circuit
from gate import Gate
from net import Net
from pin import Pin
from inputparsing import InputParser
from simulated_annealing import SimulatedAnnealing
from simulated_annealing2 import SimulatedAnnealing2
from visualizer import visualize_circuit
from visualization import visualize_gates
from time import perf_counter

import matplotlib.pyplot as plt  # For plotting the graph
random.seed(0)  # For reproducibility
import sys
sys.setrecursionlimit(10**6)

def output_results(circuit, best_solution, best_cost, output_file="output.txt"):
    
    # Calculate bounding box for the entire circuit
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')

    for gate in best_solution.gates.values():
        min_x = min(min_x, gate.x)
        min_y = min(min_y, gate.y)
        max_x = max(max_x, gate.x + gate.width)
        max_y = max(max_y, gate.y + gate.height)

    bounding_box_width = max_x - min_x
    bounding_box_height = max_y - min_y

    with open(output_file, 'w') as f:
        # Output bounding box dimensions
        f.write(f"bounding_box {bounding_box_width} {bounding_box_height}\n")

        # Adjust gate positions to set the bottom-left corner to (0, 0)
        print(min_x, min_y)
        s=''
        for gate_name, gate in best_solution.gates.items():
            adjusted_x = gate.x - min_x  # Adjust x position
            adjusted_y = gate.y - min_y  # Adjust y position
            s+=(f"{gate_name} {adjusted_x} {adjusted_y}\n")
        s.strip('\n')
        f.write(s)
        # Output total wire length (semi-perimeter cost)
        f.write(f"wire_length {wire_cost}\n")

def dummy_complex_function(n):
    # Simulate O(2 * 10^6 + n log n) operation
    constant_operation = 2 * 10**6*n  # Simulating a constant operation
    result = 0
    for _ in range(constant_operation):
        result += 1

    # Now perform O(n log n) part
    for i in range(n):
        for j in range(int(math.log(n + 1))):  # Adding 1 to avoid log(0)
            result += i * j
    return result


def plot_time_vs_gates(num_gates, sa_times, nlogn_times):
    plt.figure(figsize=(10, 6))
    
    # Plot the actual time taken for simulated annealing
    plt.plot(num_gates, sa_times, marker='o', linestyle='-', color='b', label="Simulated Annealing Time (s)")
    
    # Plot the O(2 * 10^6 + n log n) curve for the benchmark
    plt.plot(num_gates, nlogn_times, marker='x', linestyle='--', color='r', label="O(2 * 10^6*n + n log n) Time (s)")
    
    plt.title('Number of Gates vs. Time Taken for Simulated Annealing and O(2 * 10^6 + n log n)')
    plt.xlabel('Number of Gates')
    plt.ylabel('Time Taken (seconds)')
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # num_gates_list = [ 10, 20, 30, 50, 100, 200, 300, 500, 1000]
    # sa_times_taken = []
    # nlogn_times_taken = []

    # for num_gates in num_gates_list:
    #     print(f"Running simulated annealing with {num_gates} gates...")

    #     # Step 1: Generate input for the specified number of gates
    #     generate(num_gates)

    #     # Step 2: Parse input
    #     input_file = "input.txt"
    #     parser = InputParser(input_file)
    #     parser.parse()
    #     circuit = parser.get_circuit()

    #     # Initialize gates far from each other
    #     spacing = 10  # Adjust the spacing as needed
    #     for i, gate in enumerate(circuit.gates.values()):
    #         gate.set_position(i * spacing, i * spacing)  # Spread out gates diagonally

    #     # Step 3: Run simulated annealing and record time
    #     start_sa = perf_counter()
    #     sa = SimulatedAnnealing2(circuit, initial_temperature=10**8, cooling_rate=0.999, max_iterations=100_00)
    #     best_solution, best_cost = sa.run()
    #     end_sa = perf_counter()

    #     # Record time taken for simulated annealing
    #     sa_time_taken = end_sa - start_sa
    #     sa_times_taken.append(sa_time_taken)

    #     # Step 4: Run O(2 * 10^6 + n log n) loop for the same number of gates and record time
    #     start_nlogn = perf_counter()
    #     dummy_complex_function(num_gates)
    #     end_nlogn = perf_counter()

    #     # Record time taken for O(2 * 10^6 + n log n) loop
    #     nlogn_time_taken = end_nlogn - start_nlogn
    #     nlogn_times_taken.append(nlogn_time_taken)

    #     print(f"Execution time for {num_gates} gates: {sa_time_taken} seconds (SA), {nlogn_time_taken} seconds (O(2 * 10^6 + n log n))")

    #     # Step 5: Output results in the required format
    #     output_results(circuit, best_solution, best_cost, output_file="output.txt")

    # # Step 6: Plot the results
    # plot_time_vs_gates(num_gates_list, sa_times_taken, nlogn_times_taken)
    
    
    # -------------------One time Running--------------------
        # GENERATE input
    # generate(100)
    # Step 1: Parse input
    input_file = "input.txt"  # Example input file path
    parser = InputParser(input_file)
    parser.parse()
    circuit = parser.get_circuit()

    # Initialize gates far from each other
    spacing = 10  # Adjust the spacing as needed
    for i, gate in enumerate(circuit.gates.values()):
        gate.set_position(i * spacing, i * spacing)  # Spread out gates diagonally

    
    # Step 2: Run simulated annealing
    start = perf_counter()
    sa = SimulatedAnnealing2(circuit, initial_temperature=10*8, cooling_rate=0.999, max_iterations=10000)
    best_solution, best_cost = sa.run()
    end = perf_counter()
    wire_cost = best_solution.total_wire_cost()
    # Step 3: Output results in the required format
    output_results(circuit, best_solution, best_cost, output_file="output.txt")
    print("Execution time:", end - start, "seconds")
    print("Total wire cost: ", wire_cost)
    # visualize_circuit(circuit, best_solution, best_cost)
    # visualize_gates("output.txt", input_file, (10, 10))
    # visualize_gates(input_file, "output.txt", (100, 100))  # Visualize the output