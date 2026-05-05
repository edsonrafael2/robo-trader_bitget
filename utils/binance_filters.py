import math

def get_lot_size_filters(client, symbol):
    info = client.get_symbol_info(symbol)

    lot_size = next(f for f in info['filters'] if f['filterType'] == 'LOT_SIZE')

    step_size = float(lot_size['stepSize'])
    min_qty = float(lot_size['minQty'])

    return step_size, min_qty


def adjust_quantity(quantity, step_size):
    return math.floor(quantity / step_size) * step_size


def validate_quantity(quantity, min_qty):
    return quantity >= min_qty