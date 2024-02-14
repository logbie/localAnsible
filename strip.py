# Python script to strip out lines starting with ";" and remove blank lines from a config file

def strip_comments_and_blank_lines(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:
            # Check if the line starts with a semicolon or is a blank line
            if not line.lstrip().startswith(';') and not line.strip() == '':
                output_file.write(line)

if __name__ == "__main__":
    input_file_path = 'www.conf'  # Path to the input file
    output_file_path = 'www.conf.j2'  # Path to the output file
    strip_comments_and_blank_lines(input_file_path, output_file_path)