#!/bin/env python
# -*- coding: UTF-8 -*-


from multiprocessing import Process, Queue



"""启动监听文件更改"""
def start_watch_file_changes(q,path_to_watch):

    import os    
    import win32file
    import win32con
    
    FILE_LIST_DIRECTORY = 0x0001
    
    hDir = win32file.CreateFile (
      path_to_watch,
      FILE_LIST_DIRECTORY,
      win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
      None,
      win32con.OPEN_EXISTING,
      win32con.FILE_FLAG_BACKUP_SEMANTICS,
      None
    )
    while 1:
        
      results = win32file.ReadDirectoryChangesW (
        hDir,
        10240,
        True,
        win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
         win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
         win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
         win32con.FILE_NOTIFY_CHANGE_SIZE |
         win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
         win32con.FILE_NOTIFY_CHANGE_SECURITY,
        None,
        None
      )
      for action, file in results:
        full_filename = os.path.join (path_to_watch, file)
        q.put((action,full_filename))

    


    
    

def main():
    file_changes_q = Queue()
    # 启动监听线程。
    p = Process(target=start_watch_file_changes, args=(file_changes_q,".",))
    p.start()
    while 1:
        print file_changes_q.get()


    

if __name__ == "__main__":
    main()
