import pandas as pd

URL = 'thegioididong.com'
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



# print(pd.read_csv('../iphone.csv')['id'].values.tolist())
def get_phone_id(file_path, column):
    return pd.read_csv(file_path)[column].values.tolist()

