# Placeholder

def get_file(full_name: str) -> Optional[bytes]:
    """Get the file

    Args:
        full_name (str): The path of the file (including file name)

    Returns:
        list: The file, None if the path is invalid
    """
    path = os.path.join(storage_path, full_name)
    if not os.path.isfile(path):
        return None
    with open(path, 'rb') as f:
        return f.read()
    



def load_certificate_file(file_name):
    try:
        with open(file_name, 'r') as file:
            certificate = file.read()
        return certificate
    except FileNotFoundError:
        print(f"文件 {file_name} 未找到")
        return None
    except IOError:
        print("文件读取错误")
        return None



