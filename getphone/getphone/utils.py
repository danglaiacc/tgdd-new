import pandas as pd, re


# print(pd.read_csv('../iphone.csv')['id'].values.tolist())
def get_phone_id(file_path, column='id'):
    return pd.read_csv(file_path)[column].values.tolist()


# get url from link ..../123456/img_url.jpg
pattern_url_img = re.compile(r'\/\d{6}\/(.*?)\"')
def get_url_img_from_tag(img_tag, remove_string=''):
    # vì có những thẻ có url_img bằng data-src hoặc src, nên phải trích xuất kiểu này
    match = pattern_url_img.search(img_tag)
    if match:
        url_img = match.group(1)
        return re.sub(remove_string,'', url_img)
#    else:
#        with open('utils.21.txt', 'a', encoding='utf8') as f:
#            f.write(img_tag+'\n')

def get_modal_id_from_tag(img_tag):
    return re.findall(r'\d{6}', img_tag)[0]


pattern_remove = re.compile(r'\d+GB|\(|\)|/|Hộp mới|Vàng Rực Rỡ|Đặc Biệt')
pattern_split = re.compile(r'(?P<manu_text>^\S+) (?P<version_text>.+)')
pattern_modal_text = re.compile(r'\d+GB/\d+GB|\d+GB')

def clean_phone_name(string):
    # get manu_text and version_text from phone name
    modal_text = ''
    if (abc:=pattern_modal_text.search(string)):
        modal_text =abc.group(0)

    string = re.sub(pattern_remove, '',string)
    # remove multiple space
    string = re.sub(r'\s{2,}',' ',string)
    string = re.sub(r'\s+$', '', string)

    # split manu text and version text 
    match = re.match(pattern_split, string)
    return {**match.groupdict(), 'modal_text':modal_text}


url_full = 'https://www.thegioididong.com/dtdd-apple-iphone#c=42&m=80,2,1971,2236,2235,5332,19,1,2326,17201,4832,20673&o=9&pi=0'
# url_full = 'https://www.thegioididong.com/dtdd-apple-iphone#c=42&m=80&o=9&pi=0'
script_full = '''
       function main(splash, args)
           splash:on_request(function(request)
               if request.url:find('css') then
                   request.abort()
               end
           end)
           splash.images_enabled = false
           splash.js_enabled = false
           assert(splash:go(args.url))
           assert(splash:wait(0.5))
           return splash:html()
       end
    '''
script_more = '''
          function main(splash, args)
            splash:on_request(function(request)
              if request.url:find('css') then
                request.abort()
              end
            end)
            splash.images_enabled = false 
            
            time = 0.5
            assert(splash:go(args.url))
            assert(splash:wait(time))
            
            btn = assert(splash:select(".view-more a"))
            assert(splash:wait(time))
          
            while btn:visible() do
              btn:mouse_click()
              assert(splash:wait(time))
              btn = assert(splash:select(".view-more a"))
            end
            
            return {
              html = splash:html(),
              png = splash:png(),
              har = splash:har(),
            }
          end
        '''



