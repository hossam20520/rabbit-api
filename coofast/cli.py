import argparse
from typing import *
import sys
from coofast import globals as gb
from coofast.projectMaker import ProjectMaker
import os 
def parse_and_run():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="module")

    # ### Login module
    # parser_login = subparsers.add_parser('login', help="Authenticate")
    # parser_login.add_argument('--clean', action='store_true', help="Clear credentials local file.")

    ### Email module
    parser_email = subparsers.add_parser('module', help="Create simple crud")
    parser_email.add_argument("moduls")
    parser_email.add_argument('--create', type=str, help="module Name")
    # parser_email.add_argument('--type', type=str, help="Simple or auth")

 

    ### Parsing
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    process_args(args)

def process_args(args: argparse.Namespace):
    import trio
    match args.module:
        case "login":
            pass
            # from ghunt.modules import login
            # trio.run(login.check_and_login, None, args.clean)
        case "module":
            router  = ProjectMaker("modules")
            router.makeSimpleProject([ args.moduls])
            router.create_project()
            gb.rc.print(f"\n[+] Module has been Created !",  style="green4")
            gb.rc.print(f"\n[+] Please copy /build/{ args.moduls}s to your project !",  style="slate_blue3")
            # exit("[-] Creds aren't loaded. Are you logged in ?")
            # from ghunt.modules import email
            # trio.run(email.hunt, None, args.email_address, args.json)
        case "gaia":
            pass
            # from ghunt.modules import gaia
            # trio.run(gaia.hunt, None, args.gaia_id, args.json)
        case "drive":
            pass
            # from ghunt.modules import drive
            # trio.run(drive.hunt, None, args.file_id, args.json)