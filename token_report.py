
import argparse
from pathlib import Path
import unicodedata
import tiktoken


def canonical(text: str) -> str:
    """Normalize text using Unicode NFC."""
    return unicodedata.normalize("NFC", text)


def get_stats(text: str, tokenizer) -> dict:
    byte_count = len(text.encode("utf-8"))
    token_count = len(tokenizer.encode(text))

    return {
        "chars": len(text),
        "bytes": byte_count,
        "tokens": token_count,
        "bytes_per_token": (
            byte_count / token_count if token_count else 0
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Report text statistics and estimated input cost."
    )

    parser.add_argument(
        "file",
        type=Path,
        help="Path to the input text file",
    )

    parser.add_argument(
        "-e",
        "--encoding",
        default="utf-8",
        help="File encoding (default: utf-8)",
    )

    parser.add_argument(
        "--price",
        type=float,
        default=1.00,
        help="Input price per 1 million tokens in USD",
    )

    args = parser.parse_args()

    # Read file
    content = args.file.read_text(encoding=args.encoding)

    # Tokenizer
    tokenizer = tiktoken.get_encoding("cl100k_base")

    # Before canonicalization
    before = get_stats(content, tokenizer)

    # Apply canonicalization
    normalized = canonical(content)

    # After canonicalization
    after = get_stats(normalized, tokenizer)

    # Estimated input cost
    before_cost = (
        before["tokens"] * args.price / 1_000_000
    )

    after_cost = (
        after["tokens"] * args.price / 1_000_000
    )

    # Display results
    print(f"\nFile: {args.file}")
    print(f"Tokenizer: cl100k_base")
    print(f"Input price: ${args.price:.2f} per 1M tokens")

    print("\n" + "=" * 55)
    print(f"{'Metric':<22}{'Before':>15}{'After':>15}")
    print("=" * 55)

    print(
        f"{'Characters':<22}"
        f"{before['chars']:>15}"
        f"{after['chars']:>15}"
    )

    print(
        f"{'Bytes':<22}"
        f"{before['bytes']:>15}"
        f"{after['bytes']:>15}"
    )

    print(
        f"{'Tokens':<22}"
        f"{before['tokens']:>15}"
        f"{after['tokens']:>15}"
    )

    print(
        f"{'Bytes/Tokens':<22}"
        f"{before['bytes_per_token']:>15.4f}"
        f"{after['bytes_per_token']:>15.4f}"
    )

    print("=" * 55)

    print("\nEstimated Input Cost:")
    print(f"Before canonical(): ${before_cost:.8f}")
    print(f"After canonical():  ${after_cost:.8f}")

    print(
        f"Cost difference:    "
        f"${before_cost - after_cost:.8f}"
    )


if __name__ == "__main__":
    main()
