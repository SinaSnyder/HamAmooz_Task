def generate_report(total_lines, corrupted_lines, ip_counter, endpoint_counter, status_counter, hour_counter, error_rate, execution_time, start_hour, end_hour):

    top_ip, top_ip_count = ip_counter.most_common(1)[0] if ip_counter else ("None", 0)

    print("=" * 55)
    print(f"\n Total Lines Processed : {total_lines}")
    print(f"Total Corrupted Lines : {corrupted_lines}")
    print(f"Unique IPs found : {len(ip_counter)}")
    print(f"Most Active IP : {top_ip} ({top_ip_count} requests)")
    print(f"Overall Error Rate : {error_rate:.2f}% (4xx/5xx responses)\n")
    print("=" * 55)

    print(f"\nExecution time : {execution_time:.2f} seconds")
    if start_hour or end_hour:
        print(f"Active time filter : from {start_hour or '00'}:00 To {end_hour or '23'}:00")
    print("")
    print("=" * 55)

    print("\n----Top 10 Most Visited Endpoint----")
    for rank, (endpoint, count) in enumerate(endpoint_counter.most_common(10), 1):
        print(f"{rank}. {endpoint} -> {count} request")

    print("")
    print("=" * 55)

    print("\n----Status code Distribution----")
    for status, count in sorted(status_counter.items()):
        print(f"Status {status} -> {count} times")

    print("")
    print("=" * 55)

    print("\n---- Hourly Traffic Distribution & Histogram ----")
    print("Hour | Request Count | Visual Chart")
    print("-" * 55)

    max_hour_traffic = max(hour_counter.values()) if hour_counter else 1

    for h in range(24):
        hour_str = f"{h:02d}"
        count = hour_counter.get(hour_str, 0)     
        bar_length = int((count / max_hour_traffic) * 30) if max_hour_traffic > 0 else 0
        bar = "#" * bar_length
        print(f"{hour_str}:00 | {count:13d} | {bar}")

    print("")
    print("=" * 55)
    print("")