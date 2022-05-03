import os
from fcntl import F_SEAL_SEAL
from  psql_helper import init_tools as it
from dotenv import load_dotenv, dotenv_values

load_dotenv()

# it.test_assert("blobb")
it.db_set_up()

for val in dotenv_values().values():
    print(val)

print(os.getenv("MULTIMODALITY_PASSWORD"))