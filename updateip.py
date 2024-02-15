import re
import time

def load_inventory(filename):
    with open(filename, 'r') as file:
        return file.readlines()

def save_inventory(filename, lines):
    with open(filename, 'w') as file:
        file.writelines(lines)

def parse_inventory(lines):
    servers = []
    for line in lines:
        match = re.match(r'^(\S+?)\s+ansible_host=(\S+)', line)
        if match:
            servers.append((match.group(1), match.group(2), line))
    return servers

def update_ip(servers, server_name, new_ip):
    for i, (name, ip, line) in enumerate(servers):
        if name == server_name:
            servers[i] = (name, new_ip, f"{name} ansible_host={new_ip}\n")
            return True
    return False

def add_server(lines, section, server_name, ip):
    for i, line in enumerate(lines):
        if line.startswith(f'[{section}]'):
            lines.insert(i + 1, f"{server_name} ansible_host={ip}\n")
            return True
    return False

def delete_server(servers, server_name):
    return [server for server in servers if server[0] != server_name]

def confirm_action(action_description):
    print(action_description)
    time.sleep(2)  # Delay for 2 seconds
    return input("Confirm action? (y/n): ").lower() == 'y'

def rebuild_inventory_content(servers, lines):
    new_content = []
    for line in lines:
        if not re.match(r'^\S+?\s+ansible_host=\S+', line):
            new_content.append(line)
    for name, ip, original_line in servers:
        new_content.append(f"{name} ansible_host={ip}\n")
    return new_content

def list_and_select_server(servers):
    for i, (name, ip, _) in enumerate(servers, start=1):
        print(f"{i}. {name} (IP: {ip})")
    selection = input("Select a server by number, or enter name directly: ")
    if selection.isdigit():
        index = int(selection) - 1
        if 0 <= index < len(servers):
            return servers[index][0]  # Return server name
    return selection  # Assume user entered the name directly

def main():
    filename = 'hosts.ini'
    lines = load_inventory(filename)
    servers = parse_inventory(lines)

    action = input("Do you want to update (u) an IP, add (a) a server, delete (d) a server, or exit (e)? ")
    if action.lower() == 'u':
        print("Listing servers:")
        server_name = list_and_select_server(servers)
        new_ip = input("Enter the new IP address: ")
        if confirm_action(f"About to update {server_name} IP to {new_ip}."):
            if update_ip(servers, server_name, new_ip):
                print("Server IP updated.")
            else:
                print("Server not found.")
    elif action.lower() == 'a':
        section = input("Enter the section to add the server to (mysql, web): ")
        server_name = input("Enter the new server name: ")
        ip = input("Enter the IP address: ")
        if confirm_action(f"About to add {server_name} to section {section} with IP {ip}."):
            if add_server(lines, section, server_name, ip):
                print("Server added.")
            else:
                print("Section not found.")
    elif action.lower() == 'd':
        print("Listing servers:")
        server_name = list_and_select_server(servers)
        if confirm_action(f"About to delete {server_name}."):
            updated_servers = delete_server(servers, server_name)
            if len(updated_servers) < len(servers):
                servers = updated_servers
                print("Server deleted.")
            else:
                print("Server not found.")

    new_content = rebuild_inventory_content(servers, lines)
    save_inventory(filename, new_content)
    print("Inventory updated successfully.")

if __name__ == "__main__":
    main()
