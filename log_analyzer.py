import os
import argparse
from analyzer import process_log_file

def main(): 

    parser = argparse.ArgumentParser()
    parser.add_argument("log_file" , type=str , help="access.log")
    parser.add_argument("--start", type = str, help = "Start hour filter (e.g., 02)", default = None)
    parser.add_argument("--end", type = str, help = "End hour filter (e.g., 05)", default = None)

    args = parser.parse_args()
    file_path = args.log_file

    if not os.path.exists(file_path) :
        print(f"Error: {file_path} not found")
        return
    
    start_hour = f"{int(args.start):02d}" if args.start else None
    end_hour = f"{int(args.end):02d}" if args.end else None

    print(f"{file_path} found, Start Process...")

    process_log_file(file_path , start_hour , end_hour)

if __name__ == "__main__" :
    main()    

