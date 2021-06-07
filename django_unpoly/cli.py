"""Console script for django-unpoly."""

import fire


def help():
    print("django-unpoly")
    print("=" * len("django-unpoly"))
    print("Unpoly integration for Django")


def main():
    fire.Fire({"help": help})


if __name__ == "__main__":
    main()  # pragma: no cover
