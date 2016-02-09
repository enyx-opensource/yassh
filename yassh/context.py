from .run import run


class Context(object):
    __variables = []

    '''
    This class is used to keep common ``Command`` constructor variables.
    '''
    def __init__(self, **kwargs):
        '''
        Save ``kwargs`` variables in order to merge them
        uppon context enter.
        '''
        self.variables = kwargs

    def __enter__(self):
        '''
        Merge saved variables into global variables dictionary.
        '''
        Context.__variables.append(self.variables)

    def __exit__(self, *discarded):
        '''
        Remove saved variables from global variables dictionary.
        '''
        Context.__variables.pop()

    def _get(self, name):
        for variables in reversed(Context.__variables):
            v = variables.get(name, None)
            if v:
                return v

        return None

    def _get_default(self, name, default):
        found = self._get(name)

        return found if found else default

    def _get_required(self, name):
        found = self._get(name)

        if found:
            return found

        raise KeyError('Missing variable "{0}" from context'.format(name))

    def _print_header(self, logfile, cmd):
        logfile.write('#' * 30 + '\n')
        logfile.write('# {0}\n'.format(cmd))

    def run(self, cmd):
        '''
        Run the ``cmd`` picking host, username, logfile and ms_timeout
        from global variables.

        Returns
        -------
        int
            The command result code.
        '''
        logfile = self._get_default('logfile', None)
        if logfile:
            self._print_header(logfile, cmd)

        return run(self._get_required('host'),
                   self._get_required('username'),
                   cmd,
                   logfile=logfile,
                   ms_timeout=self._get_default('ms_timeout', -1))
