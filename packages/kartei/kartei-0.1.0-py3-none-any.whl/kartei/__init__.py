from difflib import SequenceMatcher
from .entry import KarteiEntry
from pathlib import Path
import argparse
import random
import secrets
import sys


def main():
    celebration_emojis = [
        "🎈",
        "🎉",
        "🎊",
        "🎓",
        "🥳",
        "🍾",
    ]

    parser = argparse.ArgumentParser(description="Kartei Vocabulary Trainer")
    parser.add_argument("file", type=Path, help="path to file")
    args = parser.parse_args()

    try:
        content = args.file.read_text()
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    entries = []
    for line in content.splitlines():
        if line.strip() == "":
            pass
        else:
            entries.append(KarteiEntry(line))

    random.shuffle(entries)

    for entry in entries:
        print("   " + entry.left)
        try:
            text = input(">> ").strip()
        except KeyboardInterrupt:
            print()
            sys.exit(0)
        similarity = SequenceMatcher(None, entry.right, text).ratio()
        if similarity == 1.0:
            print("\x1b[1;32m   " + entry.right, f"(similarity: {similarity:.2f} {secrets.choice(celebration_emojis)})\x1b[0m")
        elif similarity >= 0.86:
            print("\x1b[1;33m   " + entry.right, f"(similarity: {similarity:.2f})\x1b[0m")
        else:
            print("\x1b[1;31m   " + entry.right, f"(similarity: {similarity:.2f})\x1b[0m")
        print()

if __name__ == "__main__":
    main()
