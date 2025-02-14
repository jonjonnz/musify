# musiFy

This is a PyQt5-based GUI application for downloading audio from YouTube videos and playlists. The downloaded files are saved in the `Downloads` folder of the user's home directory.

## Features
- Simple and intuitive GUI
- Dark theme with enlarged elements for better readability
- Supports both individual YouTube videos and playlists
- Progress bar to indicate download status
- Error handling for invalid URLs and download failures
- Automatically centers the window on screen
- Includes an application icon

## Requirements
Ensure you have the following installed before running the application:
- Python 3.12
- PyQt5
- yt-dlp

You can install the required dependencies using:
```sh
pip install PyQt5 yt-dlp
```

## Usage
1. Run the script:
   ```sh
   python app.py
   ```
2. Enter a YouTube URL in the input field.
3. Click the **Download Audio** button.
4. The progress bar will update as the download progresses.
5. Once completed, the audio files will be available in the `Downloads` folder.

## Notes
- Ensure you have an internet connection while using the application.
- Place an `icon.png` file in the same directory as the script to display the application icon.
- The application only downloads the best available audio format.

## License
This project is open-source and available under the MIT License.

