import os
import sys
import re
from dotenv import load_dotenv
from app.logging import log

load_dotenv()

MONGO_CONNECTION_STRING: str = os.getenv("MONGO_CONNECTION_STRING", "")
MONGO_DATABASE: str = os.getenv("MONGO_DATABASE", "")

_environment_variables = locals().copy()

missing_env = False
for environment_variable, value in _environment_variables.items():
    if re.fullmatch(r"[A-Z_]+", environment_variable):
        if value == "":
            log.critical(f"[Environment] {environment_variable} is not configured")
            missing_env = True

if missing_env is True:
    log.critical("[Environment] Missing environment variable(s)")
    sys.exit(1)
