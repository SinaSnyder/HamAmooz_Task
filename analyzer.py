import re
import gzip
import time
from collections import Counter


def process_log_file(file_path , start_hour = None, end_hour = None):
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

    with open_func(file_path , mode="r" , encoding="utf-8" , errors="ignore") as file:
        
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

                if start_hour is not None and hour < start_hour :
                    continue
                if end_hour is not None and hour > end_hour :
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

            execution_time = time.time() - start_time

            #TEST
            # if total_lines <= 5 :
            #     print(f"Line {total_lines} : {line}")

        print("=" * 40)
        print(f"\n Total Lines : {total_lines}")
        print(f"Total Corrupted Lines : {corrupted_lines}")
        print(f"Unique IPs found : {len(ip_counter)}")

        total_valid_requests = sum(status_counter.values())
        error_requests = sum(count for status, count in status_counter.items() if status.startswith(("4" , "5")))
        error_rate = (error_requests / total_valid_requests * 100) if total_valid_requests > 0 else 0
        print(f"Overall Error Rate : {error_rate:.2f}% (4xx/5xx responses) \n")
        print("=" * 40)

        print(f"\nExecution time : {execution_time:.2f} seconds")
        if start_hour or end_hour :
            print(f"Active time filter : from {start_hour or "00"}:00 To {end_hour or "23"}:00")
        print("")
        print("=" * 40)


        print("\n----Top 10 Most Visited Endpoint----")
        for rank, (endpoint, count) in enumerate(endpoint_counter.most_common(10), 1) :
            print(f"{rank}. {endpoint} -> {count} request")

        print("")
        print("=" * 40)

        print("\n----Status code Distribution----")
        for status, count in  sorted(status_counter.items()) :
            print(f"Status {status} -> {count} times")

        print("")
        print("=" * 40)

        print("\n---- Hourly Traffic Distribution & Histogram ----")
        print("Hour | Request Count | Visual Chart")
        print("-" * 55)

        max_hour_traffic = max(hour_counter.values()) if hour_counter else 1

        for h in range(24) :
            hour_str = f"{h:02d}"
            count = hour_counter.get(hour_str, 0)     
            bar_length = int((count / max_hour_traffic) * 30) if max_hour_traffic > 0 else 0
            bar = "#" * bar_length
            print(f"{hour_str}:00 | {count:13d} | {bar}")

        print("")
        print("=" * 40)
        print("")