"""Pytest configuration. Ensures backend/src is on the path so 'api' and other modules are importable."""
import sys
from pathlib import Path

# Add backend/src to path when running pytest from backend/
backend_src = Path(__file__).resolve().parent.parent / "src"
if str(backend_src) not in sys.path:
    sys.path.insert(0, str(backend_src))


def pytest_configure(config):
    """Optional: set asyncio mode for pytest-asyncio."""
    config.addinivalue_line("markers", "asyncio: mark test as async (pytest-asyncio).")
