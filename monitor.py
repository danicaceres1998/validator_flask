import time
import pickle
import sentry_sdk
from datetime import datetime
from os import popen, environ, system
from api.model.model import Directory

SAMPLE_RATE = 0.1
DATA_FILE   = 'api/data/data.pickle'
LOG_FILE    = 'api/logs/monitor.log'
READ_MODE   = 'rb'
WRITE_MODE  = 'wb'

sentry_sdk.init(
    environ['SENTRY_KEY'],
    traces_sample_rate=SAMPLE_RATE,
)

class ProcessesDownException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class Monitor:    
    MONTHS_DIFF = 1
    INFO_STATUS = 'INFO'
    ERROR_STATUS = 'ERROR'
    MONTHS_QUANTITY = 12
    MIN_QUANT_PROCESSES = 10
    COMMAND = 'pgrep -f uwsgi'
    DELETE_LOGS = 'rm api/logs/api.log && rm api/logs/monitor.log'
    CREATE_LOGS = 'touch api/logs/api.log && touch api/logs/monitor.log'

    def main(self):
        # Restart logs every month
        directory = self.__get_directory()
        current_date = datetime.now()
        months_diff = ((current_date.year - directory.log_date.year) * self.MONTHS_QUANTITY) + (current_date.month - directory.log_date.month)
        if months_diff > self.MONTHS_DIFF:
            directory.restart_log_date()
            self.__update_directory(directory)
            system(self.DELETE_LOGS)
            system(self.CREATE_LOGS)
            self.__log_status('Se reiniciaron los logs', False)
        # Validating the uWSGI Processes
        processes = len(list(ps for ps in popen(self.COMMAND).read().split("\n") if ps != ''))
        message = "Processes: min_expected=%d, running=%d" %(self.MIN_QUANT_PROCESSES, processes)
        error = False
        if processes < self.MIN_QUANT_PROCESSES:
            error = True
            sentry_sdk.capture_exception(ProcessesDownException(message))
        self.__log_status(message, error)

    ### Private Methods ###

    def __get_directory(self):
        file = open(DATA_FILE, READ_MODE)
        directory = pickle.load(file)
        file.close()
        return directory

    def __update_directory(self, directory):
        file = open(DATA_FILE, WRITE_MODE)
        pickle.dump(directory, file)
        file.close()
    
    def __log_status(self, message, is_error):
        if is_error:
            status = self.ERROR_STATUS
        else:
            status = self.INFO_STATUS
        log_message = "[%s %s] -> %s" %(status, time.strftime('%X'), message)
        system("echo '%s' >> %s" %(log_message, LOG_FILE))


### MAIN ###
if __name__ == '__main__':
    Monitor().main()
