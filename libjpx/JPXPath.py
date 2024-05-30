import os
import glob
from .JPXError import JPXAnalysisError

class JPXXbrlPath() :

	def __init__(self, xbrl_dir_path) :

		self.__xsd_file_path = JPXXbrlPath.get_xbrl_file_path(xbrl_dir_path, 'xsd')
		self.__lab_file_path = JPXXbrlPath.get_xbrl_file_path(xbrl_dir_path, 'lab.xml')
		self.__ixbrl_file_path_list = JPXXbrlPath.get_inline_xbrl_file_path_list(xbrl_dir_path)
		self.__def_linkbase_file_path = JPXXbrlPath.get_xbrl_file_path(xbrl_dir_path, 'def.xml')
		self.__pre_linkbase_file_path = JPXXbrlPath.get_xbrl_file_path(xbrl_dir_path, 'pre.xml')
		self.__cal_linkbase_file_path = JPXXbrlPath.get_xbrl_file_path(xbrl_dir_path, 'cal.xml')
		self.__xbrl_dir_path = xbrl_dir_path


	@staticmethod
	def get_inline_xbrl_file_path_list(xbrl_dir_path) :


		file_path_list = JPXXbrlPath.get_xbrl_file_path_list(xbrl_dir_path, '-ixbrl.htm')

		if len(file_path_list) == 0 :

			file_path_list = JPXXbrlPath.get_xbrl_file_path_list(xbrl_dir_path, '_ixbrl.htm')

		return file_path_list


	@staticmethod
	def get_xbrl_file_path(xbrl_dir_path, file_kind_str) :

		file_path_list = JPXXbrlPath.get_xbrl_file_path_list(xbrl_dir_path, file_kind_str)
		if len(file_path_list) == 1 :

			return file_path_list[0]

		elif len(file_path_list) == 0 :

			return 'no files'

		else :

			raise JPXAnalysisError('duplication xbrl file is there ')

	@staticmethod
	def get_xbrl_file_path_list(xbrl_dir_path, file_kind_str) :

		file_path_list =  glob.glob(f'{xbrl_dir_path}/*{file_kind_str}')

		return file_path_list


	def get_xbrl_dir_path(self):
		return self.__xbrl_dir_path

	def get_ixbrl_file_path_list(self):
		return self.__ixbrl_file_path_list

	def get_xsd_file_path(self) :
		return self.__xsd_file_path

	def get_lab_file_path(self) :
		return self.__lab_file_path

	def get_pre_file_path(self) :
		return self.__pre_linkbase_file_path

	def get_def_file_path(self) :
		return self.__def_linkbase_file_path

	def get_cal_file_path(self) :
		return self.__cal_linkbase_file_path



def get_jpx_file_db_csv_path(stock_code) :

	return '.' + os.sep + 'tdnet_xbrl_list_csv' + os.sep + str(stock_code) + '.csv'

def get_xbrl_file_path(xbrl_record) :

	return '.' + os.sep + 'jpx_file' + os.sep + str(xbrl_record.stock_code) + os.sep + xbrl_record.xbrl_url.split('/')[-1]


