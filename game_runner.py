import sys
from millionaire.engine import Engine

engine = Engine('tasks.yml' if len(sys.argv) < 2 else sys.argv[1])
prize = engine.start_game()
