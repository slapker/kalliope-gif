#-*- coding: utf-8 -*-

from kalliope.core.NeuronModule import MissingParameterException
import unittest
from kalliope_gif import Kalliope_gif


class Test_camera(unittest.TestCase):

    def setUp(self):
        # get parameters form the neuron
        self.configuration = {
            "directory" : "/home/xxxxx/webcam_kalliope/",
            "send-to-telegram" : True,
            "telegram-cli" : "/snap/bin/telegram-cli",
            "telegram-pub" : "/home/xxxxx/tg/tg-server.pub",
            "telegram-chan" : "yourTelegramChan",
            "nb_photos" : 1,
            "reverse" : True,
            "timer" : 1,
            "duration" : 0.2,
            "synapse" : "upload-over"
        }
    def testParameters(self):
        def run_test(configuration):
            Kalliope_gif(**configuration)   

        run_test(self.configuration)

if __name__ == '__main__':
    unittest.main()