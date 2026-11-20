devices = [
    {"id": 1, "status": "Active"},
    {"id": 2, "status": "Inactive"},
    {"id": 3, "status": "Active"},
    {"id": 4, "status": "Inactive"},
    {"id": 5, "status": "Active"}
]

active_count = 0
inactive_count = 0

for device in devices:
    if device ["status"] == "Active":
        active_count += 1
    else:
        inactive_count += 1

print(f"Active Devices: {active_count}")
print(f"Inactive Devices: {inactive_count}")
