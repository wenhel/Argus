# Filename: yaml_init.py
import yaml, os, sys

CURRENT_PATH = os.path.split(os.path.realpath(__file__))[0]
DM_PATH = os.sep.join([CURRENT_PATH,'dockermodels'])
CONFIG_FILE = os.sep.join([CURRENT_PATH,'config.yaml'])
NIST_CONFIG_FILE = os.sep.join([CURRENT_PATH,'config_nist.yaml'])

def merge(fList):
    ''' 
    Takes a list of yaml files and loads them as a single yaml document.
    Restrictions:
    1) None of the files may have a yaml document marker (---)
    2) All of the files must have the same top-level type (dictionary or list)
    3) If any pointers cross between files, then the file in which they are defined (&) must be 
    earlier in the list than any uses (*).
    '''
    if not fList:
        #if flist is the empty list, return an empty list. This is arbitrary, if it turns out that
        #an empty dictionary is better, we can do something about that.
        return []
    sList = []
    for f in fList:
        with open(f, 'r') as stream:
            sList.append(stream.read())
    fString = ''
    for s in sList:
        fString = fString + '\n' + s
    y = yaml.load(fString)
    return y

def init():
    # config/config.yaml
    conf = merge([CONFIG_FILE,NIST_CONFIG_FILE])
    dm_list = []
    f_list = os.listdir(DM_PATH)
    for i in f_list:
        if os.path.splitext(i)[1] == '.yaml':
            dm_list.append(i)
    dm_dict = {}
    
    # yaml to dict{configs}
    for di in dm_list:
        dmi = os.sep.join([DM_PATH,di])
        conf_raw = merge([CONFIG_FILE,dmi])
        dockermodel = conf_raw.get('dockermodel')
        dm_dict[dockermodel.get('image')] =  dockermodel
    return dm_dict, conf



if __name__ == '__main__':
    current_path = os.path.split(os.path.realpath(__file__))[0]
    targetfile = sys.argv[1]
    y = merge([os.path.join(current_path,'config.yaml'), targetfile])
    print('TESTING yaml file:')
    print(y)

