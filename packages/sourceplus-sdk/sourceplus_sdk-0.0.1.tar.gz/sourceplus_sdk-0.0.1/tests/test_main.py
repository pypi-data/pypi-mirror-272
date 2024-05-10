from unittest import TestCase
from unittest.mock import patch
import os
import asyncio

import sourceplus_sdk.main
from sourceplus_sdk.libs import AsyncCounter


class TestMain(TestCase):

    def test_validate_args(self):
        # test validation of number of jobs
        with self.assertRaises(ValueError):
            sourceplus_sdk.main.validate_args("./files/good.parquet", "./sample", 0)
        with self.assertRaises(ValueError):
            sourceplus_sdk.main.validate_args("./files/good.parquet", "./sample", 101)

        # # test validation of output folder
        full_source_path, full_destination_path, destination_folder_exists = sourceplus_sdk.main.validate_args("./tests/files/good.parquet", "./tests/sample", 100)
        self.assertFalse(destination_folder_exists)
        full_source_path, full_destination_path, destination_folder_exists = sourceplus_sdk.main.validate_args("./tests/files/good.parquet", "./tests/files", 100)
        self.assertTrue(destination_folder_exists)

        # test expansion of user home path
        full_source_path, full_destination_path, destination_folder_exists = sourceplus_sdk.main.validate_args("~/tests/files/good.parquet", "~/tests/sample", 100)
        self.assertFalse(full_source_path.startswith("~"))
        self.assertFalse(full_destination_path.startswith("~"))

    def test_validate_file(self):
        # test validation of input file exists
        with self.assertRaises(FileNotFoundError):
            sourceplus_sdk.main.validate_file("./tests/files/nonexistent_file.parquet", "url", 1)
        sourceplus_sdk.main.validate_file("./tests/files/good.parquet", "url", 1)

        # test validation of file type
        with self.assertRaises(ValueError):
            sourceplus_sdk.main.validate_file("./tests/files/bad.tsv", "url", 1)

        # test validation of image limit
        df, image_limit = sourceplus_sdk.main.validate_file("./tests/files/good.parquet", "url", 1)
        self.assertEqual(image_limit, 1)
        df, image_limit = sourceplus_sdk.main.validate_file("./tests/files/good.parquet", "url", -1)
        self.assertEqual(image_limit, 10)
        df, image_limit = sourceplus_sdk.main.validate_file("./tests/files/good.parquet", "url", 20)
        self.assertEqual(image_limit, 10)

        # test validation of column name
        with self.assertRaises(ValueError):
            sourceplus_sdk.main.validate_file("./tests/files/good.parquet", "bad_column", 1)
        df, image_limit = sourceplus_sdk.main.validate_file("./tests/files/good.parquet", "url", 1)

    @patch('getpass.getpass', return_value='test')
    def test_prompt_for_download_key(self, mock_getpass):
        mock_getpass.return_value = "test"
        download_key = sourceplus_sdk.main.prompt_for_download_key()
        self.assertEqual(download_key, 'test')

        mock_getpass.assert_called_once_with("Enter your Source+ download key: ")

    @patch('builtins.input', return_value='y')
    def test_prompt_destination_folder_creation_success(self, mock_input):
        # tests affirmative
        sourceplus_sdk.main.prompt_destination_folder_creation("./tests/tmp")

        # make sure folder exists
        self.assertTrue(os.path.exists("./tests/tmp"))

    @patch('builtins.input', return_value='n')
    def test_prompt_destination_folder_creation_failure(self, mock_input):
        # tests negative
        with self.assertRaises(ValueError):
            sourceplus_sdk.main.prompt_destination_folder_creation("./tests/tmp2")

        # make sure folder does not exist
        self.assertFalse(os.path.exists("./tests/tmp2"))

    def test_download_image(self):
        url = "https://spawning.ai/static/media/spawning-logo-white.41278a710f4eb8e721ff.png"
        destination_folder = "./tests/tmp3"
        api_key = "test"

        os.mkdir(destination_folder)

        async def async_test_image():
            sem = asyncio.Semaphore(1)
            success_counter = AsyncCounter()
            failure_counter = AsyncCounter()

            await sourceplus_sdk.main.download_image(url, sem, success_counter, failure_counter, destination_folder, api_key)
            self.assertEqual(await success_counter.get(), 1)
            self.assertEqual(await failure_counter.get(), 0)

            # test same url
            await sourceplus_sdk.main.download_image(url, sem, success_counter, failure_counter, destination_folder, api_key)
            self.assertEqual(await success_counter.get(), 2)
            self.assertEqual(await failure_counter.get(), 0)

            # test bad url
            await sourceplus_sdk.main.download_image("https://spawning.substack.com/sdk.test.jpg", sem, success_counter, failure_counter, destination_folder, api_key)
            self.assertEqual(await success_counter.get(), 2)
            self.assertEqual(await failure_counter.get(), 1)

        asyncio.run(async_test_image())

    @patch('getpass.getpass', return_value='test')
    def test_download_images(self, mock_getpass):
        # create outputs folder
        os.mkdir("./tests/output")
        sourceplus_sdk.main.download_images("./tests/files/good.parquet", "./tests/output")

        # make sure if we don't have an environment variable set, we prompt for the download key
        mock_getpass.assert_called_once_with("Enter your Source+ download key: ")

        # make sure images exist in the folder
        # list number of files
        files = os.listdir("./tests/output")
        self.assertEqual(len(files), 9)

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists("./tests/tmp"):
            for root, dirs, files in os.walk("./tests/tmp"):
                for file in files:
                    os.remove(os.path.join(root, file))
            os.rmdir("./tests/tmp")

        if os.path.exists("./tests/tmp2"):
            for root, dirs, files in os.walk("./tests/tmp2"):
                for file in files:
                    os.remove(os.path.join(root, file))
            os.rmdir("./tests/tmp2")

        if os.path.exists("./tests/tmp3"):
            for root, dirs, files in os.walk("./tests/tmp3"):
                for file in files:
                    os.remove(os.path.join(root, file))
            os.rmdir("./tests/tmp3")

        if os.path.exists("./tests/output"):
            for root, dirs, files in os.walk("./tests/output"):
                for file in files:
                    os.remove(os.path.join(root, file))
            os.rmdir("./tests/output")