from datetime import datetime
import os
import time

iso = '2024-05-08T09:58:59.7033339Z'

dt = datetime.fromisoformat(iso)

# unix = int(time.mktime(dt.timetuple()))
unix = dt.timestamp()

pass
