from dir_util.util import Util
import _thread
from machine import Pin

class Thread:
    def __init__(self, buzzer):
        self._running               = False
        self._control_running       = False
        self._current_process       = None
        self._completed             = False
        self._counter               = 0
        self._buzzer                = buzzer
        self._dic_process_counter   = {"allowed-door": 5, "opened-door": 10, "semi-closed-door": 1, "solution-intrusion": 5, "first-time-config": 3, "minimun-presence": 5}
        self._dic_process_beep      = {"intrusion": 15, "close-door": 2}

    def start_counter(self, name_process):
        self.release_thread()
        self.set_on_process(name_process)
        self._counter  =  self._dic_process_counter[name_process]
        
        _thread.start_new_thread(self.counter, ())
    
    def start_beep(self, name_process):
        self.release_thread()
        self.set_on_process(name_process)
        
        _thread.start_new_thread(self.beep, (self._dic_process_beep[name_process],))
    
    def release_thread(self):
        if(self._running):
            self._control_running = False
            self.wait_terminate()
        
    def reset(self):
        if(self._current_process != None):
            self._control_running       = False
            self.wait_terminate()
            self._running               = False
            self._completed             = False
            self._current_process       = None

    def set_on_process(self, name_process):
        self._current_process   = name_process
        self._control_running   = True
        self._running           = True
        self._completed         = False
    
    def finish_process(self):
        self._completed          = True
        self._control_running    = False
        self._running            = False
        self._buzzer.off()
        
    def counter(self):
        while(self._counter > 0):
            Util.wait_sec(1)
            self._counter -= 1

            if(not self._control_running):
                self._running  = False
                return

        self.finish_process()
    
    def beep(self, beep_per_second):
        aux_calc = int(1000/beep_per_second)
        while(self._control_running):
            Util.wait_ms(aux_calc)
            self._buzzer.toggle()
        
        self.finish_process()

    def wait_terminate(self):
        while self._running:
            Util.wait_ms(10)

        self._running  = False

    def check_process(self, process):
        return self._current_process == process
    
    def is_running(self):
        return self._running

    def is_completed(self):
        return self._completed
    
    def get_counter(self):
        return self._counter