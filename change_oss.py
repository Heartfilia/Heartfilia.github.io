import sys
import os
from prettytable import PrettyTable

from loguru import logger


def change(content: str, src: str, dst: str) -> str:
	"""改变md的oss链接 把 src --> dst"""
	if content.find(src) != -1:
		content = content.replace(src, dst)
		return content
	return ""


def get_md(path: str) -> str:
	with open(path, 'r', encoding='utf-8') as fp:
		return fp.read()


def write_md(content: str, path: str):
	with open(path, 'w', encoding='utf-8') as fp:
		fp.write(content)
	logger.success(f"路径替换成功--> {path}")


def get_files(src: str, dst: str):
	change_num = unchange_num = 0
	base_path = os.path.join('source', '_posts')
	for name in os.listdir(base_path):
		path = os.path.join(base_path, name)
		content = get_md(path)
		new_content = change(content, src, dst)
		if new_content:
			write_md(new_content, path)
			change_num += 1
		else:
			unchange_num += 1
	logger.debug(f"[总文章: {change_num + unchange_num}] 本次修改内容数: {change_num} 。不需要修改内容数: {unchange_num}")


if __name__ == "__main__":
	tb = PrettyTable(["ind", "源链接", "目标链接"])
	tb.add_row(["0", "https://static.litetools.top", "https://raw.githubusercontent.com"])
	tb.add_row(["1", "https://raw.githubusercontent.com", "https://static.litetools.top"])
	print(tb)
	print("选择序号将改变oss地址,可选参数【0/1】,任意非0/1字符退出")
	opt = input(">>> ").strip()
	if opt == "1":
		get_files("https://raw.githubusercontent.com/Heartfilia/images/main/", "https://static.litetools.top/blogs/")
	elif opt == "0":
		get_files("https://static.litetools.top/blogs/", "https://raw.githubusercontent.com/Heartfilia/images/main/")
	else:
		print("非目标输入，程序退出。")
		exit(0)
	# get_files("https://raw.githubusercontent.com/Heartfilia/images/main/", "https://cdn.jsdelivr.net/gh/Heartfilia/images/")
	