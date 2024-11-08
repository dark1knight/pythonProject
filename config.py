
import os

# Default MongoDB URI with a fallback to localhost if the environment variable is not set
MONGODB_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "call_records")