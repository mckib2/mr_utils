## IDEA:
# Provide an interface to set things like gadgetron host, port, etc.

from configparser import ConfigParser,ExtendedInterpolation

class ProfileConfig(object):

    def __init__(self,filename='profiles.config'):
        # config file stored at top level of project
        self.filename = filename

        self.defaults = {
            'gadgetron.host': 'localhost',
            'gadgetron.port': 9002
        }

        # Make sure there is a section called 'default'
        self.parser = ConfigParser()
        self.parser.read(self.filename)
        if 'default' not in self.parser.sections():
            self.parser['default'] = self.defaults
            self.update_file()

        # Make sure there is a section called config, and make sure it has a
        # profile
        if 'config' not in self.parser.sections():
            self.parser['config'] = {'active': 'default'}
            self.update_file()
        if 'config' in self.parser.sections():
            self.active_profile = self.parser.get('config','active',fallback='default')

    def update_file(self):
        with open(self.filename,'w') as f:
            self.parser.write(f)

    def create_profile(self,profile_name,args={}):

        # Make sure args is a dictionary
        assert(type(args) is type({}))

        # Also make sure reserved names are not used
        if profile_name == 'config':
            raise ValueError('"config" is a reserved section in the config file.')

        # Make sure we're not overwriting a profile
        if profile_name in self.parser.sections():
            raise RuntimeError('Profile already exists! Not overwritten!')

        # If no values are given for any keys, use the defaults
        for key,val in self.defaults.items():
            if key not in args:
                args[key] = val

        # Create the section
        self.parser[profile_name] = args
        self.update_file()

    def activate_profile(self,profile):

        if profile not in self.parser.sections() or (profile == 'config'):
            raise ValueError('Profile label must be valid!')

        self.parser['config']['active'] = profile
        self.update_file()
        self.active_profile = profile

    def set_config(self,args,profile=None):
        '''Update profile configuration files.

        profile -- The profile to update.
        args -- Dictionary of key,value updates.

        Keys -> Values:
            'gadgetron.host' -> (string) ip-address/hostname/etc
            'gadgetron.port' -> (int) port number
        '''

        # If no profile provided, use the active profile
        if profile is None:
            profile = self.active_profile

        for key in self.defaults.keys():
            if key in args:
                self.parser[profile][key] = str(args[key])

        self.update_file()

    def get_config_val(self,key):

        # parse these out as integers
        if key in [ 'gadgetron.port' ]:
            return(self.parser.getint(self.active_profile,key))
        else:
            # as strings
            return(self.parser.get(self.active_profile,key))


if __name__ == '__main__':

    # Command line interface
    pass