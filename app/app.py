import os
from flask import Flask, render_template, request, jsonify
from .ytdownloader import ytdownloader


# Instantiate the ytdownloader class
yt_downloader = ytdownloader()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        folder_path = request.form.get('folderPath')
        url = request.form.get('url')
        excludedvideolist = request.form.get('excludedVideos')
        includedVideoslist =request.form.get('includedVideos')
        if not folder_path.strip():
            return jsonify({'error': 'Please enter folder path', 'field': 'folderPath'}), 400
        elif not url.strip():
            return jsonify({'error': 'Please enter URL', 'field': 'url'}), 400
        else:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            try:
                # Call the function from ytdownloader.py
                yt_downloader.downloadytvideos(folder_path, url,excludedvideolist,includedVideoslist)
                return jsonify({'success': 'Video Downloaded successfully'}), 200
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
            except Exception as e:
                return jsonify({'error': 'An error occurred: ' + str(e)}), 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)