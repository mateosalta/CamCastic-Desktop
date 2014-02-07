from usermodekeylog import KeyStates
import os

class CamcasticCameraConfig:
  '''
  A camera object to hold configuration data about each camera
  '''
  def __init__(self, root, url):
    super().__init__()
    self.app = root
    self.url = url
    self.res = (0,0)
    self.offset = (0,0)
    self.justify = 'bottom-right'
    self.resolutions = []
    self.opacity = 1.0
    self.visible = False

class CamcasticCameras(list):
  def __init__(self, root):
    super().__init__()
    self.app = root
  def __get_settings(self, camera):
    camera.res = (640, 480)
  def get_cameras(self):
    #TODO enumerate
    #to get something up and running I'm just setting stuff for now...
    for item in os.listdir('/dev'):
      if 'video' in item:
        self.append(CamcasticCameraConig(root=self.app, url='/dev/' + item))
    self.append(CamcasticCameraConig(self.app, '/dev/video0'))
    for camera in self:
      self.__get_settings(camera)


class CamcasticBaseConfig:
  def __init__(self, root):
    super().__init__()
    self.cameras = []
    self.app = root
  def find_cameras(self):
    self.cameras = []

class CamcasticShortcuts:
  def __init__(self, root):
    self.app = root
    self.states = KeyStates(root)
  def __check_event(self):
    pass
  def set_key_state(self, keypress):
    #update key_state table
    self.__check_event()
    pass

class CamcasticConfigParser:
  def __init__(self, root):
    self.app = root
  def __get_current(self):
    pass
  def read(self):
    pass
  def write(self):
    pass
