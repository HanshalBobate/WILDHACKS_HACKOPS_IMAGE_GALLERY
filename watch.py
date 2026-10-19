"""
WildID — Real-Time Directory Watcher
Continuously monitors images/ and blog.txt. Automatically synchronizes whenever a change occurs!
Usage: python watch.py
"""

import os, time
from sync import sync_images, sync_blog

base_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(base_dir, 'images')
blog_txt_path = os.path.join(base_dir, 'blog.txt')

def get_snapshot():
    # snapshot of images
    img_files = {}
    if os.path.exists(images_dir):
        for f in os.listdir(images_dir):
            p = os.path.join(images_dir, f)
            if os.path.isfile(p):
                try:
                    img_files[f] = os.path.getmtime(p)
                except OSError:
                    pass
    # snapshot of blog.txt
    blog_mtime = 0
    if os.path.exists(blog_txt_path):
        try:
            blog_mtime = os.path.getmtime(blog_txt_path)
        except OSError:
            pass
    return img_files, blog_mtime

if __name__ == '__main__':
    print('===================================================================')
    print('  WildID Real-Time Watcher Active')
    print('  Monitoring images/ and blog.txt for live changes...')
    print('  Press Ctrl+C to stop.')
    print('===================================================================')

    last_imgs, last_blog = get_snapshot()

    try:
        while True:
            time.sleep(2)
            cur_imgs, cur_blog = get_snapshot()

            imgs_changed = (cur_imgs != last_imgs)
            blog_changed = (cur_blog != last_blog)

            if imgs_changed:
                print(f'\n[!] Detected image changes in images/ ({len(cur_imgs)} files). Syncing...')
                sync_images()
                last_imgs = cur_imgs

            if blog_changed:
                print(f'\n[!] Detected modification in blog.txt. Rebuilding blog.html...')
                sync_blog()
                last_blog = cur_blog

    except KeyboardInterrupt:
        print('\n[*] Watcher stopped.')
