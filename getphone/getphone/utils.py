import pandas as pd, re


# print(pd.read_csv('../iphone.csv')['id'].values.tolist())
def get_phone_id(file_path, column):
    return pd.read_csv(file_path)[column].values.tolist()

# get url from link ..../123456/img_url.jpg
url_pattern = re.compile(r'(\d{6})\/(.*)')
def get_url_img(long_url, group_number):
    # group(0): get phone_id
    # group(1): get url_img
    return url_pattern.search(long_url).group(group_number)


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



