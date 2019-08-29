import sys
sys.path.append('F:\python\project\\author_wanfang')
from author_detail import get_url

def run():
    path = 'F:\python\project\\author_wanfang\detail_last\last01.txt'
    get_url(5000,50000,path)

if __name__ == '__main__':
    run()