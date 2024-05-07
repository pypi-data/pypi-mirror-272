import psutil
import time
import json
import get_process_name
import sys
import platform
if platform.system == 'Windows':
    import WinPidUtil
import asyncio
import platform
import ctypes


class PidsPerf:

    def __init__(self, process_name, interval=1):
        self.process_name = process_name
        self.interval = interval
        self.processUtil = get_process_name.ProcessName()

    def get_mac_perf(self):
        current_pid = self.processUtil.find_main_process_pid(self.process_name)
        while True:
            minor_cpu_sum = 0
            minor_real_mem_sum = 0
            minor_mem_percent_sum = 0
            minor_thread_count_sum = 0
            current_pids = self.processUtil.get_children_pids(current_pid)  # 获取所有子进程
            current_pids.add(current_pid)  # 将主进程及子进程添加到list中
            pids_process = self.processUtil.get_pids_process(current_pids)  # 获取所有进程
            for process in pids_process:
                try:
                    cpu_percent = process.cpu_percent()
                    process_memory = process.memory_info()
                    mem_percent = u'%.2f' % (process.memory_percent())  # 内存利用率
                    real_mem = round(process_memory.rss / 1024 / 1024, 2)  # 实际内存
                    thread_count = process.num_threads()  # 线程总数
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    cpu_percent = 0
                    mem_percent = 0
                    real_mem = 0
                    thread_count = 0

                # 将性能数据保存到对应PID的数据列表中
                if process.pid == current_pid:  # 主进程数据处理
                    main_cpu = cpu_percent
                    main_real_mem = real_mem
                    main_mem_percent = round(float(mem_percent), 2)
                    main_thread_count = thread_count
                    main_data = {'cpu': main_cpu, 'memory': main_real_mem, 'memory percent': main_mem_percent,
                                 'thread count': main_thread_count}
                    # print('主进程', pid_name, main_cpu, main_real_mem, main_mem_percent, main_thread_count)
                else:  # 子进程数据处理
                    minor_cpu_sum += cpu_percent
                    minor_real_mem_sum += real_mem
                    minor_mem_percent_sum += float(mem_percent)
                    minor_thread_count_sum += thread_count
                # pid_data[process.pid].append((cpu_percent, real_mem, mem_percent, thread_count))
            minor_data = {'cpu': round(float(minor_cpu_sum), 2), 'memory': round(float(minor_real_mem_sum), 2),
                          'memory percent': round(float(minor_mem_percent_sum), 2),
                          'thread count': minor_thread_count_sum}
            # print('其他子进程', pid_name, minor_cpu_sum, minor_real_mem_sum, minor_mem_percent_sum,
            #       minor_thread_count_sum)
            # 获取磁盘IO
            io_read_bytes_start, io_write_bytes_start = self.get_disk_usage()
            time.sleep(self.interval)
            io_read_bytes_end, io_write_bytes_end = self.get_disk_usage()  # io read/write
            io_read_bytes = io_read_bytes_end - io_read_bytes_start  # io read/byte
            io_write_bytes = io_write_bytes_end - io_write_bytes_start  # io write/byte
            disk_data = {'io read': io_read_bytes, 'io write': io_write_bytes}
            data = {'main': main_data, 'other': minor_data, 'disk': disk_data}
            json_data = json.dumps(data)
            print(json_data)
            sys.stdout.flush()

    def get_disk_usage(self):
        '''
        Mac 获取进程磁盘读写情况
        :return:
        '''
        try:
            io_counters = psutil.disk_io_counters()
            io_read_bytes = io_counters.read_bytes
            io_write_bytes = io_counters.write_bytes
            return io_read_bytes, io_write_bytes
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        return 0, 0

    def get_win_perf(self):
        from ctypes import byref
        pidWinPerf = WinPidUtil.PidWinPerformance()
        system_time_pre = pidWinPerf.filetime_to_100nano_seconds(WinPidUtil.FILETIME())
        p_pid = self.processUtil.find_main_process_pid(self.process_name)
        child_pids = self.processUtil.get_children_pids(p_pid)
        child_pids.add(p_pid)  # app内所有pid
        process_cpu_times_pre = {pid: pidWinPerf.get_process_cpu_time(pid) for pid in child_pids}
        process_io_counters_pre = {pid: pidWinPerf.get_io_counters(pid) for pid in child_pids}
        monitor_interval_seconds = 1  # 监控间隔（秒）
        while True:
            minor_cpu_sum = 0
            minor_workSet_mem_sum = 0
            minor_private_mem_sum = 0
            minor_mem_percent_sum = 0
            minor_thread_count_sum = 0
            minor_io_read_sum = 0
            minor_io_write_sum = 0

            current_pids = self.processUtil.get_children_pids(p_pid)  # 获取所有子进程
            current_pids.add(p_pid)  # 将主进程及子进程添加到list中

            start_time = time.time()  # 记录循环开始的时间
            system_idle_time = WinPidUtil.FILETIME()
            system_kernel_time = WinPidUtil.FILETIME()
            system_user_time = WinPidUtil.FILETIME()
            ctypes.windll.kernel32.GetSystemTimes(byref(system_idle_time),
                                                  byref(system_kernel_time),
                                                  byref(system_user_time))
            system_time_post = pidWinPerf.filetime_to_100nano_seconds(
                system_kernel_time) + pidWinPerf.filetime_to_100nano_seconds(system_user_time)

            child_pids = self.processUtil.get_children_pids(p_pid)
            child_pids.add(p_pid)  # app内所有pid

            new_pids_cpu_time_pre = {pid: pidWinPerf.get_process_cpu_time(pid) for pid in child_pids if
                                     pid not in process_cpu_times_pre}
            process_cpu_times_pre.update(new_pids_cpu_time_pre)
            new_process_io_counters_pre = {pid: pidWinPerf.get_io_counters(pid) for pid in child_pids}
            process_io_counters_pre.update(new_process_io_counters_pre)

            # print('----------------------------------------------------------')
            # print('pid', child_pids)
            for pid in child_pids:
                try:
                    process = psutil.Process(pid)
                    pid_name = process.name()
                    mem_percent = round(process.memory_percent(), 2)
                    thread_count = process.num_threads()
                except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
                    # print('pid is not found')
                    mem_percent = 0
                    thread_count = 0

                process_cpu_time_post = pidWinPerf.get_process_cpu_time(pid)
                memory_info = pidWinPerf.get_process_memory(pid)
                io_counters = pidWinPerf.get_io_counters(pid)
                read_bytes_sec = (io_counters.ReadTransferCount - process_io_counters_pre[
                    pid].ReadTransferCount) / monitor_interval_seconds
                write_bytes_sec = (io_counters.WriteTransferCount - process_io_counters_pre[
                    pid].WriteTransferCount) / monitor_interval_seconds
                if process_cpu_time_post:
                    # 计算CPU使用率
                    cpu_usage = round((process_cpu_time_post - process_cpu_times_pre[pid]) / (
                            system_time_post - system_time_pre) * 100, 2)
                    # 更新之前的CPU时间
                    process_cpu_times_pre[pid] = process_cpu_time_post
                    workSet_mem = round(memory_info.WorkingSetSize / 1024 / 1024, 2)  # MB
                    private_mem = round(memory_info.PrivateUsage / 1024 / 1024, 2)  # MB
                    if pid == p_pid:
                        main_data = {'cpu': cpu_usage, 'private': private_mem, "workset": workSet_mem}
                        # print(
                        #     f'主进程数据：cpu：{cpu_usage}，workSet：{workSet_mem}，private：{private_mem}，mem_percent：{mem_percent}，thread_count：{thread_count}')
                    else:
                        minor_cpu_sum += cpu_usage  # 子进程总
                        minor_workSet_mem_sum += workSet_mem  # 子进程workSet内存
                        minor_private_mem_sum += private_mem  # 子进程private内存
                        minor_mem_percent_sum += mem_percent  # 子进程内存使用率
                        minor_thread_count_sum += thread_count  # 子进程线程总数
                    minor_io_read_sum += read_bytes_sec  # 所有进程IO读取速率总数
                    minor_io_write_sum += write_bytes_sec  # 所有进程IO写入速率总数

                else:
                    # print(f"PID {pid}: Process not found or access denied")
                    continue
            disk_data = {'io read': minor_io_read_sum, 'io write': minor_io_write_sum}
            other_data = {'cpu': minor_cpu_sum, 'private': round(float(minor_private_mem_sum), 2),
                          'workset': round(float(minor_workSet_mem_sum), 2),
                          'memory percent': round(float(minor_mem_percent_sum), 2),
                          'thread count': minor_thread_count_sum}
            data = {'main': main_data, 'other': other_data, 'disk': disk_data}
            json_data = json.dumps(data)
            print(json_data)
            sys.stdout.flush()
            # 更新系统时间
            system_time_pre = system_time_post
            # 等待以确保大约每秒更新一次
            elapsed = time.time() - start_time
            time.sleep(max(0, monitor_interval_seconds - elapsed))

    async def start_perf(self):
        if platform.system() == 'Windows':
            await asyncio.gather(self.get_win_perf())
        else:
            await asyncio.gather(self.get_mac_perf())


if __name__ == '__main__':
    processName = 'WXWork.exe'
    perf = PidsPerf(processName)
    asyncio.run(perf.start_perf())
