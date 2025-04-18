import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
import asyncio

from server import serve


def main() -> None:
    asyncio.run(serve())


main()
