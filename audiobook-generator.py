#!/usr/bin/env python3

"""
-------------------------------------------------------------------------------
Author        : Florian Hild
Created       : 2024-01-13
Python version: 3.x
Description   :
-------------------------------------------------------------------------------
"""

__VERSION__ = '1.0.0'

import sys
import os
import argparse
import logging as log
import shutil
import eyed3

def check_directory(path: str):
    """
    Ensure the path is a valid directory
    -------------------

    Arguments:
      path: str

    Returns:
      path: str

    Example:
      check_directory("/tmp")
    """

    if os.path.isdir(path):
        return path
    else:
        log.critical('Directory \"%s\" not found.', path)
        sys.exit(1)





def check_file(path: str):
    """
    Ensure the path is a valid file
    -------------------

    Arguments:
      path: str

    Returns:
      path: str

    Example:
      check_file("/etc/hosts")
    """
    if os.path.isfile(path):
        return path
    else:
        log.critical('File \"%s\" not found.', path)
        sys.exit(1)





def main():
    """
    Main function
    -------------------
    """

     # Logger configuration
    log.basicConfig( format='[%(levelname)8s] %(message)s' )

    # Parameter configuration
    parser = argparse.ArgumentParser(
        description='Order audiobook and add ID3 tags.',
        prog='audiobook-genrator',
        usage='%(prog)s [options]',
        add_help=False,
    )

    parser.add_argument(
        '-V', '--version',
        help="Print version number and exit.",
        action='version',
        version=f"%(prog)s version {__VERSION__}",
    )

    parser.add_argument(
        '-h', '--help',
        help='Print a short help page describing the options available and exit.',
        action='help',
    )

    parser.add_argument(
        '-v', '--verbose',
        help="""Verbose mode. Multiple -v options increase the verbosity.
             The maximum is 3.""",
        action='count',
        default=0,
    )

    parser.add_argument(
        '-i', '--input',
        help='Path to audiobook source',
        required=True,
        type=check_directory
    )

    parser.add_argument(
        '-o', '--output',
        help='Path to audiobook destination',
        required=True,
        type=check_directory
    )

    parser.add_argument(
        '-p', '--prefix',
        help='Filename prefix. (e.g. Kluftinger_12_Affenhitze)',
        required=True
    )

    parser.add_argument(
        '--author',
        help='Author name',
        required=True
    )

    parser.add_argument(
        '--album',
        help='Album name',
        required=True
    )

    parser.add_argument(
        "-y", "--year",
        help="Publishing year",
        required=True,
        type=int
    )

    parser.add_argument(
        "--series",
        help="Series Name",
        default=None
    )

    parser.add_argument(
        "--asin",
        help="Amazon / Audible Standard Identification Number (e.g. B09X7FS3ZC)",
        default=None
    )

    parser.add_argument(
        "--genre",
        help="Genre",
        default="Audiobook"
    )

    args = parser.parse_args()

    parser.add_argument(
        '--cover',
        help='Path to audiobook cover (image/jpeg). Default: cover.jpg',
        default=os.path.join(args.input, "cover.jpg")
    )

    args = parser.parse_args()

    if args.verbose == 0:
        log.getLogger().setLevel(log.WARN)
    elif args.verbose == 1:
        log.getLogger().setLevel(log.INFO)
    else:
        log.getLogger().setLevel(log.DEBUG)

    copy_and_rename_files( args.input, args.output, args.prefix )

    print("Set ID3 tags to destination files")
    mp3_files = [f for f in os.listdir(args.output) if f.lower().endswith(".mp3")]
    mp3_files.sort()
    mp3_files = [os.path.join(args.output, f) for f in mp3_files]

    for index, file in enumerate(mp3_files, start=1):
        set_id3_tags(file, args.author, args.album, args.year, index, len(mp3_files),
                    args.cover, args.series, args.asin, args.genre)

