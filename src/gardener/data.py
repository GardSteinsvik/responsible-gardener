
def encode_time(time_tuple):
    time_string = '-'.join(str(x) for x in time_tuple)
    return time_string


def parse_time(time_string):
    time_tuple = tuple(int(x) for x in time_string.split('-'))
    return time_tuple


def get_last_watered():
    try:
        f = open('last_watered.txt', 'r')
        time_string = f.read()
        time_tuple = parse_time(time_string)
        print('Last watered:', time_tuple)
        return time_tuple
    except Exception as identifier:
        print(identifier)
        return (1970, 1, 1, 0, 0, 0, 1, 1)


def set_last_watered(last_watered):
    try:
        f = open('last_watered.txt', 'w')
        time_string = encode_time(last_watered)
        f.write(time_string)
        f.close()
    except Exception as identifier:
        print(identifier)


def get_water_amount():
    try:
        f = open('water_amount.txt', 'r')
        water_amount = int(f.read())
        if water_amount > 15: # Capping to max 15 secs
            water_amount = 15
        return water_amount
    except Exception as identifier:
        print(identifier)
        return 5


def set_water_amount(water_amount):
    try:
        f = open('water_amount.txt', 'w')
        f.write(str(water_amount))
        f.close()
    except Exception as identifier:
        print(identifier)


def get_pump_state():
    try:
        f = open('pump_state.txt', 'r')
        return f.read()
    except Exception as identifier:
        print(identifier)

def set_pump_state(state):
    try:
        f = open('pump_state.txt', 'w')
        f.write(state)
        f.close()
    except Exception as identifier:
        print(identifier)
