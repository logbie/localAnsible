import re

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

def main():
    filename = 'inventory.ini'
    inventory_content = load_inventory(filename)

    # Example usage
    action = input("Do you want to update (u) an IP, add (a) a server, or exit (e)? ")
    if action.lower() == 'u':
        server_name = input("Enter the server name to update: ")
        new_ip = input("Enter the new IP address: ")
        updated_content = update_ip(inventory_content, server_name, new_ip)
    elif action.lower() == 'a':
        section = input("Enter the section to add the server to (mysql, web): ")
        server_name = input("Enter the new server name: ")
        ip = input("Enter the IP address: ")
        updated_content = add_server(inventory_content, section, server_name, ip)
    else:
        return
    
    save_inventory(filename, updated_content)
    print("Inventory updated successfully!")

if __name__ == "__main__":
    main()
