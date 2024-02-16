import os
import datetime
import subprocess as sp
import sqlite3
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))					# カレントディレクトリに移動
dbname = "agri.db"

def read_value(table, key):
	# clockテーブルの項目を一つ取得する
	sql = f"SELECT value FROM {table} WHERE [index]='{key}';"
	conn = sqlite3.connect(dbname)
	cur = conn.cursor()
	cur.execute(sql)
	result = cur.fetchone()[0] 				# fetchoneは要素数=1のタプルを返すのでその要素を取り出す
	cur.close()
	conn.close()
	return result

def write_value(table, key, value):
	# clockテーブルの項目を一つ更新する
	conn = sqlite3.connect(dbname)
	cur = conn.cursor()
	sql = f"UPDATE {table} SET value='{value}' WHERE [index]='{key}';"
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()


def main():
	dt_now = datetime.datetime.now()									# 現在時刻
	dt_restart = dt_now + datetime.timedelta(minutes=1)					# 1分後
	str_now = dt_now.strftime("%Y-%m-%d %H:%M:%S")						# 現在時刻を文字列にする
	str_restart = dt_restart.strftime("%Y-%m-%d %H:%M:%S")				# 1分後の時刻を文字列にする
	autorestart = read_value("config", "autorestart")					# 現在の再起動設定を読み込む
	if autorestart == "1":												# 再起動する設定ならば
		write_value("clock", "lastDateTime", str_restart)				# DBの日時を更新する
		write_value("config", "autorestart", "2")						# 設定のautorestartを2に変更した上で
		print(f"{str_now} リブート")
		with open("restart_log.txt", "a") as f:
			print(f"{str_now} リブート", file=f)							# ログをテキストファイルに残す
		cmd = "sudo reboot"												# リブートするlinuxコマンド
		sp.Popen(cmd.split())											# 空白で区切ってリストにし、実行する
	else:
		print(f"{str_now} リブートしない")
		with open("restart_log.txt", "a") as f:
			print(f"{str_now} リブートしない", file=f)						# ログをテキストファイルに残す

if __name__ == "__main__":
	main()
