# Things for the ZMQ communication
import socket


from bluesky.callbacks import CallbackBase

# Needs the lightflow environment
from lightflow.config import Config
from lightflow.workflows import start_workflow

# set where the lightflow config file is
lightflow_config_file = "/home/xf07bm/.config/lightflow/lightflow.cfg"

def submit_lightflow_job(uid, lightflow_config):
    '''
        Submit an interpolation job to lightflow
        
        uid : the uid of the data set
        lightflow_config : the lightflow config filename
    '''
    config = Config()
    config.load_from_file(lightflow_config)

    store_args = dict()
    store_args['uid'] = uid
    # not necessary
    store_args['requester'] = socket.gethostname()
    job_id = start_workflow(name='interpolation', config=config,
                            store_args=store_args, queue="qas-workflow")
    print('Started workflow with ID', job_id)

# the job submitter for the GUI
job_submitter= functools.partial(submit_lightflow_job,
                                 lightflow_config=lightflow_config_file)

class InterpolationRequester(CallbackBase):
    '''
        The interpolation requester

        On a stop doc, submits request to lightflow
    '''
    def stop(self, doc):
        uid = doc['run_start']
        job_submitter(uid)


interpolator = InterpolationRequester()
interpolation_subscribe_id = RE.subscribe(interpolator)
