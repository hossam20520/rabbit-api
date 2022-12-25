import sys


def main():
    version = sys.version_info
    if (version < (3, 10)):
        print('[-] coofast only works with Python 3.10+.')
        print(f'Your current Python version : {version.major}.{version.minor}.{version.micro}')
        sys.exit(1)

    from coofast.cli import parse_and_run
    from coofast.helpers.banner import show_banner

    show_banner()
    parse_and_run()
    # parse_and_run()