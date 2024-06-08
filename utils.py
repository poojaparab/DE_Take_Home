import hashlib

def mask_value(value):
    return hashlib.sha256(value.encode()).hexdigest()

def mask_data(record):
    try:
        record['masked_ip'] = mask_value(record['ip'])
        record['masked_device_id'] = mask_value(record['device_id'])
        del record['ip']
        del record['device_id']
    except KeyError as e:
        print(f"KeyError: The key {e} does not exist in the record.")
        record['masked_ip'] = None
        record['masked_device_id'] = None
    return record

def convert_app_version(app_version):
    try:
        parts = app_version.split('.')
        parts = [int(part) for part in parts] + [0] * (3 - len(parts))
        return parts[0] * 10000 + parts[1] * 100 + parts[2]
    except ValueError:
        return None