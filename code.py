import matplotlib.pyplot as plt


# Disk Scheduling Algorithms
def fcfs(requests, head):
    sequence = [head] + requests
    seek_time = sum(abs(sequence[i] - sequence[i-1]) for i in range(1, len(sequence)))
    return sequence, seek_time


def sstf(requests, head):
    sequence = [head]
    seek_time = 0
    pending = requests.copy()
    while pending:
        closest = min(pending, key=lambda x: abs(x - sequence[-1]))
        seek_time += abs(sequence[-1] - closest)
        sequence.append(closest)
        pending.remove(closest)
    return sequence, seek_time


def scan(requests, head, disk_size):
    sorted_requests = sorted(requests + [disk_size])
    left = [r for r in sorted_requests if r < head]
    right = [r for r in sorted_requests if r >= head]
    sequence = [head] + right + left[::-1]
    seek_time = sum(abs(sequence[i] - sequence[i-1]) for i in range(1, len(sequence)))
    return sequence, seek_time


def cscan(requests, head, disk_size):
    sorted_requests = sorted(requests + [disk_size, 0])
    right = [r for r in sorted_requests if r >= head]
    left = [r for r in sorted_requests if r < head]
    sequence = [head] + right + [0] + left
    seek_time = sum(abs(sequence[i] - sequence[i-1]) for i in range(1, len(sequence)))
    return sequence, seek_time


# Plot Function
def plot_results(algorithm, sequence, seek_time, requests, final=False):
    avg_seek_time = seek_time / len(requests)
    throughput = len(requests) / (seek_time if seek_time != 0 else 1)


    plt.figure(figsize=(8, 5))
    plt.plot(sequence, range(len(sequence)), marker='o', linestyle='-', color='b', label="Head Movement")


    # Mark request points
    for i, req in enumerate(sequence):
        plt.text(req, i, str(req), fontsize=10, ha='right', color='red')


    plt.xlabel("Cylinder Number")
    plt.ylabel("Request Order")
    title_prefix = "FINAL EXECUTION: " if final else ""
    plt.title(f"{title_prefix}{algorithm} Disk Scheduling\nSeek Time: {seek_time} | Avg Seek Time: {avg_seek_time:.2f} | Throughput: {throughput:.2f}")
    plt.grid()
    plt.legend()
    plt.show()


# Simulation Function
def run_simulation():
    # User Inputs
    requests = list(map(int, input("Enter disk requests separated by space: ").split()))
    head = int(input("Enter initial head position: "))
    disk_size = int(input("Enter total disk size: "))


    algorithms = {"FCFS": fcfs, "SSTF": sstf, "SCAN": scan, "C-SCAN": cscan}
    results = {}


    for algorithm, func in algorithms.items():
        sequence, seek_time = func(requests, head) if algorithm in ["FCFS", "SSTF"] else func(requests, head, disk_size)
        results[algorithm] = (sequence, seek_time)
        plot_results(algorithm, sequence, seek_time, requests)
        print(f"{algorithm} Seek Time: {seek_time} units")


    # Finding the best algorithm
    best_algorithm = min(results, key=lambda x: results[x][1])
    best_sequence, best_seek_time = results[best_algorithm]


    print(f"\n✅ The best algorithm is {best_algorithm} with Seek Time: {best_seek_time} units")
   
    # Final Execution of Best Algorithm
    plot_results(best_algorithm, best_sequence, best_seek_time, requests, final=True)


if __name__ == "__main__":
    run_simulation()
