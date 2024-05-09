import csv
import os
import unittest

import prompeteer


class MyTestCase(unittest.TestCase):
    def test_run_prompt(self):
        prompeteer.run_prompt(prompt_file_path='./azure_openai_test_prompt.yaml',
                              output_csv='./output.csv',
                              include_prompt=True,
                              input_csv='./input.csv',
                              row_numbers_to_process=[0] + list(range(1, 3)),
                              destination='file')

        self.assertTrue(os.path.exists("./output.csv"))
        with open(file="./output.csv", mode='r') as output_file:
            reader = csv.reader(output_file, delimiter=",")
            lines = enumerate(reader)
            first_row = next(lines)
            self.assertEqual(first_row[1], ['request', 'response'])
            second_row = next(lines)
            self.assertEqual(second_row[1], [
                '[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "summarize about basketball in the year 2002 use this example summary: A famous quote: "Just do it".\nExtra line for detail. do it in a very formal way"}]',
                'Simulated response for with \n multiple lines in prompt with provider Mock'])

        with open(file="./output.csv", mode='r', newline='\n') as output_file:
            reader = csv.reader(output_file)
            next(reader, None)
            row_count = sum(1 for row in reader)
            self.assertEqual(row_count, 3)

        if os.path.exists("./output.csv"):
            os.remove(os.path.join("./output.csv"))

    def test_run_prompt_specific_rows(self):
        prompeteer.run_prompt(prompt_file_path='./azure_openai_test_prompt.yaml',
                              output_csv='./output.csv',
                              include_prompt=True,
                              input_csv='./input.csv',
                              row_numbers_to_process=[0, 2],
                              destination='file')

        self.assertTrue(os.path.exists("./output.csv"))
        with open(file="./output.csv", mode='r', newline='\n') as output_file:
            reader = csv.reader(output_file)
            next(reader, None)
            row_count = sum(1 for row in reader)
            self.assertEqual(row_count, 2)

        if os.path.exists("./output.csv"):
            os.remove(os.path.join("./output.csv"))

    def test_run_prompt_specific_dont_include_prompt(self):
        prompeteer.run_prompt(prompt_file_path='./azure_openai_test_prompt.yaml',
                              output_csv='./output.csv',
                              include_prompt=False,
                              input_csv='./input.csv',
                              row_numbers_to_process=[0, 2],
                              destination='file')

        self.assertTrue(os.path.exists("./output.csv"))
        with open(file="./output.csv", mode='r', newline='\n') as output_file:
            reader = csv.reader(output_file)
            headers = next(reader)
            self.assertEqual(headers, ['response'])

        if os.path.exists("./output.csv"):
            os.remove(os.path.join("./output.csv"))


if __name__ == '__main__':
    unittest.main()
