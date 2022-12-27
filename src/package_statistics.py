import os
import gzip
from typing import List, Dict
from collections import defaultdict

import wget
from dotenv import load_dotenv

from .package_statistics_logging import load_logging


class DebianContentsFile:
    def __init__(self, arch):
        load_dotenv()
        self.logger = load_logging(__name__)    # setup logger for debian packages statistics

        self.arch = arch
        self.contents_index_file_name = f"Contents-{self.arch}.gz"
        self.contents_index_file_path = "./" + self.contents_index_file_name

    def _get_contents_index_url(self) -> str:
        mirror_url = ""
        if 'DEBIAN_MIRROR_URL' in os.environ:       # check existence of env variable
            mirror_url = os.environ['DEBIAN_MIRROR_URL']
            return mirror_url + self.contents_index_file_name

        mirror_url = "http://ftp.uk.debian.org/debian/dists/stable/main/"       #const mirror url used when no env
        return mirror_url + self.contents_index_file_name

    def download_arch_contents_index_file(self):
        # check if the contents index file does not exist in directory
        if not os.path.isfile(self.contents_index_file_path):
            content_index_download_url = self._get_contents_index_url()

            try:
                wget.download(content_index_download_url)
                self.logger.info(f"Contents file for {self.arch} downloaded...")

            except Exception as err:
                self.logger.error(f"Error downloading contents file for {self.arch}, link is"
                                  " incorrect or architecture not available for mirror...")
                self.logger.error(msg=err)

    # throws error sometimes due to a windows bug
    def delete_contents_index_file(self):
        os.remove(self.contents_index_file_path)


class DebPackageStatistics():

    def __init__(self, arch: str):
        #setup logger for debian packages statistics
        self.logger = load_logging(__name__)
        self.logger.info(f"Debian package statistics for {self.arch} started...")

    # only method to be called outside class
    def get_debian_package_statistics(self):
        self.__download_arch_contents_index_file()
        if os.path.isfile('./' + self.contents_index_file_name):
            contents_index_file_data = self.__read_contents_index_file()

            all_valid_package_name = self.__get_package_name(contents_index_file_data)

            all_valid_package_name_statistics= self.__get_package_statistics(all_valid_package_name)

            self.__order_package_statistics(all_valid_package_name_statistics)

            self.delete_contents_index_file()

    # fixes filenames with ' ' back together after they've been split
    # not used because it's unrequired for final solution but works
    @staticmethod
    def __concat_filename_with_space(split_filename: List[str]) -> str:
        filename = split_filename[0]
        if len(split_filename) > 1:      #if true, means filename had spaces in it
            for seperated_filename in split_filename[1::]:
                filename = ' ' + seperated_filename
        return filename

    @staticmethod
    def __split_packagae_names(package_list_name: List[str]) -> List[str]:
        # if true means multiple packages had same filename associated with them
        if ',' in package_list_name:
            return package_list_name.split(',')    # splits the packages name by ',' into a list
        return [package_list_name]

    def __read_contents_index_file(self) -> List[str]:
        content_index_arch_info = []

        self.logger.info("Started reading compressed index file")
        contents_index_arch_file =  gzip.open(self.contents_index_file_name, 'rt',encoding='utf-8')
        for file_line in contents_index_arch_file:
            content_index_info = {}
            split_line = file_line.split()  #split on space, package will always be last index pos

            #code below cleans the filename and package name info
            #content_index_info['filename'] = self.__concat_filename_with_space(split_line[0:-1])
            content_index_info['package'] = self.__split_packagae_names(split_line[-1])

            content_index_arch_info.extend(content_index_info['package'])

        self.logger.info("Obtained package name...")
        return content_index_arch_info

    """
    called in func below.
    from the repo, an instruction was given to ignore any package name that does not conform to the structure,
    the below function checks for the structure and removes any that does not conform to the structure,
    the idea is the full package name can be split ito at least two places by '/' anything less and it is invalide
    """
    def __validate_package_name(self, package_name_value:str ) -> str:
        if self.arch == 'source':
            return package_name_value
        package_name = package_name_value.split('/')
        if len(package_name) < 2:
            return ""
        return package_name[1]

    def __get_package_name(self, arch_content_index_package_name: List[str]) -> List[str]:
        self.logger.info("Validating package name...")

        valid_package_name = []
        for package_name in arch_content_index_package_name:
            checking = self.__validate_package_name(package_name)   #function is defined above
            valid_package_name.append(checking)
        return valid_package_name

    def __get_package_statistics(self, validated_package_name: List[str]) ->Dict[str, int]:
        self.logger.info("Getting statistics of debian packages")

        package_statistics = defaultdict(int)
        for package in validated_package_name:
            package_statistics[package] +=1
        return package_statistics

    # function orders and prints pacakge statistics with most files in descending order
    def __order_package_statistics(self, stats: Dict[str, int]):
        count = 0
        chars = 50
        stats_sorted = sorted(stats, key=stats.get, reverse=True)
        print("\n\n")
        for stat_key in stats_sorted:
            count += 1
            if count > 10:
                break
            len_package_name_chars = len(stat_key)
            fillers_to_print = chars - (len_package_name_chars)
            print(stat_key, stats[stat_key], sep="."*fillers_to_print)
