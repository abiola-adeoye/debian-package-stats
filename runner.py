import sys
from src.package_statistics import DebPackageStatistics

# this is the function block that calls the CLI and package statistics class
def cil_debian_package_statistics():
    arch_input = sys.argv[1].lower()
    arch_list = ['all','amd64','arm64','armel','armhf',
                 'i386','mips64el','mipsel','ppc64el','s390x','source']
    if arch_input in arch_list:
        runner = DebPackageStatistics(arch_input)
        runner.get_debian_package_statistics()
    else:
        print("The available architectures for the default mirror link is.", end='\n\n')
        print(arch_list,end='\n\n')
        ask_new_link = input("Did you insert a new link?(y/n): ")
        if ask_new_link.lower() == "y":
            print("Note: architecture list for new link was not captured,"
                  " an error could occur downloading the file")
            runner = DebPackageStatistics(arch_input)
            runner.get_debian_package_statistics()
        else:
            print("Insert new link or input available architecture")

cil_debian_package_statistics()