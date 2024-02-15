import re
import time

def load_inventory(filename):
    with open(filename, 'r') as file:
        return file.readlines()

def save_inventory(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def parse_inventory(lines):
    sections = {}
    current_section = None
    section_order = []
    for line in lines:
        line = line.strip()
        section_match = re.match(r'^\[(.+)\]$', line)
        if section_match:
            current_section = section_match.group(1)
            sections[current_section] = []
            section_order.append(current_section)
        elif current_section and line:
            sections[current_section].append(line)
    return sections, section_order

def update_ip(sections, section_name, server_name, new_ip):
    for i, line in enumerate(sections[section_name]):
        if line.startswith(server_name + " ansible_host="):
            sections[section_name][i] = f"{server_name} ansible_host={new_ip}"
            return True
    return False

def add_server(sections, section_order, section_name, server_name, ip):
    if section_name not in sections:
        sections[section_name] = []
        section_order.append(section_name)
    sections[section_name].append(f"{server_name} ansible_host={ip}")

def delete_server(sections, server_name):
    for section in sections.values():
        for i, line in enumerate(section):
            if line.startswith(server_name + " ansible_host="):
                section.pop(i)
                return True
    return False

def confirm_action(action_description):
    print(action_description)
    time.sleep(2)
    return input("Confirm action? (y/n): ").lower() == 'y'

def rebuild_inventory_content(sections, section_order):
    content = ""
    for section in section_order:
        content += f"[{section}]\n"
        for line in sections[section]:
            content += line + "\n"
        content += "\n"  # Add a newline for spacing between sections
    return content

def list_and_select_server(sections):
    server_list = []
    for section, lines in sections.items():
        for line in lines:
            match = re.match(r'^(\S+?)\s+ansible_host=(\S+)', line)
            if match:
                server_name = match.group(1)
                server_list.append(server_name)
                print(f"{len(server_list)}. {server_name} (Section: {section})")
    selection = input("Select a server by number, or enter name directly: ")
    if selection.isdigit():
        index = int(selection) - 1
        if 0 <= index < len(server_list):
            return server_list[index]
    return selection

def main():
    filename = 'hosts.ini'
    lines = load_inventory(filename)
    sections, section_order = parse_inventory(lines)

    action = input("Do you want to update (u) an IP, add (a) a server, delete (d) a server, or exit (e)? ")
    if action.lower() in ['u', 'd']:
        print("Listing servers:")
        server_name = list_and_select_server(sections)
        if action.lower() == 'u':
            new_ip = input("Enter the new IP address: ")
            section_name = input("Enter the section name: ")
            if confirm_action(f"About to update {server_name} IP to {new_ip} in {section_name}."):
                if update_ip(sections, section_name, server_name, new_ip):
                    print("Server IP updated.")
                else:
                    print("Server not found.")
        elif action.lower() == 'd':
            if confirm_action(f"About to delete {server_name}."):
                if delete_server(sections, server_name):
                    print("Server deleted.")
                else:
                    print("Server not found.")
    elif action.lower() == 'a':
        section_name = input("Enter the section name: ")
        server_name = input("Enter the new server name: ")
        ip = input("Enter the IP address: ")
        if confirm_action(f"About to add {server_name} to section {section_name} with IP {ip}."):
            add_server(sections, section_order, section_name, server_name, ip)
            print("Server added.")

    content = rebuild_inventory_content(sections, section_order)
    save_inventory(filename, content)
    print("Inventory updated successfully.")

if __name__ == "__main__":
    main()