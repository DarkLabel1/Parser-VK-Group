import requests
import time
import os

USER_TOKEN = 'a2ad71b9a36ae1748f12a9b3bff7b580f415d8ea3504c95c9fc70c5d28c49bc2fb6d097fbf20b167f3111'
VERSION = '5.103'

ALBUM_ID = []
DOWNLOAD = []

OWNER_ID = input('Введите id группы: ')
PATH = input('Введите путь к папке куда будут сохраняться альбомы: ')

def download_url_photo(PHOTO_HREF, NAME_ALBUM, ID_PHOTO):
	r = requests.get(PHOTO_HREF, stream=True)
	with open(PATH + '\\' + NAME_ALBUM + '\\photo\\' + str(ID_PHOTO) + '.jpg', 'wb') as f:
		for chunk in r.iter_content(8192):
			f.write(chunk)

def download_url_doc(ID_PHOTO, NAME_ALBUM):
	ex = DOWNLOAD[0]['EXT']
	ur = DOWNLOAD[0]['URL']
	with open(PATH + '\\' + NAME_ALBUM + '\\DOC\\' + str(ID_PHOTO) + '.' + str(ex), 'wb') as out:
		r = requests.get(ur, stream=True)
		for chunk in r.iter_content(8192):
			out.write(chunk)
	DOWNLOAD.clear()

def file_create(NAME_ALBUM):
	try:
		path_in_album = PATH + '\\' + NAME_ALBUM
		os.mkdir(path_in_album)

		path_in_foto = path_in_album + '\\' + 'photo'
		os.mkdir(path_in_foto)
		path_in_doc = path_in_album + '\\' + 'DOC'
		os.mkdir(path_in_doc)
	except:
		pass

def GROUPS_ALBUM(OWNER_ID=OWNER_ID):
	URL = 'https://api.vk.com/method/photos.getAlbums?owner_id=-{}&access_token={}&v={}'.format(OWNER_ID, USER_TOKEN, VERSION)
	time.sleep(3)
	response_album = requests.get(URL).json()['response']['items']
	for i in response_album:
		id = i['id']
		title = i['title']
		ALBUM_ID.append({
			'ID': id,
			'TITLE': title
			})

def ALBUM_PHOTO(OWNER_ID=OWNER_ID):
	for i in ALBUM_ID:
		URL = 'https://api.vk.com/method/photos.get?owner_id=-{}&album_id={}&access_token={}&v={}'.format(OWNER_ID, i['ID'], USER_TOKEN, VERSION)
		time.sleep(3)
		response_photos = requests.get(URL).json()['response']['items']
		for a in response_photos:
			id_photo = a['id']
			kol = len(a['sizes']) - 1
			href_photo = a['sizes'][kol]['url']
			file_create(i['TITLE'])
			download_url_photo(href_photo, i['TITLE'], id_photo)
			PHOTO_DOCUMENTS(OWNER_ID, PHOTO_ID=id_photo)
			download_url_doc(str(id_photo), i['TITLE'])
			print('Альбом {} скачивается.'.format(i['TITLE']))


def PHOTO_DOCUMENTS(OWNER_ID, PHOTO_ID):
	URL = 'https://api.vk.com/method/photos.getComments?owner_id=-{}&photo_id={}&count=100&access_token={}&v={}'.format(OWNER_ID, PHOTO_ID, USER_TOKEN, VERSION)
	time.sleep(3)
	response_comments = requests.get(URL).json()['response']['items']
	for i in response_comments:
		try:
			o = 0
			if (o == 0):
				ext = i['attachments'][0]['doc']['ext']
				url = i['attachments'][0]['doc']['url']
				DOWNLOAD.append({
					'EXT': ext,
					'URL': url
					})
				o = o + 1
			else:
				pass
		except:
			pass


if __name__ == '__main__':
	GROUPS_ALBUM(OWNER_ID)
	ALBUM_PHOTO(OWNER_ID)