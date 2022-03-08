import os
import sys
import threading
import time
import unittest
import subprocess

class MyTestCase(unittest.TestCase):

    def test_if_run_server(self):
        # Check when a proper file and ip are registered.
        process = subprocess.Popen('python server.py 127.0.0.1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        self.assertNotEqual(out, '')
        # Check when an incorrect IP is registered.
        process = subprocess.Popen('python server.py 1000', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        self.assertEqual(len(out), 0)
        # Check when an invalid file is registered
        process = subprocess.Popen('python serve.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        self.assertNotEqual(len(err),0)

    def test_if_run_client(self):
        # Check when registering a valid file
        process = subprocess.Popen('python client.py', shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = process.communicate()
        self.assertNotEqual(out, '')
        # Check when an invalid file is registered
        process = subprocess.Popen('python clien.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        self.assertNotEqual(len(err), 0)

    def test_run_server_and_client(self):
        gui_thread = threading.Thread(target=self.gui_loop1)
        gui_thread.start()
        time.sleep(0.001)
        gui_thread = threading.Thread(target=self.gui_loop2)
        gui_thread.start()

    def gui_loop1(self):
        process = subprocess.Popen('python server.py 10.9.0.136', shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = process.communicate()

    def gui_loop2(self):
        process = subprocess.Popen('python client.py', shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = process.communicate()

if __name__ == '__main__':
    unittest.main()
