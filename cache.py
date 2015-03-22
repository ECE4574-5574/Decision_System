"""
Authored by Sumit Kumar on 3/22/2015

Description :
	Decorator class - Caches output/return values of a function for a particular set of arguments,
	by writing/reading a dictionary in the JSON format from a cache file.

Usage : 
	To use the caching capabilities, have the decorator coupled with the calling function as follows: 

	@cacheClass
	def myFunction(myArguments):
	   # Do something with the arguments
	   return myReturnValue

"""

import collections
import json

class cacheClass(object):
    def __init__(self, func):
      self.func = func
      try:
      	# Try reading from a cache file.
      	self.cache = json.load(open("cache.txt"))
      except:
      	self.cache = {}


    def __call__(self, *arguments):
        if arguments in self.cache:
            print "In Cache"
            return self.cache[arguments]
      
        else:
            value = self.func(*arguments)
            argumentsString = ' '.join(arguments)
            self.cache[argumentsString] = value
        try:
            #Write the cache to a file.
            json.dump(self.cache, open("cache.txt",'w'))
        except:
            print "here"
            pass

        return value