def copy_and_rename_files(input_folder: str, output_folder: str, title_prefix: str):
    """
    Copy and rename files
    -------------------

    Arguments:
      input_folder: str
      output_folder: str
      title_prefix: str

    Returns:
      None

    Example:
      copy_and_rename_files("/tmp/audiobook", "/tmp/audiobook_changed", "book_test")
    """

    print("Get all \"*.mp3\" files in subfolder")
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initialize a counter for numbering the files
    file_counter = 1

    # Iterate through subfolders
    for root, _, files in os.walk(input_folder):
        files.sort()

        print("Copy files to destination and rename files")
        log.info("Source path: \"%s\"", input_folder)
        log.info("Destination path: \"%s\"", output_folder)
        for file in files:
            if file.lower().endswith(".mp3"):
                # Cut the last underscore from the new filename
                title_prefix = title_prefix[:-1] if title_prefix.endswith("_") else title_prefix

                # Build the new file name with a numbered prefix
                new_filename = f"{title_prefix}_{file_counter:03d}.mp3"

                # Replace spaces with underscores in the new filename
                new_filename = new_filename.replace(" ", "_")

                # Replace German umlauts with English counterparts
                new_filename = replace_german_chars(new_filename)


                log.info("Rename \"%s\" to \"%s\"",file ,new_filename)

                # Construct the full paths for the source and destination
                source_path = os.path.join(root, file)
                destination_path = os.path.join(output_folder, new_filename)

                # Rename and copy the file
                shutil.copy(source_path, destination_path)

                # Increment the file counter
                file_counter += 1

def replace_german_chars(filename: str):
    """
    Replace german characters
    -------------------

    Arguments:
      filename: str

    Returns:
      filename: str

    Example:
      replace_german_chars("Völkle")
    """
    # Define a translation dictionary for German umlauts
    translation_dict = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue', 'ß': 'ss'}

    # Apply the translation to the filename
    for german_char, replacement in translation_dict.items():
        filename = filename.replace(german_char, replacement)

    return filename


def set_id3_tags(file_path: str,
                author: str,
                album: str,
                year: int,
                track_number: int,
                total_tack_number: int,
                image_path: str=None,
                series=None,
                asin: str=None,
                genre: str="Audiobook"):
    """
    Set ID3 tags
    -------------------

    Arguments:
      file_path: str,
      author: str,
      album: str,
      year: int,
      track_number: int,
      total_tack_number: int,
      image_path: str=None,
      series=None,
      asin: str=None,
      genre: str="Audiobook"

    Returns:
      None

    Example:
      set_id3_tags("/tmp/audiobook/file01.mp3", "Auth", "Album", 2021, 1, 10)
    """
    log.info("")
    log.info("Processing file: \"%s\"", file_path)
    filename = os.path.splitext(os.path.basename(file_path))[0]

    try:
        audiofile = eyed3.load(file_path)

        if not audiofile:
            log.error("File type unknown: \"%s\"", file_path)
            return
    except IOError as ioe:
        log.fatal("IOError: %s", ioe)
        sys.exit(1)

    if not audiofile.tag:
        log.info("No ID3 tag found")
        log.info("Create ID3 frame")
        audiofile.initTag(version=(2, 4, 0))

    # Clean all existing ID3 tags
    log.info("Cleanup current ID3 tags")
    audiofile.tag.clear()

    # Set ID3 tags
    log.info("Set ID3 tags")

    log.info("Set %-9s to \"%s\"", "artist", author)
    audiofile.tag.artist = author

    log.info("Set %-9s to \"%s\"", "title", filename)
    audiofile.tag.title = filename

    log.info("Set %-9s to \"%s\"", "album", album)
    audiofile.tag.album = album

    log.info("Set %-9s to \"%s\"", "year", year)
    audiofile.tag.date = year
    audiofile.tag.recording_date = year

    log.info("Set %-9s to \"%s\"", "series", series)
    audiofile.tag.series = series

    log.info("Set %-9s to \"%s\"", "asin", asin)
    audiofile.tag.asin = asin

    log.info("Set %-9s to \"%s\"", "genre", genre)
    audiofile.tag.genre = genre

    log.info("Set %-9s to \"%s\"", "track_num", str(track_number) + "/" + str(total_tack_number))
    audiofile.tag.track_num = (track_number, total_tack_number)

    if image_path and os.path.isfile(image_path):
        log.info("Set %-9s to \"%s\"", "images", image_path)
        # Set the cover in the ID3 tag
        with open(image_path, 'rb') as image_file:
            cover_bytes = image_file.read()
            audiofile.tag.images.set(3, cover_bytes, 'image/jpeg')

        # Copy cover to new folder
        log.info("Copy cover image to new destination")
        shutil.copy(image_path, os.path.dirname(file_path))

    # Save changes
    audiofile.tag.save(version=(1, 1, 0))
    audiofile.tag.save(version=(2, 4, 0))

if __name__ == '__main__':
    main()
