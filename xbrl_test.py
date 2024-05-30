import glob
import os
import time
import sys

from libjpx import JPXXbrlPath,XBRLLinkBaseTree,XBRLInstanceFileAnalysis,TDnetAnalyzer

import logging
from logging import StreamHandler, FileHandler, Formatter
from logging import INFO, DEBUG, NOTSET


#ログの設定
stream_handler = StreamHandler()
stream_handler.setLevel(DEBUG)
#stream_handler.setFormatter(Formatter("%(asctime)s - %(levelname)s:%(name)s - %(message)s"))
stream_handler.setFormatter(Formatter("%(asctime)s@ %(name)s [%(levelname)s] %(funcName)s: %(message)s"))

if not os.path.exists('.' + os.sep + 'log') :
	os.makedirs('.' + os.sep + 'log')

datetime_str = time.strftime('%Y%m%d%H%M%S', time.localtime())
log_file_path = '.' + os.sep + 'log' + os.sep + 'xbrl_test_' + datetime_str + '.log'
file_handler = FileHandler(log_file_path, encoding='utf-8')
#file_handler.setFormatter(Formatter("%(asctime)s - %(levelname)s:%(name)s - %(message)s"))
file_handler.setFormatter(Formatter("%(asctime)s@ %(name)s [%(levelname)s] %(funcName)s: %(message)s"))
file_handler.setLevel(DEBUG)

logging.basicConfig(level=NOTSET, handlers = [stream_handler, file_handler]) 



#XBRLのパスを生成
xbrl_dir_path = 'C:\\Users\\QUWE\\Desktop\\Xbrl_Search_20240526_141658\\S100R5AK\\XBRL\\PublicDoc'
xbrl_path_data = JPXXbrlPath(xbrl_dir_path)


##インラインXBRLを読み込む
xbrlInstanceFileData = XBRLInstanceFileAnalysis(xbrl_path_data)

#処理対象は連結貸借対照表
rol_str = 'rol_ConsolidatedBalanceSheet'

#表示リンクベースを読み込む
pre_tree = XBRLLinkBaseTree('presentation', xbrl_path_data)

#定義リンクベースファイルを読み込む
def_tree = XBRLLinkBaseTree('definition', xbrl_path_data)


#表示リンクベースファイルを元に値を取得する

#スキーマファイルを読み込む
pre_tree.read_xsd_file(rol_str)

#日本語名称を読み込む
pre_tree.read_jp_lab_file(rol_str)

#ディメンションデフォルトを定義リンクベースファイルから読み込む
pre_tree.set_dimension_default(def_tree, rol_str)

#値の取得
selected_axis_member_dict = {}
pre_tree.read_instance_data(rol_str, xbrlInstanceFileData, selected_axis_member_dict, 'CurrentYear', 'Prior1Year')

#読み込み結果を表示
pre_tree.show_tree(rol_str)


#計算リンクベースファイルから構造を取得し、上記で読み込んだ値を
#構造に転記する
cal_tree = XBRLLinkBaseTree('calculation', xbrl_path_data)
cal_tree.read_xsd_file(rol_str)
cal_tree.read_jp_lab_file(rol_str)
cal_tree.set_dimension_default(def_tree, rol_str)
cal_tree.set_preferred_label(pre_tree, rol_str)

cal_tree.read_instance_data_from_another_tree(pre_tree, rol_str)

#結果を表示
cal_tree.show_tree(rol_str)
