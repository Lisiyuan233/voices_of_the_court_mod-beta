import os
import re
import zipfile
from pathlib import Path

def get_version_from_mod_file(mod_file_path):
    """从mod文件中提取版本号"""
    try:
        with open(mod_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # 使用正则表达式查找版本号
            version_match = re.search(r'version="([^"]+)"', content)
            if version_match:
                return version_match.group(1)
            else:
                raise ValueError("无法在mod文件中找到版本号")
    except Exception as e:
        print(f"读取mod文件时出错: {e}")
        return None

def create_mod_package():
    # 定义路径
    mod_root = Path(r"c:\Users\A\Documents\paradox interactive\Crusader Kings III\mod\voices_of_the_court_mod")
    mod_file_path = mod_root / "voices_of_the_court_mod.mod"
    
    # 获取版本号
    version = get_version_from_mod_file(mod_file_path)
    if not version:
        print("无法获取版本号，终止打包")
        return
    
    # 创建压缩包名称
    zip_name = f"voices_of_the_court_mod{version}.zip"
    zip_path = mod_root.parent / zip_name
    
    # 定义要包含的文件夹和文件
    folders_to_include = [
        "common",
        "events", 
        "gfx",
        "gui",
        "localization"
    ]
    
    files_to_include = [
        "README.md",
        "voices_of_the_court_mod.mod"
    ]
    
    print(f"正在创建压缩包: {zip_name}")
    print(f"版本号: {version}")
    
    # 创建ZIP文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 添加文件夹
        for folder in folders_to_include:
            folder_path = mod_root / folder
            if folder_path.exists():
                print(f"添加文件夹: {folder}")
                for file_path in folder_path.rglob('*'):
                    if file_path.is_file():
                        # 计算相对路径，确保在压缩包中的结构正确
                        arcname = Path("voices_of_the_court_mod") / folder / file_path.relative_to(folder_path)
                        zipf.write(file_path, arcname)
            else:
                print(f"警告: 文件夹 {folder} 不存在")
        
        # 添加文件到voices_of_the_court_mod文件夹内
        for file in files_to_include:
            file_path = mod_root / file
            if file_path.exists():
                print(f"添加文件到voices_of_the_court_mod文件夹内: {file}")
                arcname = Path("voices_of_the_court_mod") / file
                zipf.write(file_path, arcname)
            else:
                print(f"警告: 文件 {file} 不存在")
        
        # 添加voices_of_the_court_mod.mod文件到压缩包根目录
        if mod_file_path.exists():
            print(f"添加文件到压缩包根目录: voices_of_the_court_mod.mod")
            zipf.write(mod_file_path, "voices_of_the_court_mod.mod")
    
    print(f"压缩包创建完成: {zip_path}")

if __name__ == "__main__":
    create_mod_package()