from src.package_statistics import DebPackage



runner = DebPackage("amd64")
runner.download_arch_contents_index_file()
p = runner.read_contents_index_file_to_df()

#sp= DebPackage.split_contents_index_df_columns(p)
print(p)