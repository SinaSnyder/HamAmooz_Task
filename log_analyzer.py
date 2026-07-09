import os
import argparse

def process_log_file(file_path):
    print("Reading...")
    total_lines = 0
    
    with open(file_path , mode="r" , encoding="utf-8" , errors="ignore") as file:
        for line in file :
            
            line = line.strip()
            
            if not line :
                continue
            
            total_lines += 1

            # if total_lines <= 5 :
            #     print(f"Line {total_lines} : {line}")

        print(f"Total Lines : {total_lines}")

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

