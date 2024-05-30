import requests
from bs4 import BeautifulSoup
import time
import logging
import hashlib
import os

logger = logging.getLogger(__name__)



#サーバ上のXMLファイルをキャッシュする
class XMLDataGetter() :

	data_cache = {}

	@classmethod
	def get(cls, data_path):


		soup = None

		if data_path in cls.data_cache :

			logger.debug('get xml from cache:' + data_path)
			soup = cls.data_cache[data_path]

		elif cls.__get_cache_file_path(data_path) in cls.data_cache :

			logger.debug('get xml from cache:' + data_path)
			soup = cls.data_cache[cls.__get_cache_file_path(data_path)]

		elif data_path.startswith('http') and os.path.exists(cls.__get_cache_file_path(data_path)) :

			logger.debug('get xml from webcache:' + cls.__get_cache_file_path(data_path))
			soup = cls.__get_from_local_path(cls.__get_cache_file_path(data_path))

		elif data_path.startswith('http') :

			logger.debug('get xml from url:' + data_path)
			soup = cls.__get_from_html_path(data_path)

		else :

			logger.debug('get xml from local:' + data_path)
			soup = cls.__get_from_local_path(data_path)

		return soup

	@classmethod
	def clear_cache(cls):
		cls.data_cache = {}

	@classmethod
	def __get_from_html_path(cls, url):

		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'xml')
		content_data = r.content
		r.close()

		time.sleep(1.0)

		cls.data_cache[url] = soup
		cls.__save_cache_file(content_data, url)
		return soup

	@classmethod
	def __get_from_local_path(cls, local_path):


		fin = open(local_path, 'rb')
		bdata = fin.read()
		soup = BeautifulSoup(bdata, 'xml')
		fin.close()


		cls.data_cache[local_path] = soup

		return soup

	@classmethod
	def __get_cache_file_path(cls, url) :

		hash_str = hashlib.sha256(url.encode('utf-8')).hexdigest()
		cash_file_path = '.' + os.sep + 'webcache' + os.sep + 'xml_text_' + url.translate(str.maketrans('/\\.:', '____')) +'_' + hash_str
		return cash_file_path


	@classmethod
	def __save_cache_file(cls, content_data, url):


		if not os.path.exists('.' + os.sep + 'webcache') :
			os.mkdir('.' + os.sep + 'webcache')

		f = open(XMLDataGetter.__get_cache_file_path(url), 'wb')
		f.write(content_data)
		f.close()

