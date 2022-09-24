import argparse

from utils.datapack_reader import get_chains_from_datapack
from utils.commands_writer import write_converter_datapack

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts command blocks in a Minecraft world into a datapack')

    parser.add_argument('datapack_path', metavar='datapack_path', type=str,
                        help='Path of the Minecraft datapack to convert')
    parser.add_argument('x', metavar='x', type=int,
                        help='X coordinate of location where command blocks will get placed')
    parser.add_argument('y', metavar='y', type=int,
                        help='Y coordinate of location where command blocks will get placed')
    parser.add_argument('z', metavar='z', type=int,
                        help='Z coordinate of location where command blocks will get placed')

    parser.add_argument('-ox', '-offset-x', type=int, default=2,
                        help='Distance between two command block chains in the world on the X axis. 2 by default')
    parser.add_argument('-oy', '-offset-y', type=int, default=2,
                        help='Distance between two command block chains in the world on the Y axis. 2 by default')
    parser.add_argument('-r', '-commands-per-row', type=int, default=8,
                        help='Number of command blocks in the same row. 8 by default')
    parser.add_argument('-f', '-force', action='store_true',
                        help='Overwrite existing datapack named \'converter_datapack\'. False by default')
    parser.add_argument('-d', '-delete-datapack', action='store_true',
                        help='Automatically delete the converted datapack. Do NOT use this if the datapack contains stuff other than functions or you\'ll lose them. False by default')
    parser.add_argument('-s', '-segment-functions', action='store_true',
                        help='Creates a new chain after every function call. This removes race conditions problems but decreases code readability and makes chains after a function call run one tick later. See README for more info. False by default.')

    args = parser.parse_args()

    if args.ox == 0:
        print("Argument offset-x can't be 0")
        exit(0)
    if args.oy == 0:
        print("Argument offset-y can't be 0")
        exit(0)
    if args.r <= 0:
        print("Argument commands-per-row has to be strictly positive")
        exit(0)

    chains = get_chains_from_datapack(args.datapack_path)

    write_converter_datapack(args.datapack_path, chains, args.x, args.y, args.z, args.ox, args.oy, args.r, args.f,
                             args.d, args.s)
