# Import the required modules
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QProgressBar
from youtube_dl import YoutubeDL

# Define the main window class
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the title and size of the window
        self.setWindowTitle("YouTube Video Downloader")
        self.resize(400, 130)

        # Create a label for the video URL
        self.url_label = QLabel("YouTube Video URL:", self)
        self.url_label.move(10, 10)

        # Create a text box for entering the video URL
        self.url_input = QLineEdit(self)
        self.url_input.move(10, 30)
        self.url_input.resize(380, 20)

        # Create a download button
        self.download_button = QPushButton("Download", self)
        self.download_button.move(10, 60)
        self.download_button.clicked.connect(self.download_video)

        # Create a progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.move(10, 90)
        self.progress_bar.resize(380, 20)

    def download_video(self):
        # Get the video URL from the text box
        video_url = self.url_input.text()

        # Define the options for downloading the video
        # In this case, we are setting the format to mp3 and the output file name
        ydl_opts = {
            'format': 'bestaudio/best[ext=mp3]',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [self.update_progress_bar],
        }

        # Download the video using youtube-dl
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    def update_progress_bar(self, d):
        if d['status'] == 'downloading':
            # Strip the leading and trailing whitespace from the progress percentage string
            progress_percentage = d['_percent_str'].strip()
            # Convert the progress percentage string to a float
            progress_percentage = float(progress_percentage.split('%')[0])
            # Convert the progress percentage float to an integer
            progress_percentage = int(progress_percentage)
            self.progress_bar.setValue(progress_percentage)

# Create the application object
app = QApplication(sys.argv)

# Create the main window
window = MainWindow()

# Show the main window
window.show()

# Run the application
sys.exit(app.exec_())
