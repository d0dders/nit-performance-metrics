import csv 
from datetime import datetime, timedelta

INPUT_FILENAME = 'results.csv'
OUTPUT_FILENAME = 'output.csv'
INCOMING_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
START_COLUMN_NAME = 'created'
END_COLUMN_NAME = 'updated'
  
average_runtimes = []


def import_data(filename):
    nit_runtimes_list = []
    with open(filename, 'r') as data: 
        csv_input = csv.DictReader(data)
        data = sorted(csv_input, key=lambda row: (row['created']))
        for line in data: 
            start_time = datetime.strptime(line[START_COLUMN_NAME], INCOMING_DATE_FORMAT)
            end_time = datetime.strptime(line[END_COLUMN_NAME], INCOMING_DATE_FORMAT)
            week_commencing = datetime.date(start_time - timedelta(days=start_time.weekday())).strftime("%d/%m/%Y")
            runtime = end_time - start_time
            nit_runtimes_list.append({
                "start_time": start_time,
                "week_commencing": week_commencing,
                "run_time": runtime
                })
    return nit_runtimes_list


def build_weekly_report(nit_runtimes_list):
    weekly_runtimes_dict = {}
    for nit_runtime in nit_runtimes_list: 
        week_commencing = nit_runtime["week_commencing"]
        runtime = nit_runtime["run_time"]
        if week_commencing in weekly_runtimes_dict:
            weekly_runtimes_dict[week_commencing].append(runtime)
        else:
            weekly_runtimes_dict[week_commencing] = [runtime]
    weekly_average_report = []
    for key, value in weekly_runtimes_dict.items():
        week_average = str(sum(value, timedelta()) / len(value))[:10]
        weekly_average_report.append({
            "Week_Commencing": key,
            "Average_Runtime": week_average
        })
    return weekly_average_report

def build_daily_report(nit_runtimes_list):
    daily_runtimes_dict = {}
    for nit_runtime in nit_runtimes_list: 
        day = datetime.date(nit_runtime["start_time"])
        runtime = nit_runtime["run_time"]
        if day in daily_runtimes_dict:
            daily_runtimes_dict[day].append(runtime)
        else:
            daily_runtimes_dict[day] = [runtime]
    daily_average_report = []
    for key, value in daily_runtimes_dict.items():
        day_average = str(sum(value, timedelta()) / len(value))[:10]
        daily_average_report.append({
            "Date": key,
            "Average_Runtime": day_average
        })
    return daily_average_report

def write_csv(average_runtimes):
    with open(OUTPUT_FILENAME, 'w', newline='') as csvfile:
        fieldnames = list(average_runtimes[0].keys())
        csv_output = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_output.writeheader()
        csv_output.writerows(average_runtimes)


if __name__ == "__main__":
    
    nit_runtimes_list = import_data(INPUT_FILENAME)
    average_runtimes = build_weekly_report(nit_runtimes_list)
    #average_runtimes =build_daily_report(nit_runtimes_list)
    print(average_runtimes)
    write_csv(average_runtimes)