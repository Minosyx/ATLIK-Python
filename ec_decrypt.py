import argparse
import pickle
from pathlib import Path
from time import time
import multiprocessing as mp
from functools import partial
from elliptic_curve import ECP

class FileTypeWithExtensionCheck(argparse.FileType):
    def __init__(self, mode='rb', valid_extensions=None, **kwargs):
        super().__init__(mode, **kwargs)
        self.valid_extensions = valid_extensions

    def __call__(self, string):
        if self.valid_extensions:
            if not string.endswith(self.valid_extensions):
                raise argparse.ArgumentTypeError(
                    'Not a valid filename extension!')
        return super().__call__(string)


def deserialize(data):
    return pickle.loads(data)


def save(data_stream, filename):
    with open(filename, 'wb') as f:
        f.write(data_stream)


def int2list(i, N):
    return i.to_bytes(N, 'big', signed=False)


def block2bytes(l, N):
    return b''.join([bytes(int2list(i, N)) for i in l])


def decrypt(private_key, block):
    ec, m, N = private_key
    X1, X2 = block
    p = X2 - m*X1
    P = p.x // 32
    return P


def file_decrypt(file_stream, key, processes, info):
    ec, m, N = key
    add_bytes, data = file_stream

    f = partial(decrypt, key)
    t = time()
    with mp.Pool(processes) as pool:
        tmp = pool.map(f, data)

    if info:
        print(f"Deszyfrowanie {time() - t}")

    output = block2bytes(tmp, N)
    return output[:-(N - add_bytes)]


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
    parser.add_argument('private_key', type=argparse.FileType(
        'rb'), help="Plik zawierający klucz prywatny")
    parser.add_argument('file', type=FileTypeWithExtensionCheck(
        'rb', valid_extensions=('encrypted',)), help="Plik do odszyfrowania")
    parser.add_argument('-o', dest='filename', type=str,
                        help="Nowa nazwa pliku", required=False)
    parser.add_argument('-t', dest='processes', type=int_range(1, mp.cpu_count()),
                        help="Maksymalna liczba procesów", default=1, required=False)
    parser.add_argument('-i', dest='info', help="Podsumowanie czasu deszyfrowania",
                        action='store_true', required=False)
    parser.description = "Aplikacja odszyfrowująca pliki"
    parser.usage = f"{parser.prog} private_key file [-o filename] [-t processes] [-i]"
    args = parser.parse_args()

    key = deserialize(args.private_key.read())
    file_stream = deserialize(args.file.read())

    args.private_key.close()
    args.file.close()

    data = file_decrypt(file_stream, key, args.processes, args.info)

    p = Path(args.file.name)
    x = Path(p.name).stem
    filename = x if args.filename is None else args.filename + Path(x).suffix
    new_file = p.parent.joinpath(filename)

    save(data, new_file)


if __name__ == "__main__":
    main()
