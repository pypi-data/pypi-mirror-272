import argparse
import logging
import sys
import os
import asyncio
import getpass
import time
from .libs import AsyncCounter
import time

from sourceplus_sdk import __version__

__author__ = "Nick Padgett"
__copyright__ = "Spawning Inc"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


DOWNLOAD_KEY_ENV_VAR = "SOURCEPLUS_DOWNLOAD_KEY"

import httpx
import pandas as pd
import aiofiles


def download_images(
    file_path: str,
    output_folder: str,
    num_download_jobs: int = 10,
    limit_images: int = -1,
    url_column_name: str = "url",
    show_progress: bool = False,
):
    """Download images from the given file path to the destination folder.

    Args:
        file_path (str): The path to the file containing the URLs of the images to download.
        output_folder (str): The path to the folder where the images will be saved.
        num_download_jobs (int, optional): The maximum number of parallel downloads. Defaults to 10.
        limit_images (int, optional): The maximum number of images to download. Defaults to -1, which means all images.
        url_column_name (str, optional): The name of the column containing the URLs in the file. Defaults to "url".
        show_progress (bool, optional): Whether to show a progress bar. Defaults to False.

    """

    # validate the input arguments
    full_source_path, full_destination_path, destination_folder_exists = validate_args(file_path, output_folder, num_download_jobs)

    # check if API key is present in env, and if not, prompt for it
    download_key = os.getenv(DOWNLOAD_KEY_ENV_VAR)
    if not download_key:
        download_key = prompt_for_download_key()

    # prompt to create destination folder if it does not exist
    if not destination_folder_exists:
        # ask user if we should create it
        prompt_destination_folder_creation(full_destination_path)

    df, num_images = validate_file(full_source_path, url_column_name, limit_images)

    # download the images
    asyncio.run(start_image_downloads(df, num_download_jobs, num_images, full_destination_path, download_key, show_progress))


def validate_args(file_path: str, output_folder: str, num_download_jobs: int):
    """
    Validates the input arguments.

    Args:
        file_path (str): The path to the file containing the URLs of the images to download.
        output_folder (str): The path to the folder where the images will be saved.
        num_download_jobs (int): The maximum number of parallel downloads.
    """

    # expand the paths
    full_source_path = os.path.expanduser(file_path)
    full_destination_path = os.path.expanduser(output_folder)

    # make sure the number of download jobs is within the valid range
    if num_download_jobs < 1 or num_download_jobs > 100:
        raise ValueError("max_parallel_downloads must be between 1 and 100.")

    # make sure the destination folder exists
    destination_folder_exists = os.path.exists(full_destination_path)

    return full_source_path, full_destination_path, destination_folder_exists


