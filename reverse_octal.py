import sys
from bitarray import bitarray

print('HEX | DEC | REV OCT | BINARY')
print('==============================')

for i in range(256):
    starting_byte = chr(i)
    original_bits = bitarray()
    original_bits.frombytes(starting_byte)
    
    reversed_bits = bitarray()
    reversed_bits.frombytes(starting_byte)
    reversed_bits.reverse()
    
    reversed_byte = reversed_bits.tobytes()[0]
    reversed_byte = ord(reversed_byte)
    
    sys.stdout.write(' {:02X} |'.format(reversed_byte))
    sys.stdout.write(' {:03d} |'.format(reversed_byte))
    sys.stdout.write('     {:03o} |'.format(i))
    print(' {}'.format(bin(reversed_byte)[2:].zfill(8)))