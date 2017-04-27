class RemoteConfiguration(object):
    '''
    Configuration of an ssh connection with ssh_config(5)
    parameters made available
    '''
    def __init__(self, host, username=None, port=None):
        '''
        :param str host: Distant machine hostname
        :param str username: Distant machine login (if None, let ssh decide)
        :param int port: Connection port (if None, let ssh decide)
        '''
        self._host = host
        self._ssh_config = {}
        self.username = username
        self.port = port

    @property
    def username(self):
        ''' Username on distant host '''
        return self._ssh_config.get('User', None)

    def __set_property(self, key, value):
        if value is not None:
            self._ssh_config[key] = value
        else:
            self._ssh_config.pop(key, None)

    @username.setter
    def username(self, value):
        self.__set_property('User', value)

    @property
    def port(self):
        ''' Port to connect to '''
        return self._ssh_config.get('Port', None)

    @port.setter
    def port(self, value):
        self.__set_property('Port', value)

    def get(self, key):
        '''
        Get an ssh_config entry previously set
        :returns None if key is not set
        returns associated value if key is set
        '''
        if key in self._ssh_config:
            return self._ssh_config[key]
        return None

    def set(self, key, value):
        ''' Set an ssh_config entry '''
        self._ssh_config[key] = value

    def unset(self, key):
        ''' Remove an ssh_config entry '''
        self._ssh_config.pop(key, None)

    @property
    def host(self):
        ''' Host given to ssh command line '''
        return self._host

    def get_args(self):
        ''' Return all arguments as an array '''
        args = []
        for k, value in sorted(self._ssh_config.items()):
            # All ssh options take one argument
            args.append(u'-o')
            args.append(u'{k}={v}'.format(k=k, v=value))
        return args

    def __str__(self):
        return ' '.join(self.get_args())

    def __repr__(self):
        return str(self.get_args())
