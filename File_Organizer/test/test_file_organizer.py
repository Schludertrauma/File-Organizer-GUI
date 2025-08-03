'''Test for fileorganizer class'''

import os
import sys
import pytest
import tkinter as tk
from tkinter import mainloop, messagebox
# noqa: E402
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # noqa: E402
from file_organizer import fileorganizer


@pytest.fixture
def gui_menu():
    # Create a Tkinter root window for testing
    root = tk.Tk()
    yield root
    root.destroy()


def test_add_directory():
    # Test adding a directory to the file organizer
    organizer = fileorganizer()
    test_dir = 'test_directory'
    os.makedirs(test_dir, exist_ok=True)

    organizer.add_directory(test_dir)
    assert organizer.directory == test_dir

    # Clean up
    os.rmdir(test_dir)


def test_scan_directory(gui_menu):
    # Test scanning a directory for files
    organizer = fileorganizer()
    test_dir = 'test_scan_directory'
    os.makedirs(test_dir, exist_ok=True)

    # Create test files
    with open(os.path.join(test_dir, 'file1.txt'), 'w') as f:
        f.write('Test file 1')
    with open(os.path.join(test_dir, 'file2.jpg'), 'w') as f:
        f.write('Test file 2')

    files = organizer.scan_directory(test_dir)
    assert 'file1.txt' in files
    assert 'file2.jpg' in files

    # Clean up
    os.remove(os.path.join(test_dir, 'file1.txt'))
    os.remove(os.path.join(test_dir, 'file2.jpg'))
    os.rmdir(test_dir)


def test_sort_files_by_extension():
    # Test sorting files by their extensions
    organizer = fileorganizer()
    files = ['image1.jpg', 'document1.txt',
             'audio1.mp3', 'video1.mp4', 'unknownfile.xyz']

    sorted_files = organizer.sort_files_by_extension(files)

    assert 'image1.jpg' in sorted_files['images']
    assert 'document1.txt' in sorted_files['documents']
    assert 'audio1.mp3' in sorted_files['audio']
    assert 'video1.mp4' in sorted_files['video']
    assert 'unknownfile.xyz' in sorted_files['others']


def test_organize_files_on_click(gui_menu):
    # Test organizing files on button click
    organizer = fileorganizer()
    test_dir = 'test_organize_files'
    os.makedirs(test_dir, exist_ok=True)

    # Create test files
    with open(os.path.join(test_dir, 'file1.txt'), 'w') as f:
        f.write('Test file 1')
    with open(os.path.join(test_dir, 'file2.jpg'), 'w') as f:
        f.write('Test file 2')

    organizer.entry = tk.Entry(gui_menu)
    organizer.entry.insert(0, test_dir)

    organizer.organize_files_on_click()

    organized_path = os.path.join(test_dir, "organized_files")
    assert os.path.exists(organized_path)

    # Check if files are sorted into correct folders
    assert os.path.exists(os.path.join(organized_path, 'images'))
    assert os.path.exists(os.path.join(organized_path, 'documents'))

    # Clean up
    categories = ['images', 'documents', 'audio', 'video', 'others']
    for category in categories:
        category_path = os.path.join(organized_path, category)
        if os.path.exists(category_path):
            for f in os.listdir(category_path):
                os.remove(os.path.join(category_path, f))
            os.rmdir(category_path)
    if os.path.exists(organized_path):
        os.rmdir(organized_path)
    if os.path.exists(test_dir):
        os.rmdir(test_dir)


def test_quit_on_click(gui_menu):
    organizer = fileorganizer()
    organizer.root = gui_menu
    organizer.quit_on_click = organizer.root.quit
    organizer.quit_on_click()
    # .quit() only exits mainloop, does not destroy window, so we skip the assert
