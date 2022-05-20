import pandas as pd
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import json

pd.set_option('max_colwidth', 1000)
pd.set_option('max_rows', 1000)

APPLICATION_ID = '<enter-your-auth-token-here>'

def call_api(payload):
    try:
        api = Finding(appid=APPLICATION_ID, config_file=None)
        response = api.execute('findItemsAdvanced', payload)
        return response
    except ConnectionError as e:
        print(e)
        print(e.response.dict())

def main():
    keywords = [
        'iphone',
        'iphone 10',
        'iphone 11',
        'iphone pro',
        'iphone pro max',
        'iphone mini',
        'iphone 12',
        'iphone 13',
        'iphone xr',
        'smartphone',
        'android',
        'samsung galaxy',
        'samsung galaxy s22',
        'samsung galaxy a53',
        'samsung galaxy phone',
    ]
    total_count = 0
    for keyword in keywords:
        count = 1 # start this at 1 so we can enter the while loop
        i = 0
        while count != 0:
            payload = {
                'keywords': keyword,
                'paginationInput':
                    {
                        'pageNumber': i+1,
                        'entriesPerPage': 200
                    }
            }
            r = call_api(payload)
            j = json.loads(r.json())
            print("Items in {}: {} ".format(i,j['searchResult']['_count']))
            count = j['searchResult']['_count']
            if int(j['searchResult']['_count']) == 0: break
            total_count += int(j['searchResult']['_count'])
            f = open('{}_{}.csv'.format(keyword,i),'w')
            f.write('"title","pCategoryName","pCategoryID","sCategoryName","sCategoryID","itemId","price"\n')
            for item in r.reply.searchResult.item:
                """
                The attributes we'll be accesing:
                pCategoryName - item.primaryCategory.categoryName
                pCategoryID - item.primaryCategory.categoryId
                sCategoryName - item.secondaryCategory.categoryName
                sCategoryID - item.secondaryCategory.categoryId
                itemId - item.itemId
                price - item.sellingStatus.currentPrice.value
                """
                try:
                    f.write('\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"\n'.format(str(item.title).replace('"',''),str(item.primaryCategory.categoryName).replace('"',''),\
                            str(item.primaryCategory.categoryId).replace('"',''),str(item.secondaryCategory.categoryName).replace('"',''),\
                            str(item.secondaryCategory.categoryId).replace('"',''),str(item.itemId).replace('"',''), str(item.sellingStatus.currentPrice.value).replace('"','')))
                except AttributeError:
                    f.write('\"{}\",\"{}\",\"{}\",\"\",\"\",\"{}\",\"{}\"\n'.format(str(item.title).replace('"',''),str(item.primaryCategory.categoryName).replace('"',''),\
                            str(item.primaryCategory.categoryId).replace('"',''),str(item.itemId).replace('"',''),str(item.sellingStatus.currentPrice.value).replace('"','')))
            f.close()
            i += 1
    print(total_count)

if __name__ == '__main__':
    main()
