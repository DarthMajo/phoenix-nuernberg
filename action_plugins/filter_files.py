import re

from ansible.plugins.action import ActionBase

class ActionModule(ActionBase):
    """Takes a list of file matches and filter out the ones we don't want."""
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        pattern = re.compile("\/proc\/\d+\/status")
        paths = []

        # Loop over all files found and only get the files that we want.
        for file in task_vars.get('found_files')['files']:
            if re.match(pattern, file.get('path')):
                paths.append(file.get('path'))

        return {'paths': paths}

