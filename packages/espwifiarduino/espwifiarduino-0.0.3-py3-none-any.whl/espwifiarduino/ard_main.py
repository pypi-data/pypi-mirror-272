from threading import Lock, Thread
import re, time

from websockets.sync.client import connect

type_to_pos = {"i": 0, "f": 1, "s": 2}

class ArduinoVars():

    def __init__(self, uri, room):
        self.data_mutex = Lock()
        self.main_data = [[0,0.0,""] for i in range(8)]
        self.ws = None
        self.uri = uri
        self.room = room
        self.stop_worker = False
        self.worker = Thread(target=self._ws_worker)
        self.worker.start()

    def _line_parser(self, line):
        pattern = r"ARD_PACK:(\d+):([ifs]):(.*)$"
        m = re.match(pattern, line)
        if m:
            pack_id, s_type, data = m.groups()
            with self.data_mutex:
                self.main_data[int(pack_id)][type_to_pos[s_type]] = data

    def _ws_worker(self):
        while not self.stop_worker:
            try:
                with connect(self.uri, open_timeout=2, close_timeout=1) as ws:
                    self.ws = ws
                    ws.send(f"connect {self.room}")
                    for line in ws:
                        self._line_parser(line)
                self.ws = None
                time.sleep(0.1)
            except:
                time.sleep(0.5)

    def stop(self):
        while self.worker.is_alive():
            self.stop_worker = True
            if self.ws is not None: self.ws.close()
        try:
            self.data_mutex.release()
        except:
            pass
    
    def select_room(self, room):
        try:
            if(self.ws != None):
                self.ws.send(f"connect {room}")
        except:
            pass

    def send_int(self, buf_id, val):
        try:
            if(self.ws != None):
                self.ws.send(f"ARD_PACK:{buf_id}:i:{val}")
        except:
            pass

    def send_float(self, buf_id, val):
        try:
            if(self.ws != None):
                self.ws.send(f"ARD_PACK:{buf_id}:f:{val}")
        except:
            pass

    def send_string(self, buf_id, val):
        if(len(val) > 8): raise ValueError("max str len 8")
        try:
            if(self.ws != None):
                self.ws.send(f"ARD_PACK:{buf_id}:c:{val}")
        except:
            pass
    
    def get_int(self, buf_id):
        with self.data_mutex:
            return int(self.main_data[buf_id][type_to_pos["i"]])
        
    def get_float(self, buf_id):
        with self.data_mutex:
            return float(self.main_data[buf_id][type_to_pos["f"]])
        
    def get_string(self, buf_id):
        with self.data_mutex:
            return str(self.main_data[buf_id][type_to_pos["s"]])