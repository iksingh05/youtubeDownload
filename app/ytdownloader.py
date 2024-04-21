import os, re, sys, logging
from pytube import Playlist, YouTube

logger = logging.getLogger(__name__)

class ytdownloader:
    def downloadytvideos(self,param_folder_path, param_url_input,param_excludedVideos,param_includedVideos):
        logger.info('downloadytvideos function is executed.')
        try:
            os.chmod(param_folder_path,0o755)
            # sys.stdout.write("getcwd->"+ os.getcwd())
            # sys.stdout.write("Check Folder") 
            if not os.path.exists(param_folder_path):
                # sys.stdout.write("Folder not exist")    
                os.makedirs(param_folder_path)
        except Exception as e:
            sys.stdout.write("Exception param_folder_path -->" + e)

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

        if "playlist" in param_url_input:
            playlist = Playlist(param_url_input)
        elif "," in param_url_input:
            playlist=param_url_input.split(',')
        else:
            playlist = [param_url_input]
        
        i=0
        downloadvideo = []
            
        for urlInPlayList in playlist:
            i +=1
            if i in excludedVideos_list:
                continue
            if i in includedVideos_list or not includedVideos_list:
                downloadvideo.append((i, urlInPlayList))
        
        for index,urlInPlayList in downloadvideo:
            self.downloadvideo(folder_path=param_folder_path, url=urlInPlayList,number=index)
            sys.stdout.write(str(index) + '-' + str(urlInPlayList))
 
    def downloadvideo(self,folder_path, url,number=1):
        yt = YouTube(url)
        
        if not yt:
            raise ValueError("Invalid URL provided")
        
        title = str(number)+ str(" - ") +re.sub(r'\W+', ' ', yt.title)
        filename = os.path.join(folder_path, f"{title}.mp4")
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
                sys.stdout.write(filename)
                sys.stdout.write('\n')
                high_res_vid = yt.streams.get_highest_resolution()
                yt.register_on_progress_callback(lambda chunk, file_handle, bytes_remaining: self.on_progress(chunk, file_handle, bytes_remaining, high_res_vid.filesize))
                high_res_vid.download(filename=filename)
                sys.stdout.write('\n')
                sys.stdout.write("downloaded successfully")  
            else:
                sys.stdout.write("title-" + title + "- Already downloaded!")
        except Exception as e:
            raise e

if __name__ == '__main__':
    ytobj=ytdownloader()
    url_list = 'https://youtu.be/7Ro2hjMy-xQ'
    folder_path = r'D:\IT Study Material\GoogleVertexAI\Vector Search and Embeddings'  # Use a raw string or double backslashes
    excludedVideos =''
    includedvideos = ''
    ytobj.downloadytvideos(folder_path, url_list,excludedVideos,includedvideos)
