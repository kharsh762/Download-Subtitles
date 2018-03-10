import os
import hashlib
import requests
import sys
import io

def get_hash(fname):
    readsize = 64*1024
    with open(fname,'rb') as f:
        data = f.read(readsize)
        f.seek(-readsize,os.SEEK_END)
        data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

def download(header,hash_value,language='en'):
    try:
        url = 'http://api.thesubdb.com/?action=download&hash='+hash_value+'&language='+language
        r = requests.get(url,headers=header)
        if r.status_code==404:
            print('Subtitles are not available!')
        elif r.status_code==400:
            print('Check your request query!')
        else:
            return r.text
    except:
        print('Check your internet connection!')
    return ''                

if __name__=='__main__':
    header = {'User-Agent':'SubDB/1.0 (harsh/1.0; http://github.com/kharsh762/Download-Subtitles)'}
    path = sys.argv[1:]
    path = ' '.join(path)
    for fname in os.listdir(path):
        if fname.endswith(('.mp4','.avi','.mkv')):
            file = os.path.join(path,fname)
            hash_value = get_hash(file)
            subtitle = download(header,hash_value)
            if(len(subtitle)>0):
                fname = fname.split('.')
                fname = '.'.join(fname[0:len(fname)-1]) + '.srt'
                with io.open(os.path.join(path,fname),'w',encoding='UTF-8') as f:
                    f.write(subtitle)
                print("Subtitle downloaded successfully!")             