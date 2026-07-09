import os
import argparse

def main(): 

    parser = argparse.ArgumentParser()
    parser.add_argument("log_file" , type=str , help="access.log")

    args = parser.parse_args()
    file_path = args.log_file

    if not os.path.exists(file_path) :
        print(f"Error: {file_path} not found")
        return
    
    print(f"{file_path} found, Start Process...")

if __name__ == "__main__" :
    main()    

