from configparser import ConfigParser

config = ConfigParser()
config.read(u'dev.conf')

a = config.get('dev', 'a')

print(a)