from flask import Flask, request, render_template, send_file
import yt_dlp
import os
from playwright.sync_api import sync_playwright
import requests

app = Flask(__name__)

def download_instagram_reel(url, filename):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)

            # Wait for the page to load and find the video URL
            page.wait_for_selector('video')
            video_url = page.query_selector('video').get_attribute('src')

            # Download the video
            if video_url:
                response = page.request.get(video_url)
                with open(filename, 'wb') as f:
                    f.write(response.body())
                return filename
            else:
                return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    quality = request.form['quality']

    if "instagram.com" in url:
        try:
            file_path = os.path.join('downloads', 'instagram_reel.mp4')
            result = download_instagram_reel(url, file_path)
            if result:
                return send_file(result, as_attachment=True)
            else:
                return "Instagram Reel not found or download failed."

        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    elif "youtube.com" in url or "youtu.be" in url:
        # YouTube URL handling with yt-dlp
        try:
            ydl_opts = {
                'format': 'best',  # Default to best available format
                'outtmpl': 'downloads/%(title)s.%(ext)s',
            }

            if quality == "high":
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
            elif quality == "medium":
                ydl_opts['format'] = 'best[height<=720]'
            elif quality == "low":
                ydl_opts['format'] = 'best[height<=480]'

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    video_title = ydl.prepare_filename(info_dict)
                    return send_file(video_title, as_attachment=True)
            except yt_dlp.utils.DownloadError:
                ydl_opts['format'] = 'best'
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    video_title = ydl.prepare_filename(info_dict)
                    return send_file(video_title, as_attachment=True)
        
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    else:
        return "Invalid URL or platform not supported."

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)





# from flask import Flask, request, render_template, send_file
# import os
# from playwright.sync_api import sync_playwright

# app = Flask(__name__)

def download_instagram_reel(url, filename):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)

            # Wait for the page to load and find the video URL
            page.wait_for_selector('video')
            video_url = page.query_selector('video').get_attribute('src')

            # Download the video
            if video_url:
                response = page.request.get(video_url)
                with open(filename, 'wb') as f:
                    f.write(response.body())
                return filename
            else:
                return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/download', methods=['POST'])
# def download():
#     url = request.form['url']
#     quality = request.form['quality']

#     if "instagram.com" in url:
#         try:
#             file_path = os.path.join('downloads', 'instagram_reel.mp4')
#             result = download_instagram_reel(url, file_path)
#             if result:
#                 return send_file(result, as_attachment=True)
#             else:
#                 return "Instagram Reel not found or download failed."

#         except Exception as e:
#             return f"An error occurred: {str(e)}"
    
#     elif "youtube.com" in url or "youtu.be" in url:
#         # Handle YouTube download here (already working perfectly)
#         pass

#     else:
#         return "Invalid URL or platform not supported."

# if __name__ == '__main__':
#     if not os.path.exists('downloads'):
#         os.makedirs('downloads')
#     app.run(debug=True)
