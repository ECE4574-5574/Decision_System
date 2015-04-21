#Prerana Rane

import logging

# create logger
lgr = logging.getLogger('ErrorLog')
lgr.setLevel(logging.DEBUG)

# add a file handler
fh = logging.FileHandler('ErrorLog.log')
fh.setLevel(logging.WARNING)

# create a formatter and set the formatter for the handler.
frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(frmt)

# add the Handler to the logger
lgr.addHandler(fh)

#Severity Levels
lgr.debug('DEBUG') 
lgr.info('INFO') 
lgr.warn('WARN') 
lgr.error('ERROR') 
lgr.critical('CRITICAL') 
