import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

# 允许的文件类型
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg',
    'mp3', 'wav', 'mp4', 'avi', 'mov',
    'zip', 'rar', '7z', 'tar', 'gz'
}

def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_size(file_path):
    """获取文件大小（字节）"""
    return os.path.getsize(file_path)

def save_uploaded_file(file, file_path):
    """保存上传的文件"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file.save(file_path)

def get_file_extension(filename):
    """获取文件扩展名"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def generate_unique_filename(original_filename):
    """生成唯一的文件名"""
    extension = get_file_extension(original_filename)
    unique_id = str(uuid.uuid4())
    return f"{unique_id}.{extension}" if extension else unique_id

def format_file_size(size_bytes):
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

def clean_filename(filename):
    """清理文件名，移除特殊字符"""
    # 移除路径分隔符
    filename = filename.replace('/', '').replace('\\', '')
    # 移除控制字符
    filename = ''.join(c for c in filename if ord(c) >= 32)
    # 限制长度
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename
