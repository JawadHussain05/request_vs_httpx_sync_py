import requests
import httpx
import time

# Solana JSON-RPC endpoint URL
solana_url = "https://alien-weathered-panorama.solana-mainnet.discover.quiknode.pro/964fbbd4d182e63410b924056054299d89b1a115/"
sleep_time = 50

# Number of iterations for benchmarking
num_iterations = 10

# JSON-RPC request to get the block height
data = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getBlockHeight",
}

# Create sessions for requests and httpx
requests_session = requests.Session()
httpx_client = httpx.Client()

def request_method(session):
    print("in request method\n")
    return session.post(solana_url, json=data)

def httpx_sync_method(client, data):
    return client.post(solana_url, json=data)

# Function to measure elapsed time
def benchmark_request(method, name, session):
    total_time = 0

    for _ in range(num_iterations):
        start_time = time.time()

        if name == 'requests':
            print("in if statement\n")
            response = method(session)
        elif name == 'httpx':
            response = method(httpx_client, data)
        print("after if statement\n")
        end_time = time.time()

        block_height = response.json()["result"]

        elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
        total_time += elapsed_time

        print(f"Iteration {_ + 1}: {block_height}, Elapsed Time ({name}): {elapsed_time:.3f} ms")
        time.sleep(sleep_time / 1000.0)

    avg_time = total_time / num_iterations
    print(f"Average Elapsed Time (using {name}): {avg_time:.3f} ms")
    return avg_time

# Benchmarking for 'requests'
print("Benchmarking 'requests'...")
req_avg = benchmark_request(request_method, 'requests', requests_session)

# Benchmarking for 'httpx'
print("\nBenchmarking 'httpx'...")
httpx_avg = benchmark_request(httpx_sync_method, 'httpx', httpx_client)

print("\n\n****************************************************")
print(f"Average Elapsed Time (using request): {req_avg:.3f} ms")
print(f"Average Elapsed Time (using httpx): {httpx_avg:.3f} ms")
print("\n****************************************************\n\n")