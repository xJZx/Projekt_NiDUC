import csv

from matplotlib import pyplot as plt

# opening the CSV file
with open('data.csv', mode='r') as file:
    # reading the CSV file
    csvFile = csv.reader(file)

    num_requests = 0
    time = 0
    total_repair_time = 0
    repair_times = []
    repair_time_occurances = []
    # displaying the contents of the CSV file
    for lines in csvFile:
        num_requests = int(lines[0])
        time = float(lines[1])
        total_repair_time = float(lines[2])

        for i in range(2 * num_requests + 1):
            if 0 < i <= num_requests:
                repair_times.append(lines[i + 2])

            elif num_requests <= i:
                repair_time_occurances.append(lines[i + 2])

    def plot_results():
        fig, axs = plt.subplots(figsize=(20, 10))
        axs.hist(repair_time_occurances, bins=repair_time_occurances)
        axs.set_xlabel("Time")
        axs.set_ylabel("State")
        axs.set_title("Distribution of machine states")
        plt.show()

    print(num_requests)
    print(time)
    print(total_repair_time)
    for i in repair_times:
        print(i)
    for i in repair_time_occurances:
        print(i)

    plot_results()


