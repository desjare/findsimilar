#!/usr/bin/python3

import argparse
import hashlib
import os
import sys
import difflib

if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")

default_ext = [".mp4", ".mkv", ".m4v", ".avi", ".jpg", ".jpeg", ".mp3", ".flac"]

def list_files_in_folder(folder, exts, verbose):
	l = []
	for root, subdirs, files in os.walk(folder):
		if verbose is True:
			print('Scanning %s...' % root)
		for filename in files:
			# Get the path to the file
			name, ext = os.path.splitext(filename)
			if ext != "":
				if ext.lower() in exts:
					path = os.path.join(root, filename)
					l.append(path)
				elif verbose is True:
					print("Ignoring ext: %s" % (ext))
	return l

def is_similar(a, b):
	return difflib.SequenceMatcher(None, a, b).ratio()

def get_filename_without_ext(filename):
	name, ext = os.path.splitext(filename)
	return os.path.basename(name)

def hash_file(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def find_similar(files, min_ratio, compare, verbose):
	similar_tuple_list = []
	similar_set = set()

	for f1 in files:
		for f2 in files:
			name1, ext1 = os.path.splitext(f1)
			name2, ext2 = os.path.splitext(f2)

			if f1 != f2 and not f1+f2 in similar_set:
				ratio = is_similar(get_filename_without_ext(f1),get_filename_without_ext(f2))
				if ratio >= min_ratio:
					if verbose is True:
						print("Similar %s <-> %s ratio:%f" % (os.path.basename(f1), os.path.basename(f2), ratio))

					same = False

					if compare is True and ratio == 1.0 and ext1.lower() == ext2.lower():
						
						if verbose is True:
							print("Comparing files %s <-> %s" % (os.path.basename(f1), os.path.basename(f2)))

						hash1 = hash_file(f1)
						hash2 = hash_file(f2)

						if hash1 == hash2:
							same = True

					similar_set.add(f1+f2)
					similar_tuple_list.append((ratio, f1, f2, same))

	return similar_tuple_list

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="findsimilar")
	parser.add_argument("--folders", nargs="+", action="store", dest="folders", default=["."], help="directoris to scan", required=True)
	parser.add_argument("--exts", nargs="+", action="store", dest="exts", default=default_ext, help="extensions to scan", required=False)
	parser.add_argument("--verbose", action="store_true", dest="verbose", default=False, help="verbose", required=False)
	parser.add_argument("--compare", action="store_true", dest="compare", default=False, help="compare similar files md5", required=False)
	parser.add_argument("--minratio", action="store", type=float, dest="min_ratio", default=0.9, help="minimum matching ratio", required=False)
	args = parser.parse_args()
	files = []

	# Iterate the folders given
	for folder in args.folders:

		if args.verbose is True:
			print("Scanning folder: %s" % (folder))

		if os.path.exists(folder):
			files += list_files_in_folder(folder, args.exts, args.verbose)
		else:
			print('%s is not a valid path, please verify' % (folder))
			sys.exit(1)

	similar_tuple_list = find_similar(files, args.min_ratio, args.compare, args.verbose)

	for similar in similar_tuple_list:
		strings = [str(item) for item in similar]
		print(";".join(strings))




