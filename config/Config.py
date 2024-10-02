class Config:
	def __init__(self, env):
		self.__attributes = {}

		f = open(env, "r") 
		try:
			for line in f:
				lineValues = line.split("=")
				nameAttr = lineValues[0]
				value = lineValues[1].strip()

				self.__attributes[nameAttr] = value
		except:
			raise "Not can read config.txt";
		finally:
			f.close()

	def getAttribute(self, attrName):
		if attrName in self.__attributes:
			return self.__attributes[attrName]

		return ""