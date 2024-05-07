# -- coding: utf-8 --
# @Time    : 2023/12/12 11:12
# @Author  : TangKai
# @Team    : ZheChengData

import os
import sys
import time
import pickle
import logging
import datetime
import numpy as np
import pandas as pd
from ..api.WebApi import GdRoutePlan


class RequestOnTime(object):
    def __init__(self, key_list=None, input_file_path=None, od_df: pd.DataFrame = None):
        self.key_list = key_list
        if input_file_path is None:
            self.od_df = od_df
        else:
            self.od_df = pd.read_csv(input_file_path)

    def start_request(self, out_fldr=None, cache_times=2000, id_field=None,
                      file_flag=None, o_x_field='o_x', o_y_field='o_y',
                      d_x_field='d_x', d_y_field='d_y', way_points_field=None,
                      request_hh_field=None, ignore_hh=False, log_fldr: str = None, save_log_file: bool = False,
                      remove_his: bool = True):
        """
        给一个od表, 按照时间进行请求
        :param out_fldr:
        :param cache_times:
        :param id_field:
        :param file_flag:
        :param o_x_field:
        :param o_y_field:
        :param d_x_field:
        :param d_y_field:
        :param way_points_field:
        :param request_hh_field:
        :param ignore_hh:
        :param log_fldr:
        :param save_log_file:
        :param remove_his
        :return:
        """

        # 1. 配置日志输出
        # prj_root_fldr = os.getcwd()
        # if 'log' not in os.listdir(os.path.join(prj_root_fldr, 'data/output/')):
        #     os.makedirs(os.path.join(prj_root_fldr, 'data/output/log/'))

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(
            logging.Formatter('[%(asctime)s %(levelname)s] %(message)s', datefmt='%m/%d/%Y %H:%M:%S'))
        console_handler.setLevel(logging.INFO)

        if log_fldr is not None and save_log_file:
            # file_handler = logging.FileHandler(os.path.join(prj_root_fldr, fr'data/output/log/log_request_{file_flag}.log'),
            #                                    mode='a')
            file_handler = logging.FileHandler(os.path.join(log_fldr, fr'log_request_{file_flag}.log'), mode='a')

            file_handler.setFormatter(
                logging.Formatter('[%(asctime)s %(levelname)s] %(message)s', datefmt='%m/%d/%Y %H:%M:%S'))
            file_handler.setLevel(logging.INFO)
            logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s',
                                handlers=[file_handler, console_handler])
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', handlers=[console_handler])
        logging.info(rf'{file_flag}_logging_info:.....')
        # 日志输出 #

        if remove_his:
            if 'already_request_list' in os.listdir(out_fldr):
                os.remove(os.path.join(out_fldr, 'already_request_list'))
        continue_request = True

        new_file_list = []

        # 恢复请求状态
        num_list = []
        for file_name in os.listdir(out_fldr):
            if 'gd_path' in file_name:
                num_list.append(int(file_name.split('_')[-1]))
        if num_list:
            last_num = max(num_list)
        else:
            last_num = 0

        # 读取已经请求的od_id
        try:
            with open(os.path.join(out_fldr, 'already_request_list'), 'rb') as f:
                already_request_list = pickle.load(f)
        except:
            already_request_list = []

        logging.info(rf'请求{file_flag}, 第{last_num + 1}个文件...')
        logging.info(rf'already_request_list_len: {len(already_request_list)}')

        # 路径规划对象
        route_plan = GdRoutePlan(self.key_list)

        # 开始请求数据
        while continue_request:
            # 删除已经请求的和发生联通错误的......
            self.od_df.drop(index=self.od_df[self.od_df[id_field].isin(already_request_list)].index, inplace=True, axis=0)
            self.od_df.reset_index(drop=True, inplace=True)
            logging.info(rf'尚且未请求的有{len(self.od_df)}条')

            # 如果为空, 说明请求完毕了
            if self.od_df.empty:
                logging.info('全部请求完毕...')
                return True, new_file_list

            # 请求当前时段的数据
            request_hour = datetime.datetime.now().hour
            file_prefix = str(request_hour) + '_' + file_flag
            if ignore_hh:
                request_df = self.od_df.copy()
            else:
                request_df = self.od_df[self.od_df[request_hh_field] == request_hour].copy()
            logging.info(rf'在{request_hour}时段内的有:{len(request_df)}条')
            # 目前没有满足条件的数据
            if request_df.empty:
                time.sleep(100)
                continue

            # 开始请求当前时段的
            od_route_dict, done_list, is_end = self.request_hh_df(request_df=request_df, cache_times=cache_times,
                                                                  request_hh=request_hour,
                                                                  id_field=id_field, o_x_field=o_x_field,
                                                                  o_y_field=o_y_field,
                                                                  d_x_field=d_x_field, d_y_field=d_y_field,
                                                                  way_points_field=way_points_field,
                                                                  route_plan_obj=route_plan, ignore_hh=ignore_hh)

            already_request_list.extend(done_list)
            last_num += 1
            self.save_file(out_fldr=out_fldr, file_flag=file_prefix, last_num=last_num,
                           od_route_dict=od_route_dict, already_request_list=already_request_list)
            new_file_list.append(rf'{file_prefix}_gd_path_{last_num}')

            # 配额达到上限
            if is_end:
                logging.info(rf'开始休眠等待配额恢复...')
                time.sleep(3600)

    @staticmethod
    def request_hh_df(request_df=None, cache_times=None, request_hh=None,
                      id_field=None, o_x_field='o_x', o_y_field='o_y', d_x_field='d_x', d_y_field='d_y',
                      way_points_field=None, route_plan_obj=None, ignore_hh=True):
        """请求给定表的od, 每达到cache_times次(或者在规定时段内没有请求完或者提前请求完或者达到配额上限)就返回"""
        _count = 0  # 用于计数
        od_route_dict = dict()  # 用于存储请求结果
        done_list = []  # 用于存储请求成功的od_id
        not_conn_error_num = 0  # 用于记录搜路失败的od数目
        not_conn_error_list = []  # 用于记录搜路失败的od_id
        http_error_num = 0  # 用于记录网络失败的od数目
        http_error_list = []  # 用于记录网络失败的od_id
        limit_num = 0
        for _, row in request_df.iterrows():
            strategy = None
            is_rnd_strategy = True
            od_id = int(row[id_field])
            o_loc = ','.join([str(np.around(row[o_x_field], decimals=6)), str(np.around(row[o_y_field], 6))])
            d_loc = ','.join([str(np.around(row[d_x_field], decimals=6)), str(np.around(row[d_y_field], 6))])
            if way_points_field in request_df.columns:
                way_points = row[way_points_field]
                if way_points not in [None, '', ' ']:
                    logging.info(rf'启用途径点...')
                    is_rnd_strategy = False
                    strategy = '0'
            else:
                way_points = None
                is_rnd_strategy = True

            json_data, info_code = route_plan_obj.car_route_plan(origin=o_loc, destination=d_loc,
                                                                 od_id=od_id, waypoints_loc=way_points,
                                                                 is_rnd_strategy=is_rnd_strategy, strategy=strategy)
            logging.info(rf'info_code: {info_code}, count: {_count}, od: {od_id}')

            if info_code is not None:
                # 请求成功
                if info_code == 10000:
                    logging.info(r'请求成功')
                    od_route_dict[od_id] = json_data
                    done_list.append(od_id)
                    _count += 1
                elif info_code in [10003]:
                    limit_num += 1
                    if limit_num >= 30:
                        logging.info(r'达到配额上限,结束请求')
                        return od_route_dict, done_list, True
                elif info_code in [20003, 20011, 20012, 20800, 20801, 20802, 20803]:
                    # 其他错误(未知错误, 路径错误......), 这部分不会重复请求
                    logging.info(r'未知错误, 路径错误...')
                    not_conn_error_num += 1
                    not_conn_error_list.append(od_id)
                    done_list.append(od_id)
                    _count += 1
            else:
                # 网络错误
                http_error_num += 1
                http_error_list.append(od_id)

            # 达到请求次数后缓存一次
            if _count >= cache_times:
                logging.info(rf'达到缓存次数..., 返回')
                logging.info(rf'路网不连通导致的失败od数: {len(not_conn_error_list)}')
                logging.info(rf'https网络导致的失败od数: {len(http_error_list)}')
                return od_route_dict, done_list, False

            if ignore_hh:
                pass
            else:
                # 请求完一个后检查时间
                if datetime.datetime.now().hour != request_hh:
                    logging.info(rf'时段超限..., 返回')
                    logging.info(rf'路网不连通导致的失败od数: {len(not_conn_error_list)}')
                    logging.info(rf'https网络导致的失败od数: {len(http_error_list)}')
                    return od_route_dict, done_list, False

        # 既没有达到缓存次数也没有时段超限
        logging.info(rf'od请求完毕, 没有达到配额上限也没有达到缓存次数..., 返回')
        logging.info(rf'路网不连通导致的失败od数: {len(not_conn_error_list)}')
        logging.info(rf'https网络导致的失败od数: {len(http_error_list)}')
        return od_route_dict, done_list, False

    @staticmethod
    def save_file(out_fldr=None, file_flag=None, last_num=None,
                  od_route_dict=None, already_request_list=None):
        with open(os.path.join(out_fldr, rf'{file_flag}_gd_path_{last_num}'), 'wb') as f:
            pickle.dump(od_route_dict, f)
        with open(os.path.join(out_fldr, 'already_request_list'), 'wb') as f:
            pickle.dump(already_request_list, f)