def validate_file(file_path: str, url_column_name: str, limit_images: int = -1):
    """
    Validates the file path.

    Args:
        file_path (str): The path to the file containing the URLs of the images to download.
        url_column_name (str): The name of the column containing the URLs in the file.

    Returns:
        pd.DataFrame: The DataFrame containing the URLs of the images to download.

    """

    # make sure the source file path exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")

    # open the file
    file_name = os.path.basename(file_path).lower()
    file_extension = os.path.splitext(file_name)[1]
    if file_extension == ".parquet":
        df = pd.read_parquet(file_path)
    elif file_extension == ".csv":
        df = pd.read_csv(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

    # make sure the limit_images is valid
    if limit_images < 0:
        limit_images = -1
    if limit_images == -1:
        limit_images = len(df)
    elif limit_images > len(df):
        limit_images = len(df)

    # make sure the url column exists
    if url_column_name not in df.columns:
        raise ValueError(f"Column '{url_column_name}' not found in the file.")

    return df, limit_images


def prompt_for_download_key():
    """
    Prompts the user for the download key.

    Returns:
        str: The download key.

    """

    download_key = getpass.getpass("Enter your Source+ download key: ")
    return download_key


def prompt_destination_folder_creation(destination_folder: str):
    """
    Prompts the user to create the destination folder if it does not exist.

    Args:
        destination_folder (str): The path to the destination folder.

    """

    create_folder = input(f"The destination folder '{destination_folder}' does not exist. Create it? (y/n) ")
    if create_folder.lower() == "y":
        os.makedirs(destination_folder)
    else:
        raise ValueError("Destination folder does not exist, and user chose not to create it. Exiting.")


async def start_image_downloads(df: pd.DataFrame, max_parallel_downloads: int, max_images: int, destination_folder: str, api_key: str, show_progress: bool = False):
    """
    Starts downloading images from the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the URLs of the images to download.
        max_parallel_downloads (int): The maximum number of parallel downloads.
        max_images (int): The maximum number of images to download.
        destination_folder (str): The path to the folder where the images will be saved.
        api_key (str): The Source+ download key.
        show_progress (bool, optional): Whether to show a progress bar. Defaults to False.

    """

    # create the download queue
    semaphore = asyncio.Semaphore(max_parallel_downloads)
    download_queue = df.iterrows()

    # start the download manager
    success_counter = AsyncCounter()
    failure_counter = AsyncCounter()
    tasks = []
    for i in range(0, max_images if max_images > 0 else len(df)):
        row = next(download_queue)
        url = row[1]["url"]
        tasks.append(download_image(url, semaphore, success_counter, failure_counter, destination_folder, api_key))

    # start the progress monitor
    if show_progress:
        tasks.insert(0, progress_monitor(success_counter, failure_counter, max_images))

    # wait for all tasks to complete
    await asyncio.gather(*tasks)


async def progress_monitor(success_counter: AsyncCounter, failure_counter: AsyncCounter, total_images: int):
    """
    Monitors the progress of the downloads.

    Args:
        success_counter (AsyncCounter): The counter to monitor.
        failure_counter (AsyncCounter): The counter to monitor.
        total_images (int): The total number of images to download.

    """

    # print empty lines for us to update
    for _ in range(1):
        print("\n")

    start_time = time.time()
    while True:
        successes = await success_counter.get()
        failures = await failure_counter.get()
        num_completed = successes + failures

        sys.stdout.write("\033[F" * 1)  # Move up cursor

        # print a progress bar
        progress = num_completed / total_images
        bar_length = 50
        bar = "#" * int(bar_length * progress)
        elapsed_time = time.time() - start_time
        print(f"[{bar.ljust(bar_length)}] {progress * 100:.2f}% - Elapsed Time: {elapsed_time:.2f}s")

        if num_completed == total_images:
            break
        await asyncio.sleep(.5)

    print(f"Total images: {total_images}. Successes: {successes}. Failures: {failures}")


async def download_image(url: str, semaphore: asyncio.Semaphore, success_counter: AsyncCounter, failure_counter: AsyncCounter, destination_folder: str, api_key: str):
    """
    Downloads an image from the given URL, using the semaphore to control the number of parallel downloads.

    Args:
        url (str): The URL of the image to download.
        semaphore (asyncio.Semaphore): The semaphore to control the number of parallel downloads.
        success_counter (AsyncCounter): The counter to keep track of the number of successful downloads.
        failure_counter (AsyncCounter): The counter to keep track of the number of failed downloads.
        destination_folder (str): The path to the folder where the image will be saved.
        api_key (str): The Source+ download key.

    """

    async with semaphore:
        # get file path and name
        file_name = url.split("/")[-1]
        file_path = os.path.join(destination_folder, file_name)

        # if file exists, skip it, so we don't download it twice
        if os.path.exists(file_path):
            await success_counter.increment()
            return

        async with httpx.AsyncClient(timeout=10) as client:
            try:
                async with client.stream("GET", url, headers={"Authorization": f"API {api_key}"}, follow_redirects=True) as response:
                    if response.status_code == 200:
                        image_data = await response.aread()
                        async with aiofiles.open(file_path, "wb") as f:
                            await f.write(image_data)
                        await success_counter.increment()
                    else:
                        #logging.error(f"Failed to download image from URL: {url} - {response.status_code}")
                        await failure_counter.increment()
            except Exception as e:
                #logging.error(f"Failed to download image from URL: {url} - {e}")
                await failure_counter.increment()

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Download images.")
    parser.add_argument("command", help="Command to execute. Valid commands: download_images", type=str)
    parser.add_argument("-f", "--file", dest="file_path", help="Path to the file which contains the image URLs.", type=str)
    parser.add_argument("-o", "--output", dest="output_folder", help="Path to the destination folder to download the images.", type=str)
    parser.add_argument("-j", "--jobs", dest="num_download_jobs", default=10, help="The maximum number of download jobs running in parallel. A value too high will cause resource contention and slow down the overall download rate.", type=int)
    parser.add_argument("-l", "--limit", dest="limit_images", default=-1, help="The maximum number of images you want to download from the file.", type=int)
    parser.add_argument("-n", "--name", dest="url_column_name", default="url", help="The column name for the url field.", type=str)
    parser.add_argument("-p", "--progress", dest="show_progress", default=True, help="Show progress bar.", type=bool)

    parser.add_argument(
        "--version",
        action="version",
        version=f"sourceplus-sdk {__version__}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`download_images` to be called with string arguments in a CLI fashion

    Args:
      args (List[str]): command line parameters as list of strings
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    if args.command == "download_images":
        download_images(args.file_path, args.output_folder, args.num_download_jobs, args.limit_images, args.url_column_name, args.show_progress)
    else:
        raise ValueError(f"Invalid command: {args.command}")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
