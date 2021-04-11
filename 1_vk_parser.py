import requests
import shutil
import vk_api


if __name__ == '__main__':
    vk_session = vk_api.VkApi('LOGIN', 'PASSWORD')
    vk_session.auth()
    vk = vk_session.get_api()
    offset = 0
    while True:
        response = vk.groups.get_members(group_id='pgpuspb', count=1000, offset=offset, fields='photo_200')
        for item in response['items']:
            if 'deactivated' not in item['photo_200'] and 'camera' not in item['photo_200']:
                while True:
                    try:
                        r = requests.get(item['photo_200'], stream=True)
                        r.raw.decode_content = True
                        break
                    except ConnectionError:
                        pass
                with open('jpg/{}.jpg'.format(item['id']), 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
        count = response['count']
        if offset >= count:
            break
        else:
            offset += 1000
