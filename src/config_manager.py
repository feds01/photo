def config_generation():
    file = open("E:\\Photo\\artifact\\config.yml", "w")
    file.write("""\nfolders:\n   good_folder_name:\n   - \"_Good\"\n   - \"_GOOD\"\n   - \"Good\"\n\
   - \"GOOD\"\n   - \"good\"\n   all_folder_name:\n   - \"_all\"\n   - \"_ALL\"\
  \n   - \"all\"\n   - \"All\"\n   - \"ALL\"\n   crt_folder_name:\n   - \"_DNG\"\n   - \"DNG\"\n
  - \"crt\"\n   - \"CRT\"\n   - \"Crt\"\n   - \"CRT\"\nblacklist:\n\
    enabled: true\n    location: \"artifact\\\\blacklist.txt\"\n\nfile_extensions:\n\
   crt:\n   - \".CR2\"\n   - \".dng\"\n   - \".TIF\"\n   good:\n   - \".jpg\"\n\
  \ndata:\n   index_data: \"temp\\\\photo_directories_data.txt\"\n   table_data: \"\
  temp\\\\table_data.txt\"\n   size_data: \"temp\\\\size_data.txt\"\n   removed_files_data:\
   \"temp\\\\removed_files_data.txt\"\n   completed_directories: \"artifact\\\\completed_directories.txt\"\
  \n""")
    file.close()

