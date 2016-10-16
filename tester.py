import os
chosen_path = ("C:\\Users\\Alex\\PycharmProjects")

for root, dirs, files in os.walk(chosen_path):
    if not dirs:

        print('%s is a leaf' % root)
