#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def run(cmd: str) -> str:
	res = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	return res.stdout.strip()


def get_remote_info():
	url = run('git remote get-url origin')
	parsed = urlparse(url)
	# Expect: https://x-access-token:TOKEN@github.com/owner/repo
	netloc = parsed.netloc  # e.g., x-access-token:TOKEN@github.com
	m = re.match(r"x-access-token:([^@]+)@github\.com", netloc)
	if not m:
		raise RuntimeError('Could not parse token from remote URL')
	token = m.group(1)
	path = parsed.path.strip('/')  # owner/repo(.git)?
	if path.endswith('.git'):
		path = path[:-4]
	owner, repo = path.split('/', 1)
	return token, owner, repo


def get_current_branch() -> str:
	return run('git branch --show-current')


def get_default_branch() -> str:
	# Parse from `git remote show origin`
	out = run('git remote show origin')
	for line in out.splitlines():
		if 'HEAD branch:' in line:
			return line.split(':', 1)[1].strip()
	# Fallback
	return 'main'


def create_pr(token: str, owner: str, repo: str, head: str, base: str, title: str, body: str) -> str:
	url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
	payload = {
		'title': title,
		'head': head,
		'base': base,
		'body': body,
	}
	data = json.dumps(payload).encode('utf-8')
	req = Request(url, data=data, headers={
		'Authorization': f'token {token}',
		'Accept': 'application/vnd.github+json',
		'Content-Type': 'application/json',
	})
	with urlopen(req, timeout=20) as resp:
		resp_data = json.loads(resp.read().decode('utf-8'))
	return resp_data.get('html_url') or ''


def main():
	token, owner, repo = get_remote_info()
	head = get_current_branch()
	base = get_default_branch()
	title = 'Add assessment documents and fixes (Q6=400, Q11 corrected)'
	body = (
		'Automated PR adding the Word document with 25 questions (images embedded), '\
		'generator script, and fixes: Q6 corrected to 400m; Q11 updated to the provided question.\n'\
		'Files: generated/Assessment_25_Questions_With_Images.docx, generated/assessment_25_questions.txt.'
	)
	pr_url = create_pr(token, owner, repo, head, base, title, body)
	print(pr_url)


if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print(f'ERROR: {e}', file=sys.stderr)
		sys.exit(1)