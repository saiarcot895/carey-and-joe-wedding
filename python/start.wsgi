import sys
import os
sys.stdout = sys.stderr
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weddingWebsite import app as application
