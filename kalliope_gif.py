#! usr/bin/python
# -*- coding: ISO-8859-1 -*-
import logging

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException
import os
import imageio
import threading
from pygame import mixer
from pygame import camera
from pygame import image
from time import sleep
from time import time


logging.basicConfig()
logger = logging.getLogger("kalliope")


class Kalliope_gif(NeuronModule):
    """
    Use the your cam to make Funny GIF
    """
    def __init__(self, **kwargs):
        super(Kalliope_gif, self).__init__(**kwargs)

        # get the command
        self.nb_photos = kwargs.get('nb_photos', None)
        self.duration = kwargs.get('duration', None)
        self.directory = kwargs.get('directory', None)
        self.timer = kwargs.get('timer', 1)
        self.reverse = kwargs.get('reverse', False)
        self.send_to_telegram = kwargs.get('send-to-telegram',None)
        self.telegram_cli = kwargs.get('telegram-cli', None)
        self.synapse = kwargs.get('synapse', None)
        self.telegram_pub = kwargs.get('telegram-pub', None)
        self.telegram_chan = kwargs.get('telegram-chan', None)
        
        if self._is_parameters_ok():
            myGif = Gif(self.directory,self.nb_photos,self.reverse,self.duration,self.timer)
            mySound = Sound()
            mySound.play_countdown()
    
            file_gif=myGif.make_gif(mySound)
            mySound.quit()
            
            upload = UploadThread(self.telegram_cli,self.telegram_pub,self.telegram_chan, file_gif,callback=self.callback_run_synapse)
            upload.start()
            self.say({})
        
    def callback_run_synapse(self):
        """
        Callback method which will be started once the upload GIF is over
        :return:
        """
        logger.debug("[KALLIOPE_GIF] GIF upload is over, start the synapse %s" % self.synapse)
        self.run_synapse_by_name(synapse_name=self.synapse,
                                 high_priority=False)
        

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise
        .. raises:: InvalidParameterException
        """
        if self.nb_photos is None:
            raise InvalidParameterException("Kalliope_GIF needs a photo number")
        if self.duration is None:
            raise InvalidParameterException("Kalliope_GIF needs a duration")
        if self.directory is None:
            raise InvalidParameterException("Kalliope_GIF needs a directory")
        if self.send_to_telegram is None :
            raise InvalidParameterException("Kalliope_GIF needs to know if the Gif should be sent to your telegram account")
        if self.send_to_telegram == True:
            if self.telegram_cli is None:
                raise InvalidParameterException("Kalliope_GIF needs your telegram-cli path")
            if self.telegram_pub is None:
                raise InvalidParameterException("Kalliope_GIF needs your Telegram pub for authenticate")
            if self.telegram_chan is None:
                raise InvalidParameterException("Kalliope_GIF needs your Telegram channel where the Gif will be upload")
            if self.synapse is None:
                raise InvalidParameterException("Kalliope_GIF needs a synapse to launch once the Gif is sent to telegram")
        return True

class UploadThread(threading.Thread):
    def __init__(self,telegram_cli,telegram_pub,telegram_chan,file_gif, callback):
        """
        A Thread that will call the given callback method after uploaded the Gif on telegram
        :param telegram_cli : Path of the telegram_cli bin
        :param file_gif : Path of GIF to upload
        :param callback: callback method
        """
        threading.Thread.__init__(self)
        self.telegram_cli = telegram_cli
        self.telegram_pub = telegram_pub
        self.telegram_chan = telegram_chan
        self.file_gif=file_gif
        self.callback = callback

    def run(self):
        logger.debug("[KALLIOPE_GIF] Uploading GIF : " + str(self.file_gif) + " with : " + self.telegram_cli)
        os.system(self.telegram_cli + " -k " + self.telegram_pub + " -W -e 'send_file " + self.telegram_chan + " " + self.file_gif + "'")
        # then run the callback method
        self.callback()
        
class Gif(NeuronModule):
    def __init__(self, save_directory,nb_photos,isReverse,duration,timer):
        camera.init()
        self.cam = camera.Camera("/dev/video0",(320,200))
        self.images_cam=[]
        self.save_directory=save_directory
        self.nb_photos=nb_photos
        self.isReverse=isReverse
        self.duration=duration
        self.timer=timer
           
    def make_gif(self,mySound):
        self.cam.start()
    	for j in range(50):
    	    self.cam.get_image()

        while mySound.is_mixer_busy(): {
            sleep(0.1)
        }
        
        mySound.prepare_single_shot_song()
        i=0
        oldTime=None
        while (i<self.nb_photos):
            self.cam.get_image()
            if self.second_passed(oldTime):
                mySound.play_single_shot()
                sleep(0.3)
                img=self.cam.get_image()
                self.images_cam.append(img)
                oldTime=time()
                i+=1
                
        self.cam.stop()
        self.save_images()
        return self.save_gif()

            
    def save_images(self):
        for j in range(len(self.images_cam)):
            image.save(self.images_cam[j],self.save_directory + "camlliope_" + str(j) +".png")
            
    def save_gif(self):
        images=[]
        for i in range(self.nb_photos):
            images.append(imageio.imread(self.save_directory + "camlliope_" + str(i) + ".png"))
 
        if self.isReverse==True:
            for i in range(self.nb_photos - 2):
                images.append(imageio.imread(self.save_directory + "camlliope_" + str(self.nb_photos - i - 2) + ".png"))
        
        file_gif = self.save_directory + "camlliope.gif"
        imageio.mimsave(file_gif, images,"GIF",duration=self.duration)
        return file_gif
    
    def second_passed(self,oldTime):
        if (oldTime is None):
            return True
        else:
            return time() - oldTime >= self.timer

        

class Sound(NeuronModule):
    def __init__(self,**kwargs):
        mixer.init()
        mixer.music.set_volume(100)
        self.sound_path = self.get_sound_path();
        
    def play_countdown(self):
        mixer.music.load(self.sound_path + "countdown_female.wav")
        mixer.music.play()
        
    def prepare_single_shot_song(self):
        mixer.music.load(self.sound_path + "single-shoot.wav")

    def play_single_shot(self):
        mixer.music.play()
    
    def is_mixer_busy(self):
        return mixer.music.get_busy()
        
    def get_sound_path(self):
        sound_path = os.path.dirname(os.path.abspath(__file__)) + "/sounds/"
        return sound_path
    
    def quit(self):
        mixer.quit()
        
        
