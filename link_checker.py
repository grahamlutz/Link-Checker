import requests
from bs4 import BeautifulSoup
import validators
import html_linter

class LinkChecker:
	'''Class that checks sites for bad links'''
	def __init__(self, url, headers):
		self.url = url
		self.headers = headers

	def get_response(self):
		response = requests.get(self.url, headers=self.headers)
		if not 200 <= response.status_code < 300:
			raise Exception("Error while getting url, code: " + str(response.status_code))
		return response

	def get_link_text(self):
		response = self.get_response()
		plain_text = response.text
		return plain_text

	def get_source_code(self):
		plain_text = self.get_link_text()
		source_code = BeautifulSoup(plain_text, "html.parser")
		return source_code

	def lint_html(self):
		source_code = self.get_source_code()
		plain_text = self.get_link_text()
		messages = html_linter.lint(plain_text, [html_linter.QuotationMessage, html_linter.IndentationMessage])
		print(messages)


	def loop_source_code_tag(self, tag, attr):
		source_code = self.get_source_code()
		for tag in source_code.findAll(tag):
			tag_url = tag.get(attr)
			if validators.url(str(tag_url)):
				response = requests.get(tag_url, headers=headers)
				if not 200 <= response.status_code < 300:
					print(tag_url + ' returned a ' + response.status_code)
				else:
					print(tag_url + ' works just fine!')

	def check_a_tags(self):
		self.loop_source_code_tag(tag='a', attr='href')

	def check_img_src(self):
		self.loop_source_code_tag(tag='img', attr='src')

	def check_link_tags(self):
		self.loop_source_code_tag(tag='link', attr='href')

	def check_all(self):
		self.check_img_src()
		self.check_a_tags()
		self.check_link_tags()

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
grahamlutz = LinkChecker('http://www.grahamlutz.com', headers)
grahamlutz.lint_html()
