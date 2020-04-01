import unittest
import wget
import os

class TestStringMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.file_name = 'beagle_eD.txt'
        if not os.path.isfile(self.file_name):
            url = 'https://gitlab.com/eic/escalate/workspace/raw/master/data/beagle_eD.txt'
            print(f"Downloading {url}")
            wget.download(url, out=self.file_name)
            print("Done download")

    def test_vmeson_beagle(self):
        self.assertEqual('foo'.upper(), 'FOO')
        from pyjano.jana import Jana
        Jana()\
            .plugin('beagle_reader') \
            .plugin('vmeson') \
            .plugin('jana', nevents=1, output='beagle.root') \
            .source('./beagle_eD.txt')\
            .run(retval_raise=True)



if __name__ == '__main__':
    unittest.main()
