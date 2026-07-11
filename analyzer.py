import re
import gzip
import time
from collections import Counter
from report import generate_report


def process_log_file(file_path , start_hour = None, end_hour = None, output_file = None):
    start_time = time.time()
    print("Reading... \n")

    total_lines = 0
    corrupted_lines = 0

    ip_counter = Counter()
    endpoint_counter = Counter()
    status_counter = Counter()
    hour_counter = Counter()

    log_pattern = re.compile(
        r'^(?P<ip>[\d\.]+)\s+'                
        r'(?:\S+)\s+'                          
        r'(?:\S+)\s+'                          
        r'\[(?P<time>[^\]]+)\]\s+'             
        r'"(?P<method>[A-Z]+)\s+'              
        r'(?P<endpoint>[^\s]+)\s+'             
        r'[^"]*"\s+'                           
        r'(?P<status>\d{3})\s+'                
        r'(?P<size>\d+|\-)'                    
    )

    open_func = gzip.open if file_path.endswith(".gz") else open
    mode = "rt" if file_path.endswith(".gz") else "r"

    with open_func(file_path , mode=mode , encoding="utf-8" , errors="ignore") as file:
        
        for line in file :

            line = line.strip()
            if not line :
                continue
            
            total_lines += 1
            match = log_pattern.match(line)
            
            if match : 
                data = match.groupdict()

                time_str = data["time"]
                hour = "00"
                if ":" in time_str:
                    hour = time_str.split(":")[1]

                if start_hour is not None and hour < start_hour:
                    continue
                if end_hour is not None and hour > end_hour:
                    continue 

                ip_counter[data["ip"]] += 1
                endpoint_counter[data["endpoint"]] += 1
                status_counter[data["status"]] += 1
                hour_counter[hour] += 1

                #TEST
                # if total_lines <= 5 :
                #     print(f"--- Line {total_lines} Parsed ---")
                #     print(f"IP: {data['ip']}")
                #     print(f"Time: {data['time']}")
                #     print(f"Method: {data['method']}")
                #     print(f"Endpoint: {data['endpoint']}")
                #     print(f"Status: {data['status']}")
                #     print(f"Size: {data['size']}")
            else :
                corrupted_lines += 1

            #TEST
            # if total_lines <= 5 :
            #     print(f"Line {total_lines} : {line}")

        execution_time = time.time() - start_time

        total_valid_requests = sum(status_counter.values())
        error_requests = sum(count for status, count in status_counter.items() if status.startswith(("4" , "5")))
        error_rate = (error_requests / total_valid_requests * 100) if total_valid_requests > 0 else 0
    
        generate_report(total_lines, corrupted_lines, ip_counter, endpoint_counter, status_counter, hour_counter, error_rate, execution_time, start_hour, end_hour, output_file)