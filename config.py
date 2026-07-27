import os
from dotenv import load_dotenv

load_dotenv()

print("BOT_TOKEN =", os.getenv("BOT_TOKEN"))
print("ADMIN_ID =", os.getenv("ADMIN_ID"))

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
