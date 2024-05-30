
import requests
from bs4 import BeautifulSoup
import urllib.parse
import logging
import traceback
import time
from .JPXError import JPXAnalysisError

logger = logging.getLogger(__name__)


class TDnetDisclosureRecord():

    def __init__(self, date_str, \
                        kj_time_str, \
                        kj_code_str, \
                        kj_name_str, \
                        kj_title_str, \
                        pdf_url_str, \
                        xbrl_url_str, \
                        kj_place_str, \
                        kj_history_str) :

        self.date_str = date_str
        self.kj_time_str = kj_time_str
        self.kj_code_str = kj_code_str
        self.kj_name_str = kj_name_str
        self.kj_title_str = kj_title_str
        self.pdf_url_str = pdf_url_str
        self.xbrl_url_str = xbrl_url_str
        self.kj_place_str = kj_place_str
        self.kj_history_str = kj_history_str

        self.unique_code = f'{date_str} {kj_time_str} {kj_code_str} {kj_title_str}'


    def __str__(self) :

        return f'{self.date_str}, {self.kj_time_str}, {self.kj_code_str}, {self.kj_name_str}, {self.kj_title_str}, {self.pdf_url_str}, {self.xbrl_url_str}, {self.kj_place_str}, {self.kj_history_str}'


class TDnetAnalyzer() :


    @staticmethod
    def get_DisclosureRecordList() :

        date_str = '20240517'
        page_num = 1
        page_is_end = False

        disclosure_record_list = list()

        #最終ページまで処理する
        while page_is_end == False :

            #リクエストURLを生成
            page_str = f'{page_num:03}'
            url = f'https://www.release.tdnet.info/inbs/I_list_{page_str}_{date_str}'


            #GETリクエストしページソースを取得する
            soup = None
            r = None
            retry_count = -1
            while retry_count < 10 :

                retry_count = retry_count + 1

                
                try :

                    logger.debug(f'request count : {retry_count} , url : {url}')
                    r = requests.get(url)

                except requests.exceptions.RequestException as e:

                    r.close()
                    logger.error(list(traceback.TracebackException.from_exception(e).format()))
                    time.sleep(10)

                    continue


                #ページリソースがないなら最終ページを越えていると判断する
                if r.status_code == 404 :

                    r.close()
                    page_is_end = True
                    logger.debug('page is end')

                    break


                #その他のエラー
                if r.status_code != 200 :

                    logger.debug(f'request status {r.status_code} , sleep 10s and retry')
                    r.close()
                    time.sleep(10)

                    continue


                #status_code 200ならページソースを取得する
                soup = BeautifulSoup(r.content, 'html.parser')
                r.close()
                break



            #リトライオーバーしたら処理を終了する
            if retry_count >= 10 :

                raise JPXAnalysisError('リクエストリトライオーバー')


            #ページソースを取得できていないなら同一ページの処理を繰り返す
            if soup == None :
                continue


            #ページソースの解析

            tr_elms = soup.select('table#main-list-table > tr')
            for tr_elm in tr_elms :

                kj_time_str = None
                kj_code_str = None
                kj_name_str = None
                kj_title_str = None
                pdf_url_str = None
                xbrl_url_str = None
                kj_place_str = None
                kj_history_str = None

                td_elms = tr_elm.select('td')
                for td_elm in td_elms :

                    class_list = td_elm.get("class")
                    if 'kjTime' in class_list :

                        kj_time_str = td_elm.get_text().strip()

                    elif 'kjCode' in class_list :

                        kj_code_str = td_elm.get_text().strip()

                    elif 'kjName' in class_list :

                        kj_name_str = td_elm.get_text().strip()

                    elif 'kjPlace' in class_list :

                        kj_place_str = td_elm.get_text().strip()

                    elif 'kjHistroy' in class_list :

                        kj_history_str = td_elm.get_text().strip()

                    elif 'kjTitle' in class_list :

                        a_elm = td_elm.select_one('a')

                        kj_title_str =  a_elm.get_text().strip()

                        pdf_name_str = a_elm.get("href")
                        pdf_url_str = urllib.parse.urljoin('https://www.release.tdnet.info/inbs/', pdf_name_str)


                    elif 'kjXbrl' in class_list :

                        a_elm = td_elm.select_one('a')

                        if a_elm != None :

                            xbrl_name_str = a_elm.get("href")
                            xbrl_url_str = urllib.parse.urljoin('https://www.release.tdnet.info/inbs/', xbrl_name_str)

                        else :

                            xbrl_url_str = ""


                disclosure_record_list.append(TDnetDisclosureRecord(date_str, \
                                                                        kj_time_str, \
                                                                        kj_code_str, \
                                                                        kj_name_str, \
                                                                        kj_title_str, \
                                                                        pdf_url_str, \
                                                                        xbrl_url_str, \
                                                                        kj_place_str, \
                                                                        kj_history_str))

            #次のページへ
            page_num = page_num + 1



        return disclosure_record_list
                