import warnings

from labcodes.fileio.base import LogFile, LogName

try:
    from labcodes.fileio.labber import read_labber
except:
    warnings.warn('Fail to import fileio.labber.')

try:
    from labcodes.fileio.labrad import read_labrad, LabradRead
    from labcodes.fileio import labrad
except:
    warnings.warn('Fail to import fileio.labrad.')

# try:
#     from labcodes.fileio.ltspice import LTSpiceRead
# except:
#     warnings.warn('Fail to import fileio.ltspice.')

try:
    from labcodes.fileio.misc import data_to_json, data_from_json
except:
    warnings.warn('Fail to import fileio.misc.')
