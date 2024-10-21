def convert_ip_to_binary(ip):
    parts = ip.split('.')
    binary_parts = []

    for part in parts:
        if len(part) == 2 and part.isalnum():
            try:
                binary_parts.append(format(int(part, 16), '08b'))
            except ValueError:
                raise ValueError(f"Unsupported hexadecimal part: {part}")
        else:
            try:
                binary_parts.append(format(int(part), '08b'))
            except ValueError:
                raise ValueError(f"Unsupported decimal part: {part}")

    result = ''.join(binary_parts)
    return result


def longest_prefix_match(dest_ip, routing_table):
    try:
        dest_ip_bin = convert_ip_to_binary(dest_ip)
    except ValueError as e:
        return None

    longest_prefix_len = -1
    best_line = None

    for entry in routing_table:
        network, line = entry
        network_ip, prefix_len = network.split('/')
        prefix_len = int(prefix_len)

        try:
            network_ip_bin = convert_ip_to_binary(network_ip)
        except ValueError as e:
            continue

        if dest_ip_bin[:prefix_len] == network_ip_bin[:prefix_len]:
            if prefix_len > longest_prefix_len:
                longest_prefix_len = prefix_len
                best_line = line

    return best_line


def read_routing_table(filename):
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
    except FileNotFoundError:
        pass
    except Exception as e:
        pass

    return routing_table


def read_test_cases(filename):
    test_cases = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip().strip("',")
                if line:
                    test_cases.append(line)
    except FileNotFoundError:
        pass
    except Exception as e:
        pass

    return test_cases


def write_output(filename, results):
    try:
        with open(filename, 'w') as file:
            for ip, result in results:
                if result is not None:
                    output = f"Packet to {ip}: Forward to {result}"
                else:
                    output = f"Packet to {ip}: No valid forwarding line found."
                file.write(output + "\n")
    except Exception as e:
        pass


# Main execution
routing_table_file = 'routing_table.txt'
test_cases_file = 'test_cases.txt'
output_file = 'output.txt'

routing_table = read_routing_table(routing_table_file)
test_cases = read_test_cases(test_cases_file)

results = []
for ip in test_cases:
    result = longest_prefix_match(ip, routing_table)
    results.append((ip, result))

write_output(output_file, results)

print(f"Results written to {output_file}.")