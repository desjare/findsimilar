#!/usr/bin/python3

import argparse
import hashlib
import os
import sys
import difflib

if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")

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

def find_similar(files, min_ratio, verbose):
	similar_tuple_list = []
	for f1 in files:
		for f2 in files:
			if f1 != f2:
				ratio = is_similar(get_filename_without_ext(f1),get_filename_without_ext(f2))
				if ratio >= min_ratio:
					if verbose is True:
						print("Similar %s <-> %s ratio:%f" % (os.path.basename(f1), os.path.basename(f2), ratio))

					similar_tuple_list.append((ratio, f1, f2))

	return similar_tuple_list

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="findsimilar")
	parser.add_argument("--folders", nargs="+", action="store", dest="folders", default=["."], help="directoris to scan", required=True)
	parser.add_argument("--exts", nargs="+", action="store", dest="exts", default=[".mp4", ".mkv", ".m4v", ".avi"], help="extensions to scan", required=False)
	parser.add_argument("--verbose", action="store_true", dest="verbose", default=False, help="verbose", required=False)
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

	similar_tuple_list = find_similar(files, args.min_ratio, args.verbose)

	for similar in similar_tuple_list:
		ratio, f1, f2 = similar

		print("Found ratio %f\n%s\n%s\n" % (ratio, f1, f2))



