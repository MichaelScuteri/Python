import re
from collections import defaultdict
import ipaddress
import csv

# Define the log file path
log_file_path = "auth.log"

# Define unusual IP ranges in CIDR notation
unusual_ip_ranges = ['179.39.0.0/16', '52.32.226.0/24'] 
unusual_hours = range(0, 6)  # Example: 12 AM to 6 AM
unusual_hour_logins = defaultdict(int)

# Convert CIDR blocks to ipaddress.IPv4Network objects for easy checking
unusual_networks = [ipaddress.ip_network(cidr) for cidr in unusual_ip_ranges]

# Initialize counters and storage
# Use defaultdict to initialise any new keys to 0
invalid_login_ip = defaultdict(int)
invalid_login_user = defaultdict(int)
successful_login_ip = defaultdict(int)
successful_login_user = defaultdict(int)
preauth_disconnect_ip = defaultdict(int)
unusual_ips = set()


# Exmaple invalid user event: Jan 11 10:22:56 ip-172-31-1-163 sshd[2363]: Invalid user ubnt from 179.39.2.133
# Below regex will extract the match groups 'user' and 'ip'
invalid_user_pattern = re.compile(r'Invalid user (?P<user>\S+) from (?P<ip>\S+)')

# Exmaple login event: Jan 11 12:07:15 ip-172-31-1-163 sshd[2434]: Accepted publickey for ubuntu from 208.167.254.47 port 49268 ssh2: RSA 0a:78:92:3c:c8:27:13:d3:f7:ee:d5:ac:75:45:31:5c
# Below regex will extract the match groups 'user' and 'ip'
success_pk_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}) .*?Accepted publickey for (\S+) from (\S+) port', re.IGNORECASE)

# Received disconnect from 121.18.238.114: 11:  [preauth]
# Below regex will extract the match group 'ip''
preauth_pattern = re.compile(r'Received disconnect from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*\[preauth\]')


# Check if the supplied IP address is in the IP range provided by the CIDR
def is_ip_unusual(ip_address):
    ip_obj = ipaddress.ip_address(ip_address)
    for network in unusual_networks:
        if ip_obj in network:
            return True
    return False


# Open the log file and check for matches
with open(log_file_path, 'r') as log_file:
    for line in log_file:

        # Check if the line matches any of the desired regex cases
        match_invalid_user = invalid_user_pattern.search(line)
        match_pk = success_pk_pattern.search(line)
        match_preauth = preauth_pattern.search(line)

        # If there are regex matches for invalid users, process the event
        if (match_invalid_user):
            ip = match_invalid_user.group('ip')
            user = match_invalid_user.group('user')

            # store the ip in the invalid_login_ip Dictionary
            # invalid_login_ip = {'ip1':count1, 'ip2':count2, etc}
            invalid_login_ip[ip] += 1

            # store the user in the invalid_login_user Dictionary
            # invalid_login_user = {'alice':1, 'bob':2, etc}
            invalid_login_user[user] += 1
            if is_ip_unusual(ip):
                unusual_ips.add(ip)

        # If there are regex matches for preauth disconnects, process the event
        elif (match_preauth):
            ip = match_preauth.group('ip')
            # store the ip in the preauth_disconnect_ip Dictionary
            # preauth_disconnect_ip = {'ip1':count1, 'ip2':count2, etc}
            preauth_disconnect_ip[ip] += 1

            # use the is_ip_unusual(ip_address) function to check if the ip is in the unusual_ip_ranges
            if is_ip_unusual(ip):
                # if it is, add the ip to the unusual_ips Set object (see https://www.w3schools.com/python/python_sets.asp)
                unusual_ips.add(ip)

        elif (match_pk):
            ip = match_pk.group(3)
            user = match_pk.group(2)
            successful_login_ip[ip] += 1
            successful_login_user[user] += 1

            if is_ip_unusual(ip):
                unusual_ips.add(ip)
                
            time = match_pk.group(1)
            hour = int(time.split(":")[0])
            if hour in unusual_hours:
                unusual_hour_logins[user] += 1


# Print analysis results
print("SSH Log Analysis Results:")


total_invalid_user_attempts = sum(invalid_login_user.values())
print(f"Total Invalid Login Attempts: {total_invalid_user_attempts}")

# Print the ip of the highest number of attempts
most_invalid_ip = max(invalid_login_ip, key=invalid_login_ip.get)
most_invalid_ip_count = invalid_login_ip[most_invalid_ip]
print(f"Most Invalid Login Attempts (IP): {most_invalid_ip} with {most_invalid_ip_count} attempts.")

# Print the highest attempted username
most_invalid_user = max(invalid_login_user, key=invalid_login_user.get)
most_invalid_user_count = invalid_login_user[most_invalid_user]
print(f"Most Invalid Login Attempts (User): {most_invalid_user} with {most_invalid_user_count} attempts.")

# Print any unusual IPs
print(f"Unusual IPs: {list(unusual_ips)}")

# Print the names of successful logon users
print(f"Successful Logins By: {list(successful_login_user.keys())}")

# Print the number of unusual hour logons and total successful logins
unusual_hour_logins_count = sum(unusual_hour_logins.values())
print(f"Unusual Hour Logins: {unusual_hour_logins_count}")


outfile = 'invalid_logins_by_ip.csv'
with open(outfile,'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ip', 'count'])
    for ip, count in invalid_login_ip.items():
        writer.writerow([ip, count])

    print(f"Output: {outfile}")