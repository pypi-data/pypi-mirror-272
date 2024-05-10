# -*- coding: utf-8 -*-
from package.airtest.cli.parser import get_parser


def main(argv=None):
    ap = get_parser()
    args = ap.parse_args(argv)
    if args.action == "info":
        from package.airtest.cli.info import get_script_info
        print(get_script_info(args.script))
    elif args.action == "report":
        from package.airtest.report.report import main as report_main
        report_main(args)
    elif args.action == "run":
        from package.airtest.cli.runner import run_script
        run_script(args)
    elif args.action == "version":
        from package.airtest.utils.version import show_version
        show_version()
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
