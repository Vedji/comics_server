import requests


def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Файл '{filename}' успешно скачан.")
    else:
        print(f"Ошибка при скачивании файла: статус-код {response.status_code}")


for i in range(1, 19):
    download_file(
        f"https://img33.imgslib.link//manga/gabriel-dropout/chapters/2-10/gabriel-dropout_vol2_chapter10_page{i}.jpg",
        f"C:\\Users\\stret\\Documents\\uploads_files\\Gabriel_dropout_shcool\\chapter_10\\{i}.jpg")
