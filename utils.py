import psycopg2

def get_bin(filename):
    # file = open(filename, 'rb')
    # bin = file.read()
    # bin = psycopg2.Binary(file)
    # file.close()

    f = open(filename, 'rb').read()
    binary = psycopg2.Binary(f)

    return binary

def write_bin(filename, binary):
    f = open(filename, 'wb')
    f.write(binary)
    f.close()

