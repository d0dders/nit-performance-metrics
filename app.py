import csv 
from datetime import datetime, timedelta

filename ="results.csv"

INCOMING_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
START_COLUMN_NAME = 'created'
END_COLUMN_NAME = 'updated'
  
interim_metrics = {}
average_runtimes = []

with open(filename, 'r') as data: 
      
    csv_input = csv.DictReader(data)
    data = sorted(csv_input, key=lambda row: (row['created']))
    for line in data: 
        
        start_time = datetime.strptime(line[START_COLUMN_NAME], INCOMING_DATE_FORMAT)
        week_commencing = datetime.date(start_time - timedelta(days=start_time.weekday())).strftime("%d/%m/%Y")
        end_time = datetime.strptime(line[END_COLUMN_NAME], INCOMING_DATE_FORMAT)
        runtime = end_time - start_time
        if week_commencing in interim_metrics:
            interim_metrics[week_commencing].append(runtime)
        else:
            interim_metrics[week_commencing] = [runtime]
        
    for key, value in interim_metrics.items():
        average_runtime = str(sum(value, timedelta()) / len(value))[:10]
        average_runtimes.append({
            "Week_Commencing": key,
            "Average_Runtime": average_runtime
        })
        
    print(average_runtimes)


with open('output.csv', 'w', newline='') as csvfile:
    csv_output = csv.DictWriter(csvfile, fieldnames=['Week_Commencing', 'Average_Runtime'])
    for row in average_runtimes:
        csv_output.writerow(row)