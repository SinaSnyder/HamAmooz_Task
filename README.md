# Log Analyzer CLI Tool

This is a simple CLI tool written in Python to parse and analyze large web server

## Project Structure
The project into two separate files :
1. "log_analyzer.py": The entry point of app, using "argparse"
2. "analyzer": Contains the core logic for reading, parsing and analyzing

## Features
- Memory Efficient: Process file line by line, it can handle huge log files without filling up your computer's RAM
- Gzip Support (".gz"): Automatically detects and reads compressed ".gz" log files
- Time window Filtering: Allows users to filter the log analysis between specific hours of the day
- Execution Timer: displays exactly how long the analysis took in seconds
- Comprehensive Statistics :
    - Total number of processed lines and corrupted lines
    - Overall server error rate 
    - Total number of unique IPs
    - Top 10 most visited EndPoints using an optimized Heap based structur
    - A text based hourly traffic histogram 

# How to Run

To analyze log file, pass the path of your "access.log" file as an argument:

```bash
python log_analyzer.py access.log
python log_analyzer.py access.log --start {start_hour} --end {end_hour}
```

To see available arguments and help:
```bash
python log_analyzer.py --help