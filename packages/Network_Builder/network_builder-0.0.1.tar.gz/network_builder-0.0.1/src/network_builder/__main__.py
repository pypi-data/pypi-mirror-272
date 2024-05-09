import argparse
from .network_builder import main

if __name__ == '__main__':
    argparse = argparse.ArgumentParser()
    argparse.add_argument('--devices_file', help='Path to device file', required=True)
    argparse.add_argument('--tasks_file', help='Path to tasks file', required=True)
    args = argparse.parse_args()

    main(args.tasks_file, args.devices_file)
