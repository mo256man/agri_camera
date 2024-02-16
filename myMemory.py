import psutil
import datetime

class Memory():
	def __init__(self):
		self.filename = "memory.csv"
		self.process = psutil.Process()
		memory_info = self.process.memory_info()
		self.last_rss = memory_info.rss									# Resident Set Siteの初期値
		self.last_vms = memory_info.vms									# Virtual Memory Sizeの初期値

	def show(self, text):
		memory_info = self.process.memory_info()
		rss = memory_info.rss
		rss_diff = rss - self.last_rss
		self.last_rss = rss
		vms = memory_info.vms
		vms_diff = rss - self.last_vms
		self.last_vms = vms
		str_date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
		msg = f"{str_date},{text},{rss},{rss_diff},{vms},{vms_diff}\n"
		with open(self.filename, "a", encoding="utf-8") as f:
			f.write(msg)

