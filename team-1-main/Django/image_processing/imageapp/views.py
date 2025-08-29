from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image
import os

# プロジェクトのベースディレクトリを取得
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 相対パスを指定
PROCESSED_IMAGE_PATH = os.path.join(BASE_DIR, 'media', 'after')

def image_upload(request):
    original_image_url = None
    processed_image_url = None

    if request.method == 'POST' and 'image' in request.FILES:
        # 获取上传的文件
        uploaded_image = request.FILES['image']
        original_image_name = os.path.splitext(uploaded_image.name)[0]  # 去掉文件扩展名

        # 打开上传的图像
        image = Image.open(uploaded_image)

        # 初始化处理后的文件名
        processed_image_name = original_image_name

        # 根据用户选择的操作处理图像，并为文件命名
        if request.POST['action'] == 'rotate':
            image = image.rotate(180)  # 旋转180度
            processed_image_name = f"Rotate_{original_image_name}"
        elif request.POST['action'] == 'flip':
            image = image.transpose(Image.FLIP_LEFT_RIGHT)  # 左右翻转
            processed_image_name = f"Flip_{original_image_name}"
        elif request.POST['action'] == 'resize':
            image = image.resize((int(image.width / 2), int(image.height / 2)))  # 缩小为原尺寸的一半
            processed_image_name = f"Resize_{original_image_name}"

        # 拼接处理后的完整文件路径
        processed_image_full_path = os.path.join(PROCESSED_IMAGE_PATH, f"{processed_image_name}.jpg")

        # 创建目录（如果不存在）
        os.makedirs(PROCESSED_IMAGE_PATH, exist_ok=True)

        # 检查处理后的图像文件是否已经存在，如果存在则删除
        if os.path.exists(processed_image_full_path):
            os.remove(processed_image_full_path)

        # 保存处理后的图像
        image.save(processed_image_full_path)

        # 生成处理后的图像 URL
        # Note: You might need to adjust the URL path according to your MEDIA_URL configuration
        processed_image_url = os.path.join('/media/after', f"{processed_image_name}.jpg")

    return render(request, 'imageapp/image_upload.html', {
        'original_image_url': original_image_url,
        'processed_image_url': processed_image_url,
    })
