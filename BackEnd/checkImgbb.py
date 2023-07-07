import requests

# imgbb hoat dong

def check_imgbb_api_key(api_key):
    url = f'https://api.imgbb.com/1/upload?key={api_key}'
    response = requests.get(url)
    if str(response.content)[41 :60] == "Empty upload source":
        return True
    else:
        return False

def check_imgbb_update(list_api_key , index):
    if check_imgbb_api_key(list_api_key[index])==True:
        return True
    check_imgbb_api_key(list_api_key[index+1])

