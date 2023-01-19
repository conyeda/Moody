import audio_metadata
from os import listdir
from os.path import isfile
import pandas as pd
from pandas.api.types import is_numeric_dtype

def is_audio_with_meta(audio_path, meta_title, meta_df):
    audio_df =pd.DataFrame.from_dict(dict(audio_metadata.load(audio_path)['tags']))
    print(audio_df)
    for c in meta_title:
        if is_numeric_dtype(meta_df.dtypes[c]) and c in audio_df.columns:
            audio_df[c] = pd.to_numeric(audio_df[c])
    
    
    return not pd.merge(audio_df,meta_df, on=meta_title).empty
    
    
    

def get_audios_from_metadata(path, meta_title, meta_df):

    audios_and_dirs = listdir(path)
    audios = [
        file 
        for file in audios_and_dirs 
        if isfile('/'.join((path,file)))
        and is_audio_with_meta('/'.join((path,file)),meta_title,meta_df)
    ]
    return audios
    

def search_songs(path, album):
    """Search songs based on album name.

    Args:
        path (_type_): _description_
        album (_type_): _description_
    """
    audios_and_dirs = listdir(path)
    """audios = [
        audio 
        for audio in audios_and_dirs 
        if isfile('/'.join((path,audio)))
        and 'tags' in dict(audio_metadata.load('/'.join((path,audio))))
        and 'album' in dict(audio_metadata.load('/'.join((path,audio)))['tags'])
        and audio_metadata.load('/'.join((path,audio)))['tags']['album'] == album
    ]"""
    audios = []
    for audio in audios_and_dirs:
        try:
            audio_df =pd.DataFrame.from_dict(dict(audio_metadata.load('/'.join((path,audio)))['tags']))
            if 'album' in audio_df.columns and audio_df['album'][0] == album:
                audios.append(audio)
        except:
            pass
    
    return audios

if __name__ == '__main__':
    import pathlib

    PATH = str(pathlib.Path(__file__).parent.parent.parent.resolve())
    FILE_PATH = '/'.join((PATH, 'stimulus_set_1.csv'))
    DIR_PATH = '/'.join((PATH, 'masCanciones'))
    audios = search_songs(DIR_PATH,'Soundtrack360')
    audios.sort()
    print(audios)
    """audios_and_dirs = listdir(DIR_PATH)
    audios = [
        file 
        for file in audios_and_dirs 
        if isfile('/'.join((DIR_PATH,file)))
    ]
    for audio in audios:
        audio_df =pd.DataFrame.from_dict(dict(audio_metadata.load('/'.join((DIR_PATH,audio)))['tags']))
        if  'album' not in audio_df.columns or 'tracknumber' not in list(audio_df.columns):
            print(audio_df, audio)"""
