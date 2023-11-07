# Modnificent

## Scrape creator data from social media platforms using Selenium

## Set-up

Create a python virtual environment (documentation: https://docs.python.org/3/library/venv.html) "python -m venv /path/to/venv"

Activate the virtual environment (same documentation; is different for Linux, MacOS, and Windows)
The command for MacOS is:

```bash
source /path-to-venv/bin/activate
```

In your environment run: "pip install -r requirements.txt"

In order to use `youtube_creator.py`, you need to create a .txt file with all of desired search terms and specify the path when running the script.

You also need to download the Chrome Driver from here: https://chromedriver.chromium.org/downloads, extract it, and try opening the chromedriver. After successfully opening it, put the `chromedriver` file in `/usr/local/bin` by doing `mv chromedriver /usr/local/bin`
Make sure you are on the version that is compatible with your version of Google Chrome.

If your terminal says you don't have permission, you can run "sudo mv chromedriver /usr/local/bin" and it will ask for your computer password.

## Prerequisites

To write to csv files with creator data, you will need to have the Google Drive desktop app (download [here](https://www.google.com/drive/download/)).

Make sure your virtual environment is activated according to the `README.md` in the root of this repository (creator-serving).

Change your present working directory so that your current working directory is `selenium/`. You can do this by `cd selenium` from the root `creator-serving` directory.

_Note: The following commands are examples using a Mac terminal. Use the proper commands and file paths for your OS._

## Scrape data on Youtube creators

Run "python3 main.py"

Follow the prompts

The csv files should download into a folder called "csv_files" which you can then copy / import into GDrive.
