import os
from flask import current_app
from PIL import Image


def add_profile_pic(pic_upload, username):
    filename = pic_upload.filename
    ext_type = filename.split(".")[-1]
    storage_filename = str(username) + '.' + ext_type
    filepath = os.path.join(current_app.root_path, 'static/image/user_profile', storage_filename)
    output_size = (200, 200)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename