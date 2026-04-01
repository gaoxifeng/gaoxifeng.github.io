import os, glob
from PIL import Image

def convert_dir(base_dir):
    count = 0
    saved_kb = 0
    for ext in ['*.jpg','*.jpeg','*.png','*.gif','*.JPG','*.JPEG','*.PNG','*.GIF']:
        for path in glob.glob(os.path.join(base_dir, '**', ext), recursive=True):
            webp_path = os.path.splitext(path)[0] + '.webp'
            if os.path.exists(webp_path):
                continue
            try:
                with Image.open(path) as img:
                    if img.mode in ('RGBA', 'LA', 'PA'):
                        img = img.convert('RGBA')
                    elif img.mode == 'P':
                        img = img.convert('RGBA')
                    else:
                        img = img.convert('RGB')
                    img.save(webp_path, 'WEBP', quality=80)
                orig = os.path.getsize(path)
                new = os.path.getsize(webp_path)
                saving = orig - new
                saved_kb += saving
                print(f'  {path} ({orig//1024}KB -> {new//1024}KB, -{saving*100//orig if orig else 0}%)')
                count += 1
            except Exception as e:
                print(f'  ERROR {path}: {e}')
    return count, saved_kb

print('Converting paper thumbnails...')
c1, s1 = convert_dir('papers')
print(f'\nConverting profile images...')
c2, s2 = convert_dir('images')
total = c1 + c2
saved = (s1 + s2) // 1024
print(f'\nDone: {total} images converted, ~{saved}KB saved')
