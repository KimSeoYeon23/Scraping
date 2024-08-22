import csv

def save_to_file(file_name, jobs):
    file = open(f"{file_name}-jobs.csv", "w")
    writer = csv.writer(file)
    writer.writerow(["Title", "Company", "Reward", "Link"])

    for job in jobs:
        writer.writerow(list(job.values()))

    file.close()

    print('CSV file has been created!')
