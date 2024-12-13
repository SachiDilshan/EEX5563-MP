import tkinter as tk
from tkinter import messagebox


# Function to perform the First Fit memory allocation algorithm
def first_fit(partitions, jobs):
    """
    Simulates the First Fit algorithm for memory allocation.

    Args:
    partitions (list): List of integers representing partition sizes.
    jobs (list): List of integers representing job sizes.

    Returns:
    allocation (list): List indicating which partition each job is allocated to (-1 if not allocated).
    original_partitions (list): Original sizes of the partitions.
    remaining_partitions (list): Updated sizes of partitions after allocation.
    partition_status (list): Status of each partition ("Free", "Partially Used", "Fully Used").
    """
    # Copy the original partition sizes to preserve them for display
    original_partitions = partitions.copy()

    # Initialize allocation list (-1 means not allocated)
    allocation = [-1] * len(jobs)

    # Initialize partition status to "Free"
    partition_status = ["Free"] * len(partitions)

    # Iterate over each job
    for i, job in enumerate(jobs):
        # Try to allocate the job to the first suitable partition
        for j, partition in enumerate(partitions):
            if partition >= job:  # Check if the partition can accommodate the job
                allocation[i] = j  # Allocate the job to this partition
                partitions[j] -= job  # Reduce the available size of the partition
                # Update the partition status
                partition_status[j] = "Partially Used" if partitions[j] > 0 else "Fully Used"
                break  # Stop searching for partitions for this job

    return allocation, original_partitions, partitions, partition_status


# Function to handle the simulation when the "Run Simulation" button is clicked
def run_simulation():
    try:
        # Parse the user input into lists of integers
        partitions = list(map(int, partition_input.get().split(',')))
        jobs = list(map(int, job_input.get().split(',')))

        # Validate the input to ensure all values are positive
        if any(p <= 0 for p in partitions) or any(j <= 0 for j in jobs):
            raise ValueError("Partition and job sizes must be positive integers.")

        # Run the First Fit algorithm
        allocation, original_partitions, remaining_partitions, partition_status = first_fit(partitions, jobs)

        # Display the results in the output text box
        result_text.delete("1.0", tk.END)  # Clear previous results
        result_text.insert(tk.END, "Job No.\tJob Size\tPartition No.\n")
        for i, job in enumerate(jobs):
            partition_no = allocation[i] + 1 if allocation[i] != -1 else "Not Allocated"
            result_text.insert(tk.END, f"{i + 1}\t\t{job}\t\t{partition_no}\n")

        # Display the status of each partition
        result_text.insert(tk.END, "\nPartition Status:\n")
        for i, (original, remaining, status) in enumerate(
                zip(original_partitions, remaining_partitions, partition_status)):
            result_text.insert(tk.END,
                               f"Partition {i + 1}: Original={original}, Remaining={remaining}, Status={status}\n")

    except ValueError:
        # Show an error message if the input is invalid
        messagebox.showerror("Input Error", "Please enter valid positive integers separated by commas.")


# Function to reset the input fields and result display when the "Reset" button is clicked
def reset_inputs():
    partition_input.delete(0, tk.END)  # Clear the partition input field
    job_input.delete(0, tk.END)  # Clear the job input field
    result_text.delete("1.0", tk.END)  # Clear the result display


# Create the main Tkinter window
root = tk.Tk()
root.title("First Fit Memory Allocation")

# Input labels and entry fields for partitions and jobs
tk.Label(root, text="Partition Sizes (comma-separated):").grid(row=0, column=0, padx=10, pady=5)
partition_input = tk.Entry(root, width=40)
partition_input.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Job Sizes (comma-separated):").grid(row=1, column=0, padx=10, pady=5)
job_input = tk.Entry(root, width=40)
job_input.grid(row=1, column=1, padx=10, pady=5)

# Buttons for running the simulation and resetting the inputs
simulate_button = tk.Button(root, text="Run Simulation", command=run_simulation)
simulate_button.grid(row=2, column=0, pady=10)

reset_button = tk.Button(root, text="Reset", command=reset_inputs)
reset_button.grid(row=2, column=1, pady=10)

# Text box to display the simulation results
result_text = tk.Text(root, height=20, width=80)
result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
