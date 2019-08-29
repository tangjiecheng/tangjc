import traceback

from tools import lxml_to_string


def is_page_false(html):
    try:
        html_str=lxml_to_string(html)
        page_status=True
        if len(html.xpath('//body//div[@class="error"]'))!=0:
            str=lxml_to_string(html.xpath('//body')[0])
            page_status=False
        return page_status
    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass