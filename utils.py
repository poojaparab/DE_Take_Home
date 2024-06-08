import hashlib

def mask_value(value):
    return hashlib.sha256(value.encode()).hexdigest()

def mask_data(record):
    record['masked_ip'] = mask_value(record['ip'])
    record['masked_device_id'] = mask_value(record['device_id'])
    del record['ip']
    del record['device_id']
    return record

def convert_app_version(app_version):
    try:
        # Split the version string into its parts
        parts = app_version.split('.')
        # Ensure there are three parts
        parts = [int(part) for part in parts] + [0] * (3 - len(parts))
        # Convert to integer representation
        return parts[0] * 10000 + parts[1] * 100 + parts[2]
    except ValueError:
        return None