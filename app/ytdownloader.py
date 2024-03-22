import os, re, sys, logging
from pytube import Playlist, YouTube

logger = logging.getLogger(__name__)

class ytdownloader:
    def downloadytvideos(self,param_folder_path, param_url_input,param_excludedVideos,param_includedVideos):
        
        logger.info('downloadytvideos function is executed.')
        
        if param_includedVideos:
            if '-' in param_includedVideos:
                startIn, endIn = map(int, param_includedVideos.split('-'))
                includedVideos_list = list(range(startIn, endIn + 1))
            else:
                includedVideos_list = [int(x) for x in param_includedVideos.split(',')]
        else:
            includedVideos_list = []
        
        if param_excludedVideos:
            if '-' in param_excludedVideos:
                startEx, endEx = map(int, param_excludedVideos.split('-'))
                excludedVideos_list = list(range(startEx, endEx + 1))
            else:
                excludedVideos_list =  [int(x) for x in param_excludedVideos.split(',')]
        else:
            excludedVideos_list = []

        sys.stdout.write(param_folder_path)
        sys.stdout.write(param_url_input)
        sys.stdout.write(param_excludedVideos)
        sys.stdout.write(param_includedVideos)

        # for url in url_list:
        if "playlist" in param_url_input:
            playlist = Playlist(param_url_input)
            i=0
            downloadvideo = []
            #create download video list
                
            for urlInPlayList in playlist.video_urls:
                i +=1
                if i in excludedVideos_list:
                    continue
                if i in includedVideos_list or not includedVideos_list:
                    downloadvideo.append((i, urlInPlayList))
            
            sys.stdout.write(str(downloadvideo))

            os.system('cls')  # Clear the screen then download

            for index,urlInPlayList in downloadvideo:
                self.downloadvideo(folder_path=param_folder_path, url=urlInPlayList,number=index)
                # sys.stdout.write(str(index) + '-' + str(urlInPlayList))
                
            # os.system('cls')  # Clear the screen after processing a playlist
        else:
            self.downloadvideo(param_folder_path, param_url_input)

    def downloadvideo(self,folder_path, url,number=1):
        yt = YouTube(url)
        
        if not yt:
            raise ValueError("Invalid URL provided")
        
        title = str(number)+ str(" - ") +re.sub(r'\W+', ' ', yt.title)
        filename = os.path.join(folder_path, f"{title}.mp4")
        sys.stdout.write(filename)
        self.videodownload(yt,filename,title)
        

    def on_progress(self,chunk, file_handle, bytes_remaining, filesize):
        current = ((filesize - bytes_remaining) / filesize)
        percent = ('{0:.1f}').format(current * 100)
        progress = int(50 * current)
        status = '█' * progress + '-' * (50 - progress)
        sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
        sys.stdout.flush()

    def videodownload(self,yt,filename,title):
        try:
            if not os.path.exists(filename):
                high_res_vid = yt.streams.get_highest_resolution()
                yt.register_on_progress_callback(lambda chunk, file_handle, bytes_remaining: self.on_progress(chunk, file_handle, bytes_remaining, high_res_vid.filesize))
                high_res_vid.download(filename=filename)
            else:
                print(title ,"-Already downloaded!")
        except Exception as e:
            raise e

if __name__ == '__main__':
    ytobj=ytdownloader()
    url_list = 'https://www.youtube.com/playlist?list=PLFLyCYS0pGW4C1oqM4PPfvlMrcGqjrGq4'
    folder_path = r'F:\Study Material\Class 6\Maths'  # Use a raw string or double backslashes
    excludedVideos ='1'
    includedvideos = '16'
    ytobj.downloadytvideos(folder_path, url_list,excludedVideos,includedvideos)
