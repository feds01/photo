from src.utils import *
from src.data import Table

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


def fancy_tree_display(roots, values):
    full_string, tree_symbol = "", "|_ "
    max_root = Utility().get_largest_element(roots)
    for i in range(len(roots)):
        align = ""
        if len(roots[i]) < 5:
            align = " " * (max_root - len(roots[i]))
        full_string += tree_symbol + roots[i] + align + ": " + str(values[i]) + "\n"
    return full_string


def table_instance_display(instance_data):
    instance_leaves = {}
    file_count = 0
    for directory in instance_data[1]:
        instance_leaves.update({os.path.basename(directory): Directory(directory).index_directory(count=True, file=True)})
    instance_data.pop(1)
    print("More detail about the photo directory - '" + os.path.basename(instance_data[0]) + "' :", space(1))
    print("Full directory path: ", instance_data[0])
    for i in range(1, 5):
        file_count += instance_data[i]
    print("Total files:", file_count)
    print(fancy_tree_display(list(instance_leaves.keys()), list(instance_leaves.values())),)
    print("Total directory size: " + str(instance_data[-1][0]) + " " + instance_data[-1][1])


def table_selector(max_id, prefix="~$ "):
    print("Enter the ID of the directory or enter the path of the directory to continue: ")
    dirs = []
    for i in range(1, max_id):
        dirs.append(Table().load_instance_by_id(i)[0])
    while True:
        scan_dir_input = input(prefix)
        try:
            scan_dir_input = int(scan_dir_input)
            if max_id < scan_dir_input or scan_dir_input < 0:
                print("The entered ID is too high or too low.")
            else:
                return safe_mode_selector(scan_dir_input, "path")
        except ValueError:
            try:
                if scan_dir_input[0] is ":":
                    if scan_dir_input[1:] == "paths":
                        for path in dirs:
                            print(path)
                    continue
            except IndexError:
                pass
            if scan_dir_input.isspace() or scan_dir_input == "":
                continue
            if scan_dir_input not in dirs:
                print("Entered directory path not present.")
            else:
                return safe_mode_selector(scan_dir_input, "path")


def safe_mode_selector(directory, pid):
    if pid == "path":
        pass
    else:
        directory = Table().load_instance_by_id(directory)
    while True:
        safe_scan_input = input("Scan the directory in safe mode [Y/n]? ").lower()
        if safe_scan_input == "y":
            return [directory, "--safe"]
        if safe_scan_input == "n":
            return [directory]


def safe_mode_file_deletion(files):
    crt_files = files.values()
    delete_list = []
    for file in files:
        print(file)
    for file in crt_files:
        confirm_delete_input = input("Are you sure you want to delete '" + file + "' [Y/n]?").lower()
        if confirm_delete_input == "y":
            delete_list.append(file)
        if confirm_delete_input == "n":
            print(files.fromkeys(files))


safe_mode_file_deletion({'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1726.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1726.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1755.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1755.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1731.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1731.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1742.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1742.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1762.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1762.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1733.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1733.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1761.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1761.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1769.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1769.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1796.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1796.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1789.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1789.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1795.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1795.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1804.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1804.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1786.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1786.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1800.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1800.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1794.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1794.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1748.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1748.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1734.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1734.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1746.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1746.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1767.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1767.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1744.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1744.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1785.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1785.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1768.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1768.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1771.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1771.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1745.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1745.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1753.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1753.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1803.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1803.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1775.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1775.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1781.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1781.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1750.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1750.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1774.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1774.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1792.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1792.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1760.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1760.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1756.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1756.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1747.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1747.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1743.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1743.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1757.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1757.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1759.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1759.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1776.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1776.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1779.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1779.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1787.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1787.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1729.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1729.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1778.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1778.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1739.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1739.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1764.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1764.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1777.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1777.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1720.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1720.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1727.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1727.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1802.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1802.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1782.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1782.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1797.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1797.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1754.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1754.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1793.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1793.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1799.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1799.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1738.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1738.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1798.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1798.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1740.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1740.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1783.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1783.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1730.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1730.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1758.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1758.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1784.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1784.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1780.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1780.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1763.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1763.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1765.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1765.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1728.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1728.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1766.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1766.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1772.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1772.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1788.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1788.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1770.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1770.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1790.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1790.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1773.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1773.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1749.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1749.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1752.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1752.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1791.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1791.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1723.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1723.dng', 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1801.JPG': 'E:\\Files\\Ana Felix Snow Queen\\crt\\IMG_1801.dng'})