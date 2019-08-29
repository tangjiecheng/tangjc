import fake_useragent

def ranking_list_headers():
    ua = fake_useragent.FakeUserAgent()
    headers={
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Content-Length': '13',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'med.wanfangdata.com.cn',
            'Origin': 'http://med.wanfangdata.com.cn',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
    }
    return headers

def base_info_headers():
    ua = fake_useragent.FakeUserAgent()
    headers={
        'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Content-Length': '14',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'med.wanfangdata.com.cn',
            'Origin': 'http://med.wanfangdata.com.cn',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
    }
    return headers

# headers={
#     'Accept': '* / *',
#     'Host': 'med.wanfangdata.com.cn',
#     'Connection': 'keep - alive',
#     'Content - Length': '13',
#     'Origin': 'http: // med.wanfangdata.com.cn',
#     'X - Requested - With': 'XMLHttpRequest',
#     # 'User - Agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 72.0.3626.109Safari / 537.36',
#     'Content - Type': 'application / x - www - form - urlencoded;charset = UTF - 8',
#     'Accept - Encoding': 'gzip, deflate',
#     'Accept - Language': 'zh - CN, zh;q = 0.9, en - US;q = 0.8, en;q = 0.7, zh - TW;q = 0.6',
#     'Cookie': 'SEARCHHISTORY_0=UEsDBBQACAgIAKlb%2FU4AAAAAAAAAAAAAAAABAAAAMM1VaWsTQRj%2BK7Iw%2FWJpk80eM4Eiu8kWiwdo%0AC4LWD2uzbQPb3ZDdGA%2BEVOxhNNBiD7FRS6k90NYL7WUV%2FCvN7Kb%2Fwncm8WjagH6phbB5570Gnud9%0A3rl2V%2FDNG7Z10RyyhLiTs%2B1WIZ0S4sItL2bEriYvy5IitAo5z8p2pX4meJaZ7RvsuZ2BkigEszYU%0ADPp%2BJt7ens%2Fn2%2FKm0286AynTN9v63KG2Pqe9VlL%2FO5%2F2%2FLaUe%2BZ3nw7TtltqxytuNtWBDAnpSUQS%0AyMAIRxCW40gUkaEgkkQaRgZBmoiIAs7Th3ORISMMHrkewsk4MmI8pnEXRlqSJRGdhaEZwUiH9ioi%0AKm%2FP78Eiy9E7mbNervNQApFOfgfmDaEEehoAk3Urk7U8L%2B06AEhlt1wtjMR7heD5yv7CTK9wquah%0ApenKbim%2BVyhWNtfo3O7%2B0w%2Fh7Erw%2FD79NrtXeBSUX9LxYrj4Ffr5HGKh5torDNO1JSgFo%2FLlWXV9%0AnRmbT%2Bj4Khjh8mRQLATFV3Sy%2BPs4PhG8KMMxmB%2BjY6PM%2BDhdXX7AWpXfBTNb%2FMrh6vLo%2FsIkc859%0ArWwtwcVObqjTzTnAuNIq9GUt07d60mxCorISw7IoiQoMxr3WZtPTb1%2F0b%2FoXkjFJ%2FA%2FT08jEyUAy%0AcgSSEpElFUBqjqTTpV3KJc55MibHgWTGyqbdLqffbfEG3Tx3pSzfTNstGXPA6k7fsTrEyEGlykgz%0AkK5wrWh1YeEE0nWuR5BrJ0qISFfrYtJ0LkHQXIRnyjwTlCeBqhqZo%2Buf6fYafbxTLb39vkG%2Fva5s%0ATdCRnXDqZSOnB6COHoZakqKiKgKKzaF2pW47k%2FTOqkQ6QStP5sjUsNIRVv9h5f2x6fQo%2BzGuJKRx%0AKsCvKU13Fp2aoI%2FGGncWW1jv39PFZZDPyRBVVJKPlpWiAI3Nub6qu5hY3jkiHYus%2FpJreEkSwAon%0ADOghPE9DJPoPpCtIl%2BtqYzGVayuBcJQZIDUSYzlahM1G7cFjjX49gQr71hQJOTB6zCBc3wrCBC5u%0AOjPhmyW6u1rZnmwcm%2BDTBi3NhuXhcOdJML8Zzo7Amxd82Annp8LVz8HDwsmYpcNPnRRTIwR2hkTu%0AXf8BUEsHCMmlW8A7AwAAKgkAAA%3D%3D%0A; firstvisit_backurl=http%3A//www.wanfangdata.com.cn; Hm_lvt_838fbc4154ad87515435bf1e10023fab=1563884908,1564391666,1564588137,1564727747; Hm_lpvt_838fbc4154ad87515435bf1e10023fab=1564732166; popped=true; searchHistory=W3siQ3JlYXRlVGltZSI6IjIwMTktMDgtMDJUMTk6MTI6MzMuOTc1MDc2NSswODowMCIsIkhpdENvdW50IjozODMsIlVybCI6InE95L2c6ICFPShBMDAwMDAwMDE0KSBBTkQg5pyf5YiKSUQ9KHpnenp6eikm6LWE5rqQ57G75Z6LX2ZsPSjkuK3mlofmnJ_liIopIiwiRmF2b3VyaXRlQ29udGVudCI6Ilt7XCJLZXlcIjpcInFcIixcIlZhbHVlXCI6XCLkvZzogIU9KEEwMDAwMDAwMTQpIEFORCDmnJ_liIpJRD0oemd6enp6KVwifSx7XCJLZXlcIjpcIui1hOa6kOexu-Wei19mbFwiLFwiVmFsdWVcIjpcIijkuK3mlofmnJ_liIopXCJ9XSIsIlF1ZXJ5IjpudWxsfV01; Hm_cv_af200f4e2bd61323503aebc2689d62cb=1*facetMoreBtn*facetMoreBtn; Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1563450322,1564533354,1564744247,1564745799; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1564968313; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%5d%2c%22Data%22%3a%5b%5d%2c%22SessionId%22%3a%224d65d1ff-6cea-42cc-afa6-5c0258977c3e%22%2c%22Sign%22%3anull%7d%2c%22LastUpdate%22%3a%222019-08-05T01%3a25%3a13Z%22%2c%22TicketSign%22%3a%22sNmpjTz0XR1FjizBsf6rrQ%3d%3d%22%7d',
#     'User-Agent':ua.random
#     }




# 'Accept': 'application / json, text / javascript, * / *; q = 0.01',
#                 'Accept - Encoding': 'gzip, deflate',
#                 'Accept - Language': 'zh - CN, zh;q = 0.8, zh - TW;q = 0.7, zh - HK;q = 0.5, en - US;q = 0.3, en;q = 0.2',
#                 'Cache - Control': 'max - age = 0',
#                 'Connection': 'keep - alive',
#                 'Content - Length': '14',
#                 'Content - Type': 'application / x - www - form - urlencoded;charset = UTF - 8',
#                 'Cookie': 'WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%5d%2c%22Data%22%3a%5b%5d%2c%22SessionId%22%3a%229c5e7fc6-5b4c-4415-92a5-dbcf8f3d8b02%22%2c%22Sign%22%3anull%7d%2c%22LastUpdate%22%3a%222019-08-05T05%3a44%3a16Z%22%2c%22TicketSign%22%3a%22Igr1gENP84onkIhUlfEutQ%3d%3d%22%7d; Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1564983844; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1564983856',
#                 'Host': 'med.wanfangdata.com.cn',
#                 'Referer': 'http://med.wanfangdata.com.cn/Author/Professional/A0010908495',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
#                 'X-Requested-With': 'XMLHttpRequest'