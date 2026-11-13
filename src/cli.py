import argparse
import sys

from src.request_workflow import InvalidTransition, Request, Status
from src.storage import DEFAULT_PATH, load_store, save_store


def _format(request: Request) -> str:
    approver = request.approver or "-"
    return (
        f"#{request.id} [{request.status.value}] {request.amount:,.2f} "
        f"| {request.requester} | {request.description} | approver: {approver}"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="purchase-approval")
    parser.add_argument("--file", default=DEFAULT_PATH, help="path to the data file")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="create a draft request")
    create.add_argument("--requester", required=True)
    create.add_argument("--amount", required=True, type=float)
    create.add_argument("--description", required=True)

    for name in ("submit", "approve", "reject", "show"):
        p = sub.add_parser(name)
        p.add_argument("id", type=int)

    lst = sub.add_parser("list", help="list requests")
    lst.add_argument("--status", choices=[s.value.lower() for s in Status])

    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    store = load_store(args.file)

    try:
        if args.command == "create":
            request = store.add(
                Request(
                    requester=args.requester,
                    amount=args.amount,
                    description=args.description,
                )
            )
            save_store(store, args.file)
            print(f"Created {_format(request)}")

        elif args.command in ("submit", "approve", "reject"):
            request = store.get(args.id)
            getattr(request, args.command)()
            save_store(store, args.file)
            print(f"{args.command.capitalize()}: {_format(request)}")

        elif args.command == "show":
            print(_format(store.get(args.id)))

        elif args.command == "list":
            if args.status:
                requests = store.list_by_status(Status(args.status.upper()))
                requests = sorted(requests, key=lambda r: r.id)
            else:
                requests = store.list_all()
            if not requests:
                print("No requests found.")
            for request in requests:
                print(_format(request))

    except (KeyError, ValueError, InvalidTransition) as exc:
        message = exc.args[0] if isinstance(exc, KeyError) and exc.args else exc
        print(f"Error: {message}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())