import os

for i in range(40,51):
	try:
		os.system("python closed.py "+str(i))
	except Exception as err:
		print(str(i)+":"+str(err))