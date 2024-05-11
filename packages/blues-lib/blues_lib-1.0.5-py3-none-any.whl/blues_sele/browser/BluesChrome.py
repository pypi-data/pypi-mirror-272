import sys,os,re,subprocess,time
from selenium import webdriver
from seleniumwire import webdriver as wireWebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

sys.path.append(re.sub('packages.*','',os.getcwd()))
from packages.blues_util.BluesPowerShell import BluesPowerShell 
from packages.blues_sele.action.BluesDriverAction import BluesDriverAction  

class BluesChrome():

  CONFIG = {
    'url':'https://www.baidu.com', # default open web page
  }

  # https://peter.sh/experiments/chromium-command-line-switches/
  ARGUMENTS = {
    '--start-maximized':'',
    '--no-default-browser-check':'',
    '--disable-notifications':'',
    '--disable-web-security':'',
    '--ignore-certificate-errors':'',
    '--disable-infobars':'',
    '--hide-crash-restore-bubble':'',
    '--disable-popup-blocking':'',
  }

  EXPERIMENTAL_OPTIONS = {
    'detach':True,
    'prefs' : {
      # 0 - Default, 1 - Allow, 2 - Block
      "profile.default_content_setting_values.notification": 2,
      # Removing the webdriver property from the navigator object,so the browser could not distinguish whether for robots
      "Page.addScriptToEvaluateOnNewDocument":{
        "source": """
          Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
          })
        """
      }
    }
  }

  def __init__(self,config={},arguments={},experimental_options={}):
    '''
    @description : Get a Chrome Driver instance
    @param {dict} config
    '''
    self.config = {**self.CONFIG,**config}
    self.arguments = {**self.ARGUMENTS,**arguments} 

    # connect to a exist chrome, can't set detach and prefs options
    if experimental_options.get('debuggerAddress'):
      self.experimental_options = experimental_options
    else:
      self.experimental_options = {**self.EXPERIMENTAL_OPTIONS,**experimental_options}

    self.chrome_driver_exe = BluesPowerShell.get_env_value('CHROME_DRIVER_EXE')
    self.driver = None
    self.action = None
    self.__created()

  def __created(self):
    chrome_service = self.__get_service()
    chrome_options = self.__get_options()
    self.driver = webdriver.Chrome( service = chrome_service, options = chrome_options)
    self.action = BluesDriverAction(self.driver)  
    
    url = self.config.get('url')
    if url:
      self.driver.get(url)
  
  def quit(self):
    self.driver.quit()

  def __get_options(self):
    chrome_options = ChromeOptions()
    
    for key,value in self.arguments.items():
      arg_value = '%s=%s' % (key,value) if value else key
      chrome_options.add_argument(arg_value)

    for key,value in self.experimental_options.items(): 
      chrome_options.add_experimental_option(key,value)

    return chrome_options

  def __get_service(self):
    executable_path=self.chrome_driver_exe if self.chrome_driver_exe else ChromeDriverManager().install()
    return ChromeService(executable_path) 

