# File-Organizer-GUI
This Python script provides a simple GUI built with `tkinter` to help you organize files in a specified directory by their extensions. It categorizes files into subfolders like **Images**, **Documents**, **Audio**, **Video**, and **Others**.

## Features

- User-friendly GUI interface
- Drag-and-drop-style window movement
- Organizes files based on file extensions
- Creates folders automatically inside an `organized_files` directory
- Graceful error handling with dialog boxes

## How It Works

The GUI offers three main components:

1. **Input Field**: Enter the full path of the directory you want to organize.
2. **Organize Button**: Starts organizing files in the given directory.
3. **Exit Button**: Closes the application.

## Supported File Categories

| Category   | Extensions                      |
|------------|----------------------------------|
| Images     | `.jpg`, `.jpeg`, `.png`, `.gif`  |
| Documents  | `.txt`, `.docx`, `.pdf`          |
| Audio      | `.mp3`, `.wav`                   |
| Video      | `.mp4`, `.avi`                   |
| Others     | All other file types             |
