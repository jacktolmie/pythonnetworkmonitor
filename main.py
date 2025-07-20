from modules import get_host_info

server = "192.168.1.200"
hostname = "Test1"
server1 = "192.168.1.203"
hostname1 = "Test2"
server2 = "bork-and-borr"
hostname2 = "Bork-and-borr"
server3 = "asdf"
hostname3 = "asdf"

get_host_info.get_host_info(hostname, server, True, 2)
get_host_info.get_host_info(hostname1, server1, True, 2)
get_host_info.get_host_info(hostname2, server2, True, 2)
get_host_info.get_host_info(hostname3, server3, True, 2)
get_host_info.get_host_info("bad", "192.168.1.22", False, 2)

get_host_info.get_host_info("Alienware", "192.168.1.199", True, 2)
#
# # --- API Configuration ---
# API_URL = "http://127.0.0.1:8000/monitor/api/delete_target/" # Adjust if your URL is different
#
# # --- Helper Function to Send Delete Request ---
# def send_delete_request(payload, test_name):
#     """Sends a POST request to the delete API and prints the response."""
#     print(f"\n--- Testing Scenario: {test_name} ---")
#     print(f"Sending payload: {json.dumps(payload)}")
#
#     try:
#         response = requests.post(API_URL, json=payload)
#         print(f"Status Code: {response.status_code}")
#         try:
#             response_data = response.json()
#             print(f"Response Body: {json.dumps(response_data, indent=2)}")
#         except json.JSONDecodeError:
#             print(f"Response Body (not JSON): {response.text}")
#     except requests.exceptions.ConnectionError:
#         print("ERROR: Could not connect to Django server. Is it running?")
#     except Exception as e:
#         print(f"An unexpected error occurred during request: {e}")
#
#
# # --- Main Test Execution ---
# if __name__ == "__main__":
#     print("Starting API Delete Test Script...")
#
#     # --- Test Case 1: Successful Deletion ---
#     # Create a host to be deleted
#     print("\nSetting up for successful deletion test...")
#     try:
#         test_host_name = "TestHostForDeletion"
#         test_host_ip = "192.168.1.200"
#         host_to_delete, created = Host.objects.get_or_create(
#             name=test_host_name,
#             ip_address=test_host_ip,
#             defaults={'description': 'Temporary host for testing delete'}
#         )
#         if created:
#             print(f"Created test host: {host_to_delete.name} (ID: {host_to_delete.name})")
#         else:
#             print(f"Test host already exists: {host_to_delete.name} (ID: {host_to_delete.name})")
#
#         # Add a ping result to ensure cascade delete works
#         Host.objects.get_or_create(host=host_to_delete, is_up=True)
#         print(f"Added a ping result for host ID {host_to_delete.name}.")
#
#         initial_host_count = Host.objects.count()
#         initial_ping_count = PingHost.objects.count()
#         print(f"Initial DB state: Hosts={initial_host_count}, PingResults={initial_ping_count}")
#
#         send_delete_request({"id": host_to_delete.name}, "Successful Deletion")
#
#         # Verify deletion in DB
#         final_host_count = Host.objects.count()
#         final_ping_count = PingHost.objects.count()
#         print(f"Final DB state: Hosts={final_host_count}, PingResults={final_ping_count}")
#         if not Host.objects.filter(id=host_to_delete.name).exists():
#             print(f"Verification: Host ID {host_to_delete.name} successfully removed from DB.")
#         else:
#             print(f"Verification: Host ID {host_to_delete.name} still exists in DB (unexpected).")
#
#     except Exception as e:
#         print(f"Error during successful deletion test setup/execution: {e}")
#
#     # --- Test Case 2: Host Not Found (404) ---
#     non_existent_id = 999999999  # A very high ID unlikely to exist
#     send_delete_request({"id": non_existent_id}, "Host Not Found (404)")
#
#     # --- Test Case 3: Invalid JSON (400) ---
#     # This payload is intentionally malformed JSON
#     print("\n--- Testing Scenario: Invalid JSON (400) ---")
#     print("Sending malformed JSON payload: {'id': 123, 'extra_comma':,}")  # Example of malformed JSON
#     try:
#         # requests.post(..., data=...) sends raw string, good for malformed JSON
#         response = requests.post(API_URL, data='{"id": 123, "extra_comma":,}')
#         print(f"Status Code: {response.status_code}")
#         try:
#             response_data = response.json()
#             print(f"Response Body: {json.dumps(response_data, indent=2)}")
#         except json.JSONDecodeError:
#             print(f"Response Body (not JSON): {response.text}")  # Should still be JSON but with parser error
#     except requests.exceptions.ConnectionError:
#         print("ERROR: Could not connect to Django server. Is it running?")
#     except Exception as e:
#         print(f"An unexpected error occurred during invalid JSON request: {e}")
#
#     # --- Test Case 4: Missing Host ID (400) ---
#     send_delete_request({"some_other_key": "value"}, "Missing Host ID (400)")
#
#     # --- Test Case 5: Simulated Internal Server Error (500) ---
#     print("\n--- Testing Scenario: Simulated Internal Server Error (500) ---")
#     print("To test this, you MUST temporarily add 'raise ValueError(\"Simulated error!\")'")
#     print("inside your delete_monitor_target_api view, just before the final 'except Exception as e:' block.")
#     print("Then run this script again. Remember to remove it afterwards!")
#     # To run this, you'd need to manually modify your Django view:
#     # 1. Open network_monitor/views.py
#     # 2. Inside delete_monitor_target_api, find the line after host_to_delete.delete()
#     # 3. Add: raise ValueError("Simulated database error!")
#     # 4. Save views.py (Django dev server should auto-reload)
#     # 5. Run this test script.
#     # 6. REMOVE the 'raise ValueError' line from views.py after testing!
#
#     # Create another host for this test
#     try:
#         error_test_host_name = "ErrorTestHost"
#         error_test_host_ip = "192.168.1.201"
#         error_host, created = Host.objects.get_or_create(
#             name=error_test_host_name,
#             ip_address=error_test_host_ip,
#             defaults={'description': 'Host for error simulation'}
#         )
#         if created:
#             print(f"Created test host for error simulation: {error_host.name} (ID: {error_host.name})")
#         else:
#             print(f"Test host for error simulation already exists: {error_host.name} (ID: {error_host.name})")
#
#         send_delete_request({"id": error_host.name}, "Simulated 500 Error")
#
#     except Exception as e:
#         print(f"Error during simulated 500 error test setup/execution: {e}")
#
#     print("\nTest script finished.")
#     print("Remember to remove any temporary 'raise ValueError' lines from your Django view!")
#
# # ip6 = "2001:0db8:0001:0000:0000:0ab9:C0A8:0102"
# # get_host_info.get_host_info(ip6, True, 2)