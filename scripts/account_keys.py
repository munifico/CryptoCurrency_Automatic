import pyupbit
access_key = None
secret_key = None

def get_keys():
    '''
        read key text files

        return access_key, secret_key
    '''
    with open("pyupbit_key.txt") as f:
        lines = f.readlines()
        access_key = lines[0].strip()
        secret_key = lines[1].strip()

    return access_key, secret_key
