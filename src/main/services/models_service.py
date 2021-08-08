import os


def message_upload_path_create(instance, filename):
    _, file_extension = os.path.splitext(filename)
    return f"{instance.chat_id}/{instance.user_id}/%H_%M_%S_%f{file_extension}"
