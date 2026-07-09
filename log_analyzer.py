import os
import argparse
import re

def process_log_file(file_path):
    print("Reading...")

    total_lines = 0
    corrupted_lines = 0

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

    with open(file_path , mode="r" , encoding="utf-8" , errors="ignore") as file:
        for line in file :

            line = line.strip()
            if not line :
                continue
            
            total_lines += 1
            match = log_pattern.match(line)
            
            if match : 
                data = match.groupdict()

                #TEST
                if total_lines <= 5 :
                    print(f"--- Line {total_lines} Parsed ---")
                    print(f"IP: {data['ip']}")
                    print(f"Time: {data['time']}")
                    print(f"Method: {data['method']}")
                    print(f"Endpoint: {data['endpoint']}")
                    print(f"Status: {data['status']}")
                    print(f"Size: {data['size']}")

            else :
                corrupted_lines += 1

            #TEST
            # if total_lines <= 5 :
            #     print(f"Line {total_lines} : {line}")

        print(f"Total Lines : {total_lines}")
        print(f"Total Corrupted Lines : {corrupted_lines}")


def main(): 

    parser = argparse.ArgumentParser()
    parser.add_argument("log_file" , type=str , help="access.log")

    args = parser.parse_args()
    file_path = args.log_file

    if not os.path.exists(file_path) :
        print(f"Error: {file_path} not found")
        return
    
    print(f"{file_path} found, Start Process...")

    process_log_file(file_path)

if __name__ == "__main__" :
    main()    

