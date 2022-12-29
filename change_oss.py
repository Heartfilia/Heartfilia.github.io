import re
import os

from loguru import logger


def change(content: str, src: str, dst: str) -> str:
	"""改变md的oss链接 把 src --> dst"""
	content = content.replace(src, dst)
	return content


def get_md(path: str) -> str:
	with open(path, 'r', encoding='utf-8') as fp:
		return fp.read()


def write_md(content: str, path: str):
	with open(path, 'w', encoding='utf-8') as fp:
		fp.write(content)
	logger.success(f"路径替换成功--> {path}")


def get_files(src: str, dst: str):
	for name in os.listdir("_posts"):
		path = os.path.join("source", "_posts", name)
		content = get_md(path)
		new_content = change(content, src, dst)
		write_md(new_content, path)


if __name__ == "__main__":
	get_files("https://raw.githubusercontent.com/Heartfilia/images/main/", "https://static.litetools.top/blogs/")
	# get_files("https://static.litetools.top/blogs/", "https://raw.githubusercontent.com/Heartfilia/images/main/")
