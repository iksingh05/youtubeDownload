import os
from flask import Flask, render_template, request, jsonify
# from applicationinsights import TelemetryClient
from .ytdownloader import ytdownloader
from .logger import configure_logging
from flask_cors import CORS

# Configure logging
configure_logging()

# Instantiate the ytdownloader class
yt_downloader = ytdownloader()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# app_insights_key = 'd204baed-6660-4a5a-ad9e-e4faa99df561'
# app_insights_client = TelemetryClient(app_insights_key)


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
                app.logger.info('Index route accessed.')
                yt_downloader.downloadytvideos(folder_path, url,excludedvideolist,includedVideoslist)
                return jsonify({'success': 'Video Downloaded successfully'}), 200
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
            except Exception as e:
                return jsonify({'error': 'An error occurred: ' + str(e)}), 500

    return render_template('index.html')
@app.errorhandler(500)
def internal_server_error(error):
    app_insights_client.track_exception()
    return 'Internal Server Error', 500

if __name__ == '__main__':
    app.run(debug=True)
