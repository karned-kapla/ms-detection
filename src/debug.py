from src.treat import treat

data = {
    'uuid_detection': 'e5822b9a-eeb4-4303-bbed-9eac0e72af48',
    'url': 'https://api.francelive.fr/resources'
           '/Jrb9CPou0YLx68fBAvHJ0QB4Cth6L6ad7U9Ya_e5CN7ziXoZuYVIXnxp5wcYn3XYa3Y60uKOgyZ_ezJWdhtKKrU6q0KpJxbjvCX6ySbQe0c?width=512',
    'model_name': 'yolo11l', 'uuid_user': '87d478de-8ca7-4b48-ab0f-7d843d44fbba',
    'uuid_entity': 'a4cfe4a1-35fb-4c91-afb6-14f8c05c4265', 'uuid_credentials': '1efaeb5d-b01d-47f4-8423-d822185c7a0f'
}
print(data)

treat(data)
