import json
import logging
import unittest

from coalib.output.Logging import (configure_json_logging,
                                   configure_logging)


class LoggingTest(unittest.TestCase):

    def test_json_logging(self):
        log_stream = configure_json_logging()

        logging.debug('This is debug log.')
        logging.info('This is info log.')
        logging.warning('This is warning log.\n This is continued')
        logging.error('This is error log.')

        # This is a list of logs dicts.
        # Each log dict has a `message`, `level` and `time`
        # We will check message and level for each of the logs
        logs_list = [json.loads(line)
                     for line in log_stream.getvalue().splitlines()]

        self.assertEqual(logs_list[0]['message'], 'This is debug log.')
        self.assertEqual(logs_list[0]['level'], 'DEBUG')
        self.assertEqual(logs_list[1]['message'], 'This is info log.')
        self.assertEqual(logs_list[1]['level'], 'INFO')
        self.assertEqual(logs_list[2]['message'],
                         'This is warning log.\n This is continued')
        self.assertEqual(logs_list[2]['level'], 'WARNING')
        self.assertEqual(logs_list[3]['message'], 'This is error log.')
        self.assertEqual(logs_list[3]['level'], 'ERROR')

    def test_file_logging(self):
        configure_logging()
        debug_text = 'This is debug log.'
        logging.debug(debug_text)
        with open('.coala.log') as log_file:
            self.assertIn(debug_text, log_file.read())

        configure_logging(logging.ERROR, True)
        debug_text2 = 'This is another debug log.'
        logging.debug(debug_text2)
        with open('.coala.log', 'r') as log_file:
            self.assertIn(debug_text2, log_file.read())
