from hexutil import Hex

hex_a = Hex(2, 2)

hex_b = Hex(2, 0)

c = hex_a.distance(hex_b)
print(c)
