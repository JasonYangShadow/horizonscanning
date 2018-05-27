from Crypto.Cipher import AES
import base64
from config import Config
from exception import Type, TeleException

class Crypto:
	def __init__(self,config_path='config.ini'):
		self.__config=Config(config_path)
		self.__key=self.__config.getValue('Crypto','KEY')
		self.__iv=self.__config.getValue('Crypto','IV')

	def encrypt(self,input):
		if self.__key is not None and self.__iv is not None:
			obj=AES.new(self.__key,AES.MODE_CFB,self.__iv)
			return base64.b64encode(obj.encrypt(input))
		else:
			raise TeleException(Type.NoneException,'doesn\'t exist key or iv') 

	def decrypt(self,input):
		if self.__key is not None and self.__iv is not None:
			obj=AES.new(self.__key,AES.MODE_CFB,self.__iv)
			return obj.decrypt(base64.b64decode(input))
		else:
			raise TeleException(Type.NoneException,'doesn\'t exist key or iv') 
