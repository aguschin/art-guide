from services import run_all_models

file_path = '/home/jason/Downloads/test_mona.jpg'
image_url = f'file://{file_path}'

run_all_models(filename="test_mona", photo_url=image_url)