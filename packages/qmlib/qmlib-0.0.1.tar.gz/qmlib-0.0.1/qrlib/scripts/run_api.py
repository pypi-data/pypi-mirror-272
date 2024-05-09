import argparse
import os
import uvicorn

CONFIG_LOCATION = os.environ.get("CONFIG_LOCATION")
if not CONFIG_LOCATION:
    relative_path = "../api"
    absolute_path = os.path.abspath(relative_path).replace("\\", "/") + "/" + "config.toml"
    os.environ["CONFIG_LOCATION"] = absolute_path

try:
    from qrlib.api import app
finally:
    print("FastAPI version:" + app.version)


def main() -> None:
    parser = argparse.ArgumentParser(description="api config")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Set host. Default: '127.0.0.1'.",
    )
    parser.add_argument(
        "--port",
        "-p",
        default=8000,
        help="Set port. Default: 8000.",
        type=int,
    )
    parser.add_argument(
        "--reload",
        "-r",
        type=bool,
        default=False,
        help="Set reload. Default: True.",
    )
    args = parser.parse_args()

    if not (args.host and args.port):
        raise ValueError(
            "You must set host and port either via the CLI"
            " variables."
        )

    uvicorn.run(
        app='run_api:app',
        host=args.host,
        port=args.port,
        root_path='../api',
        reload=args.reload
    )

    print("Api successful!")  # noqa: T201


if __name__ == "__main__":
    main()
