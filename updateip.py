import re
import time

def load_inventory(filename):
    with open(filename, 'r') as file:
        return file.read()

def save_inventory(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def update_ip(content, server_name, new_ip):
    pattern = re.compile(r'(' + re.escape(server_name) + r' ansible_host=)(\S+)')
    return re.sub(pattern, r'\g<1>' + new_ip, content)

def add_server(content, section, server_name, ip):
    pattern = re.compile(r'(\[' + re.escape(section) + r'\]\n)')
    return re.sub(pattern, r'\g<1>' + server_name + ' ansible_host=' + ip + '\n', content, count=1)

def delete_server(content, server_name):
    pattern = re.compile(r'^' + re.escape(server_name) + r'\s+ansible_host=\S+\s*$', re.MULTILINE)
    new_content = re.sub(pattern, '', content)
    # Check if content changed to confirm deletion
    if new_content == content:
        return None  # No change indicates server not found
    return new_content

def list_servers(content, start=0, step=10):
    server_pattern = re.compile(r'^(\S+?)\s+ansible_host=(\S+)', re.MULTILINE)
    servers = server_pattern.findall(content)
    for i, (name, ip) in enumerate(servers[start:start+step], start=1):
        print(f"{start + i}. {name} (IP: {ip})")
    return servers, start + step

def confirm_action(action_description):
    print(action_description)
    time.sleep(2)  # Delay for 2 seconds
    return input("Confirm action? (y/n): ").lower() == 'y'

def main():
    filename = 'hosts.ini'
    inventory_content = load_inventory(filename)

    action = input("Do you want to update (u) an IP, add (a) a server, delete (d) a server, or exit (e)? ")
    if action.lower() == 'u':
        servers, next_start = list_servers(inventory_content)
        while True:
            user_choice = input("Choose a server to update (name or number), list more (l), or enter (m) to manually input a name: ")
            if user_choice.isdigit():
                server_number = int(user_choice) - 1
                if server_number < len(servers):
                    server_name, _ = servers[server_number]
                    new_ip = input("Enter the new IP address: ")
                    if confirm_action(f"About to update {server_name} IP to {new_ip}."):
                        inventory_content = update_ip(inventory_content, server_name, new_ip)
                        print("Server IP updated.")
                    break
                else:
                    print("Invalid server number.")
            elif user_choice.lower() == 'l':
                _, next_start = list_servers(inventory_content, next_start)
            elif user_choice.lower() == 'm':
                server_name = input("Enter the server name to update: ")
                new_ip = input("Enter the new IP address: ")
                if confirm_action(f"About to update {server_name} IP to {new_ip}."):
                    inventory_content = update_ip(inventory_content, server_name, new_ip)
                    print("Server IP updated.")
                break
            else:
                new_ip = input("Enter the new IP address: ")
                if confirm_action(f"About to update {user_choice} IP to {new_ip}."):
                    inventory_content = update_ip(inventory_content, user_choice, new_ip)
                    print("Server IP updated.")
                break
    elif action.lower() == 'a':
        section = input("Enter the section to add the server to (mysql, web): ")
        server_name = input("Enter the new server name: ")
        ip = input("Enter the IP address: ")
        if confirm_action(f"About to add {server_name} to section {section} with IP {ip}."):
            inventory_content = add_server(inventory_content, section, server_name, ip)
            print("Server added.")
    elif action.lower() == 'd':
        servers, _ = list_servers(inventory_content)
        server_name = input("Enter the server name to delete: ")
        if confirm_action(f"About to delete {server_name}."):
            updated_content = delete_server(inventory_content, server_name)
            if updated_content is not None:
                inventory_content = updated_content
                print("Server deleted.")
            else:
                print("Server not found.")

    save_inventory(filename, inventory_content)
    print("Inventory updated successfully!")

if __name__ == "__main__":
    main()
