from . import package_statistics_logging
from collections import defaultdict
from dotenv import load_dotenv
from typing import List, Dict
import gzip
import wget
import sys
import os

class DebPackageStatistics(object):

    def __init__(self, arch: str):
        #setup logger for debian packages statistics
        self.logger = package_statistics_logging.load_logging(__name__)

        self.arch = arch
        self.contents_index_file_name = f"Contents-{self.arch}.gz"
        load_dotenv()   # loads env variable from, but if not available uses a default link

        self.logger.info(f"Debian package statistics for {self.arch} started...")

    # only method to be called outside class
    def get_debian_package_statistics(self):
        self.__download_arch_contents_index_file()
        if os.path.isfile('./' + self.contents_index_file_name):
            contents_index_file_data = self.__read_contents_index_file()

            all_valid_package_name = self.__get_package_name(contents_index_file_data)

            all_valid_package_name_statistics = self.__get_package_statistics(all_valid_package_name)

            self.__order_package_statistics(all_valid_package_name_statistics)

            self.delete_contents_index_file()

    def __get_contents_index_package_url(self) -> str:
        mirror_url = os.environ['DEBIAN_MIRROR_URL']

        if not mirror_url:      # if mirror url can't be gotten from env variable
            mirror_url = "http://ftp.uk.debian.org/debian/dists/stable/main/"

        return mirror_url + self.contents_index_file_name

    def __download_arch_contents_index_file(self):
        file_path = "./"+ self.contents_index_file_name
        if not os.path.isfile(file_path):   # check if the contents index file does not exist in directory
            content_index_package_download_url = self.__get_contents_index_package_url()

            try:
                file_name = wget.download(content_index_package_download_url)
                self.contents_index_file_path = './'+file_name
                self.logger.info(f"Contents file for {self.arch} downloaded...")

            except Exception as err:
                self.logger.error(f"Error while downloading the contents file for {self.arch}, either the link is "
                                  " incorrect or architecture not available for this mirror...")

    # throws error sometimes due to a windows bug
    def delete_contents_index_file(self):
        os.remove(self.contents_index_file_path)

    # fixes filenames with ' ' back together after they've been split
    @classmethod
    def __concat_filename_with_space(cls, split_filename: List[str]) -> str:
        filename = split_filename[0]
        if len(split_filename) > 1:      #if true, means filename had spaces in it
            for seperated_filename in split_filename[1::]:
                filename = ' ' + seperated_filename
        return filename

    @classmethod
    def __split_packagae_names(cls, package_list_name: List[str]) -> List[str]:
        if ',' in package_list_name:    #if true means multiple packages had same filename associated with them
            return package_list_name.split(',')    # splits the packages name by ',' into a list
        return [package_list_name]

    def __read_contents_index_file(self) -> List[str]:
        content_index_arch_info = []

        self.logger.info("Started reading compressed index file")
        with gzip.open(self.contents_index_file_name, 'rt',encoding='utf-8') as contents_index_arch_file:
            for file_line in contents_index_arch_file:
                content_index_info = {}
                split_line = file_line.split()  #split on space, package name will always be at last index position

                #code below cleans the filename and package name info
                content_index_info['filename'] = self.__concat_filename_with_space(split_line[0:-1])
                content_index_info['package'] = self.__split_packagae_names(split_line[-1])

                for seperated_package_name in content_index_info['package']:
                    # list of all package name without the associated filename
                    content_index_arch_info.append(seperated_package_name)

                """ list of all package name without the associated filename
                    it is commented out because i realized we don't exactly need the associated filename to 
                    get the package statisitcs but if you want to see it, you can remove the comment below and 
                    comment out the append code above"""
                    #content_index_info.append([content_index['filename'], seperated_package_name])

        self.logger.info("Obtained package name...")
        return content_index_arch_info

    """
    called in func below.
    from the repo, an instruction was given to ignore any package name that does not conform to the structure,
    the below function checks for the structure and removes any that does not conform to the structure,
    the idea is the full package name can be split ito at least two places by '/' anything less and it is invalide
    """
    def __validate_package_name(self, package_name_value:str ) -> str:
        package_name = package_name_value.split('/')
        if len(package_name) < 2:
            return ""
        return package_name[1]

    def __get_package_name(self, arch_content_index_package_name: List[str]) -> List[str]:
        self.logger.info("Validating package name...")

        valid_package_name = []
        for package_name in arch_content_index_package_name:
            checking = self.__validate_package_name(package_name)   #function up called to append valid package name
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
        stats_sorted = sorted(stats, key=stats.get, reverse=True)
        print("\n\n")
        for stat_key in stats_sorted:
            count += 1
            if count > 10:
                break
            print("{}             {}".format(stat_key, stats[stat_key]))