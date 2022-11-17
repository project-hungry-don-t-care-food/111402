import os
import threading
threading.Thread(target=os.system("python 1restaurant.py"))
threading.Thread(target=os.system("python 2data.py"))
threading.Thread(target=os.system("python 3comment.py")) 
threading.Thread(target=os.system("python 4picture.py")) 