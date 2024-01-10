# convert 6-byte hex address to string
xtos = lambda x: ':'.join('{0:012x}'.format(x)[i:i + 2] for i in range(0, 12, 2))