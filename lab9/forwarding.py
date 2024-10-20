import logging

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


def convert_ip_to_binary(ip):
    logging.debug(f"Converting IP to binary: {ip}")
    parts = ip.split('.')
    binary_parts = []

    for part in parts:
        if len(part) == 2 and part.isalnum():  # Assumes hex part (e.g., C0, 5E)
            try:
                binary_parts.append(format(int(part, 16), '08b'))
                logging.debug(f"Converted hex part {part} to binary: {binary_parts[-1]}")
            except ValueError:
                logging.error(f"Unsupported hexadecimal part: {part}")
                raise ValueError(f"Unsupported hexadecimal part: {part}")
        else:
            try:
                binary_parts.append(format(int(part), '08b'))
                logging.debug(f"Converted decimal part {part} to binary: {binary_parts[-1]}")
            except ValueError:
                logging.error(f"Unsupported decimal part: {part}")
                raise ValueError(f"Unsupported decimal part: {part}")

    result = ''.join(binary_parts)
    logging.debug(f"Full binary result: {result}")
    return result


def longest_prefix_match(dest_ip, routing_table):
    logging.debug(f"Finding longest prefix match for IP: {dest_ip}")
    try:
        dest_ip_bin = convert_ip_to_binary(dest_ip)
        logging.info(f"Destination IP in binary: {dest_ip_bin}")
    except ValueError as e:
        logging.error(e)
        return None

    longest_prefix_len = -1
    best_line = None

    for entry in routing_table:
        network, line = entry
        network_ip, prefix_len = network.split('/')
        prefix_len = int(prefix_len)

        logging.debug(f"Checking network: {network_ip}/{prefix_len}")

        try:
            network_ip_bin = convert_ip_to_binary(network_ip)
            logging.info(f"Network IP in binary: {network_ip_bin} with prefix length {prefix_len}")
        except ValueError as e:
            logging.error(e)
            continue

        if dest_ip_bin[:prefix_len] == network_ip_bin[:prefix_len]:
            logging.info(f"Match found for {dest_ip} with network {network}")
            if prefix_len > longest_prefix_len:
                longest_prefix_len = prefix_len
                best_line = line
                logging.debug(f"New best match: {network} with prefix length {prefix_len}")

    if best_line is None:
        logging.info(f"No valid forwarding line found for {dest_ip}")
    else:
        logging.info(f"Best match for {dest_ip}: {best_line} with prefix length {longest_prefix_len}")
    return best_line


def read_routing_table(filename):
    logging.debug(f"Reading routing table from file: {filename}")
    routing_table = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip().strip("(),")
                if line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        network = parts[0].strip().strip("'")
                        line = parts[1].strip().strip("'")
                        entry = (network, line)
                        routing_table.append(entry)
                        logging.debug(f"Added routing table entry: {entry}")
    except FileNotFoundError:
        logging.error(f"Routing table file not found: {filename}")
    except Exception as e:
        logging.error(f"Error reading routing table: {e}")

    logging.info(f"Read {len(routing_table)} entries from routing table")
    return routing_table


def read_test_cases(filename):
    logging.debug(f"Reading test cases from file: {filename}")
    test_cases = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip().strip("',")
                if line:
                    test_cases.append(line)
                    logging.debug(f"Added test case: {line}")
    except FileNotFoundError:
        logging.error(f"Test cases file not found: {filename}")
    except Exception as e:
        logging.error(f"Error reading test cases: {e}")

    logging.info(f"Read {len(test_cases)} test cases")
    return test_cases


def write_output(filename, results):
    logging.debug(f"Writing results to file: {filename}")
    try:
        with open(filename, 'w') as file:
            for ip, result in results:
                if result is not None:
                    output = f"Packet to {ip}: Forward to {result}"
                else:
                    output = f"Packet to {ip}: No valid forwarding line found."
                file.write(output + "\n")
                logging.debug(f"Wrote output: {output}")
        logging.info(f"Finished writing {len(results)} results to {filename}")
    except Exception as e:
        logging.error(f"Error writing output: {e}")


# Main execution
routing_table_file = 'routing_table.txt'
test_cases_file = 'test_cases.txt'
output_file = 'output.txt'

routing_table = read_routing_table(routing_table_file)
test_cases = read_test_cases(test_cases_file)

results = []
for ip in test_cases:
    logging.debug(f"Processing test case: {ip}")
    result = longest_prefix_match(ip, routing_table)
    results.append((ip, result))

write_output(output_file, results)

print(f"Results written to {output_file}.")