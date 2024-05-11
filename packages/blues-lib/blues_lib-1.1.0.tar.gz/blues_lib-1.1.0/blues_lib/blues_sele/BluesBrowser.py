from .browser.BluesChrome import BluesChrome 
from .browser.BluesDebugChrome import BluesDebugChrome

class BluesBrowser():

  @classmethod
  def chrome(cls,config={},arguments={},experimental_options={}):
    return BluesChrome(config,arguments,experimental_options)
  
  @classmethod
  def debug_chrome(cls,config={},arguments={},experimental_options={}):
    return BluesDebugChrome(config,arguments,experimental_options)