# comment 100-continue in boto
import os
import botocore
import platform

file_to_update = os.path.join(os.path.dirname(botocore.__file__), 'handlers.py')

current_os = platform.platform().lower()
if current_os.startswith('windows'):
    pass
else:
    if current_os.startswith('linux'):
        sed_cmd = "sed -i \"s/^[ \t]*params\[['\\\"]headers['\\\"]\]\[['\\\"]Expect['\\\"]\][ \t]*=[ \t]*['\\\"]100-continue['\\\"]/#&/\" %s" % file_to_update
    else:
        sed_cmd = "sed -i \"\" \"s/^[ \t]*params\[['\\\"]headers['\\\"]\]\[['\\\"]Expect['\\\"]\][ \t]*=[ \t]*['\\\"]100-continue['\\\"]/#&/\" %s" % file_to_update
    os.system(sed_cmd)
