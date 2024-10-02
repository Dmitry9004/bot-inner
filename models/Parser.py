from abc import ABCMeta, abstractmethod

class Parser:
	
	@abstractmethod
	def parse(self, string):
		raise Exception("Not implemented!")