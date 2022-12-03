import wget
from dotenv import load_dotenv
import gzip
import os

class DebPackage(object):

    def __init__(self, arch: str):
        self.arch = arch
        self.contents_index_file_path = ""
        load_dotenv()


    def get_contents_index_url(self):
        mirror_url = os.environ['DEBIAN_MIRROR_URL']
        content_index_url_addon = f"Contents-{self.arch}.gz"
        return mirror_url+content_index_url_addon

    def download_arch_contents_index_file(self):
        content_index_download_url = self.get_contents_index_url()
        try:
            file_name = wget.download(content_index_download_url)
            self.contents_index_file_path = './'+file_name
        except Exception as error:
            print("There was a problem with downloading this file", error)

    # needs fixing
    def delete_contents_index_file(self):
        os.remove(self.contents_index_file_path)

    @staticmethod
    def concat_filename_with_space(cls):
        pass

    @staticmethod
    def split_packagae_list(package_list):
        pass

    def read_contents_index_file_to_df(self):
        with gzip.open(self.contents_index_file_path) as contents_index_file:
            for i in contents_index_file:
                contents_index_df = i
                contents_index_df_1 = contents_index_df.split()
            #contents_index_df = pd.read_fwf(contents_index_file,width=5, header=None)
                break
        return contents_index_df_1



