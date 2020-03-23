import requests, lxml
from bs4 import BeautifulSoup
import os, pprint

DIR_PATH = 'programmers/'
LEVEL_DIR_PATH = lambda x: 'level{}/'.format(x)

def crawling_problem():
    p_level = input('input Problem Level\n>> ')
    p_url = input('Input Problem URL\n>> ').replace(' ', '')
    if '?language=python3' not in p_url: p_url = ''.join([p_url, "?language=python3"])
    html = requests.get(p_url).text
    soup = BeautifulSoup(html, 'lxml')

    ############################
    # <q> 태그를 " 문자로 변환 #
    ############################
    for q in soup.findAll('q'):
        text = q.get_text()
        q.replaceWith('"{}"'.format(text))

    # 카테고리, 문제이름
    p_category = soup.select_one('body > div.navbar.navbar-dark.navbar-expand-lg.navbar-application.navbar-breadcrumb '
                               '> ol > li:nth-child(2) > a').get_text()
    p_name = soup.select_one('body > div.navbar.navbar-dark.navbar-expand-lg.navbar-application.navbar-breadcrumb '
                               '> ol > li.active').get_text()
    filename = '[{}] {}'.format(p_category, p_name)

    # 코드
    code = soup.select_one('#code').get_text()

    # 입출력 예
    p_input_list = []
    p_output_list = []

    p_example_tr_list = soup.select("#tour2 > div > div > table > tbody > tr")
    p_example_td_list = [e.find_all('td') for e in p_example_tr_list]

    for *i, o in p_example_td_list:
        p_input_list.append([a.get_text() for a in i])
        p_output_list.append(o.get_text())

    test_code_list = []
    for i, o in zip(p_input_list, p_output_list):
        test_code_list.append('print(solution({}) == {})'.format(', '.join(i), o))

    test_code = '\n    '.join(test_code_list)

    # 파일 내용
    default_code = """{}
    
if __name__ == "__main__":
    {}""".format(code, test_code)

    file = DIR_PATH + LEVEL_DIR_PATH(p_level) + filename + '.py'

    try:
        if not os.path.exists(DIR_PATH + LEVEL_DIR_PATH(p_level)):
            os.makedirs(DIR_PATH + LEVEL_DIR_PATH(p_level))
    except OSError:
        print(DIR_PATH + LEVEL_DIR_PATH(p_level), '폴더 생성 오류!')

    if os.path.isfile(file):
        print('해당 문제의 파일은 이미 존재합니다.')
    else:
        with open(file, 'w', encoding='utf-8') as f:
            f.write('# ' + filename + '\n')
            f.write(default_code)
        print(file, '생성 완료')

if __name__ == "__main__":
    crawling_problem()