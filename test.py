import libtmux
import os
import time
server = libtmux.Server()
session = server.new_session(session_name="session_test", kill_session=True, attach=False)
session = server.find_where({"session_name": "session_test"})
window = session.new_window(attach=True, window_name="session_test")

pane1 = window.attached_pane
#pane2 = window.split_window(vertical=True)
#.select_layout('even-horizontal')
pane1.send_keys('./build/examples/accel_perf -w copy -q 16 -o 131072 -m 0x1 -t 5 --wait-for-rpc;sleep 10;')
#pane2.send_keys('./scripts/rpc.py idxd_scan_accel_engine -c 0')
#pane2.send_keys('./scripts/rpc.py framework_start_init')
#pane1.send_keys('tmux kill-session -t session_test')

time.sleep(5)
os.system("./scripts/rpc.py idxd_scan_accel_engine -c 0")
os.system("./scripts/rpc.py framework_start_init")

server.attach_session(target_session="session_test")
