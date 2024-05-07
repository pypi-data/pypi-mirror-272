# from yplib.index import *
# import threading
#
#
# # all_list   : 所有的线程,需要处理的数据总数
# # thread_num : 线程数量
# # thread_fun : 每个线程需要执行的函数
# def do_thread(all_list=[], thread_num=100, thread_fun=None):
#     # 线程数量
#     t_num = int(thread_num) if thread_num is not None else 10
#     # 所有的线程,需要做的任务总数
#     one_thread_do_num = int(len(all_list) / thread_count) + 1 if int(len(all_list) % thread_count) > 0 else 0
#     for t_i in range(t_num):
#         temp_list = all_list[t_i * one_thread_do_num:(t_i + 1) * one_thread_do_num]
#         ta = threading.Thread(target=do_thread, args=(temp_list, index))
#         ta.start()
#     print('do_thread done')
#
#
# ##############################################################################################################
# from yplib import *
#
#
# # 50 个线程
# def do_thread_fun(do_list=[], index=1):
#     print('do_thread done')
#
#
# sql = "SELECT data FROM tb_data WHERE JSON_EXTRACT(data, '$.type') = 'oss_data_ng' order by id desc limit 1;"
# id_list = json.loads(get_data_from_sql(sql=sql, db_config='dev_db')[0][0])['data']
#
# print('start')
# print(len(id_list))
# # 线程数量
# thread_count = 100
# # 所有的线程,需要做的任务总数
#
# one_thread_do_num = int(len(id_list) / thread_count) + 1 if int(len(id_list) % thread_count) > 0 else 0
#
# print(one_thread_do_num)
# for i in range(one_thread_do_num):
#     temp_list = id_list[use_length: use_length + 100]
#     ta = threading.Thread(target=do_thread, args=(temp_list, index))
#     ta.start()
#
# print('end')
