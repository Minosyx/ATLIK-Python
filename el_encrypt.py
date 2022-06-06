import argparse
import pickle
from secrets import token_bytes, randbelow
from pathlib import Path
from time import time
import multiprocessing as mp
from functools import partial

def deserialize(key_stream):
    return pickle.loads(key_stream)


def serialize(data, filename):
    with open(filename, "wb") as f:
        pickle.dump(data, f)


def list2int(t):
    return int.from_bytes(t, 'big', signed=False)


def bytes2block(s, N):
    return [list2int(s[N*i:N*(i+1)]) for i in range(len(s)//N)]


def encrypt(public_key, block):
    B, C, n, _ = public_key
    return (pow(B, r := (randbelow(n - 3) + 2), n), block * pow(C, r, n) % n)


def file_encrypt(file_stream, key, processes, info):
    B, C, n, N = key

    if add_bytes := len(file_stream) % N:
        file_stream += token_bytes(N - add_bytes)

    res = bytes2block(file_stream, N)
    f = partial(encrypt, key)

    t = time()
    with mp.Pool(processes) as pool:
        output = pool.map(f, res)

    if info:
        print(f"Szyfrowanie {time() - t}")

    return (add_bytes, output)


def int_range(mini, maxi):
    def int_range_checker(arg):
        try:
            num = int(arg)
        except ValueError:
            raise argparse.ArgumentTypeError("Must be an integer")
        if num < mini or num > maxi:
            raise argparse.ArgumentTypeError(
                "Must be in range [" + str(mini) + " .. " + str(maxi)+"]")
        return num
    return int_range_checker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('public_key', type=argparse.FileType(
        'rb'), help="Plik zawierający klucz publiczny")
    parser.add_argument('file', type=argparse.FileType(
        'rb'), help="Plik do zaszyfrowania")
    parser.add_argument('-o', dest='filename', type=str,
                        help="Nowa nazwa pliku", required=False)
    parser.add_argument('-t', dest='processes', type=int_range(1, mp.cpu_count()),
                        help="Maksymalna liczba procesów", default=1, required=False)
    parser.add_argument('-i', dest='info', help="Podsumowanie czasu szyfrowania",
                        action='store_true', required=False)
    parser.description = "Aplikacja szyfrująca pliki"
    parser.usage = f"{parser.prog} public_key file [-o filename] [-t processes] [-i]"
    args = parser.parse_args()

    key = deserialize(args.public_key.read())
    file_stream = args.file.read()

    args.public_key.close()
    args.file.close()

    data = file_encrypt(file_stream, key, args.processes, args.info)
    p = Path(args.file.name)
    filename = p.name if args.filename is None else args.filename + p.suffix
    new_file = p.parent.joinpath(filename + '.encrypted')

    serialize(data, new_file)


if __name__ == "__main__":
    main()
