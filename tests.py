import unittest
from unittest.mock import patch, mock_open, MagicMock
import main

class TestMain(unittest.TestCase):

    @patch('main.os')
    @patch('main.subprocess')
    def test_run_autopep8(self, mock_subprocess, mock_os):
        """
        Test that run_autopep8 correctly processes Python files and ignores other file types.
        It should call subprocess.run with the correct command for each .py file in the folder.
        """
        mock_os.listdir.return_value = ['file1.py', 'file2.py', 'file3.txt']

        main.run_autopep8('test_folder')

        mock_os.listdir.assert_called_once_with('test_folder')
        expected_calls = [
            (('autopep8 --in-place --aggressive --aggressive test_folder/file1.py',), {'shell': True, 'text': True}),
            (('autopep8 --in-place --aggressive --aggressive test_folder/file2.py',), {'shell': True, 'text': True}),
        ]
        self.assertEqual(mock_subprocess.run.call_args_list, expected_calls)

    @patch('main.os')
    @patch('main.subprocess')
    def test_run_pylint(self, mock_subprocess, mock_os):
        """
        Test that run_pylint correctly processes Python files by running pylint
        and captures the output for each file in the folder.
        """
        mock_os.listdir.return_value = ['file1.py', 'file2.py']
        mock_subprocess.run.return_value.stdout = "Report\nSome issues\nfile.py:1:0: C0103: Variable name \"x\" doesn't conform to snake_case naming style (invalid-name)\n\n"

        main.run_pylint('test_folder')

        mock_os.listdir.assert_called_once_with('test_folder')
        expected_calls = [
            (('pylint test_folder/file1.py',), {'shell': True, 'text': True, 'capture_output': True}),
            (('pylint test_folder/file2.py',), {'shell': True, 'text': True, 'capture_output': True}),
        ]
        self.assertEqual(mock_subprocess.run.call_args_list, expected_calls)

    @patch('main.os')
    @patch('main.subprocess')
    @patch('main.BeautifulSoup')
    def test_generate_html_report(self, mock_soup, mock_subprocess, mock_os):
        """
        Test that generate_html_report creates an HTML report correctly, 
        calling BeautifulSoup to modify the HTML and subprocess.run for pylint output.
        """
        mock_os.listdir.return_value = ['file1.py', 'file2.py']
        mock_subprocess.run.return_value.stdout = "Line 1\nLine 2\nLine 3\n"
        mock_soup.return_value = MagicMock()
        mock_soup.return_value.find.return_value = MagicMock()

        main.generate_html_report('test_folder')

        mock_os.listdir.assert_called_once_with('test_folder')
        expected_calls = [
            (('pylint test_folder/file1.py',), {'shell': True, 'text': True, 'capture_output': True}),
            (('pylint test_folder/file2.py',), {'shell': True, 'text': True, 'capture_output': True}),
        ]
        self.assertEqual(mock_subprocess.run.call_args_list, expected_calls)
        self.assertTrue(mock_soup.return_value.find.called)

    @patch('main.os.system')
    @patch('main.run_autopep8')
    @patch('main.run_pylint')
    @patch('main.generate_html_report')
    def test_main_with_autopep8(self, mock_generate_html_report, mock_run_pylint, mock_run_autopep8, mock_system):
        """
        Test that the main function calls run_autopep8, run_pylint, and generate_html_report
        when autopep8 is set to True in the config.
        """
        main.main('test_folder', autopep8=True)

        mock_run_autopep8.assert_called_once_with('test_folder')
        mock_run_pylint.assert_called_once_with('test_folder')
        mock_generate_html_report.assert_called_once_with('test_folder')

    @patch('main.os.system')
    @patch('main.run_pylint')
    @patch('main.generate_html_report')
    def test_main_without_autopep8(self, mock_generate_html_report, mock_run_pylint, mock_system):
        """
        Test that the main function only calls run_pylint and generate_html_report
        when autopep8 is set to False in the config.
        """
        main.main('test_folder', autopep8=False)

        mock_run_pylint.assert_called_once_with('test_folder')
        mock_generate_html_report.assert_called_once_with('test_folder')

if __name__ == '__main__':
    unittest.main()
