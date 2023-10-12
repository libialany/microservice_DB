import os
from dotenv import load_dotenv
import multiprocessing as mp

if not load_dotenv():
  raise SystemError('No existe .env')

bind = f'0.0.0.0:{os.getenv("PORT")}'
workers = 2
timeout = 600
