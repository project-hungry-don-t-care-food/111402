import os
import threading
import time

# 1.開始測量
start = time.time()
threading.Thread(target=os.system("python 1restaurant.py"))
# 結束測量
end = time.time()
# 輸出結果
print("執行時間：%f 秒" % (end - start))

# 2.開始測量
start = time.time()
threading.Thread(target=os.system("python 2data.py"))
# 結束測量
end = time.time()
# 輸出結果
print("執行時間：%f 秒" % (end - start))

# 3.開始測量
start = time.time()
threading.Thread(target=os.system("python 3comment.py")) 
# 結束測量
end = time.time()
# 輸出結果
print("執行時間：%f 秒" % (end - start))

# 4.開始測量
start = time.time()
threading.Thread(target=os.system("python 4picture.py")) 
# 結束測量
end = time.time()
# 輸出結果
print("執行時間：%f 秒" % (end - start))