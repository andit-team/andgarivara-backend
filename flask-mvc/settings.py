from dotenv import load_dotenv
load_dotenv()
import os
MONGO_URI = os.getenv("MONGO_URI")
JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")