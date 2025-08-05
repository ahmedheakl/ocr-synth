def extract_dir_path(path: str) -> str:
    path_split = path.split("/")[0:-1]
    return "/".join(path_split) + "/"

def extract_fname_with_ext(path: str) -> str:
    print(f'path extract fname {path}')
    return path.split("/")[-1]

def extract_fname_wo_ext(path: str) -> str:
    if (type(path) != str):
        return ""
    file_name = extract_fname_with_ext(path)
    return file_name.split(".")[0]

def extract_file_ext(path: str) -> str:
    if (type(path) == str):
        return path.split(".")[-1]
    return None

def replace_file_extension(path: str, new_extension: str) -> str:
    split = path.split(".")
    split[-1] = new_extension
    return ".".join(split)
