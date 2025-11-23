from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

ROUTES_DIR = PROJECT_ROOT / "routes"
PROMO_CODES_FILE = PROJECT_ROOT / "promo_codes.txt"
PROMO_ACTIVATED_CODES_FILE = PROJECT_ROOT / "promo_codes_activated.txt"
