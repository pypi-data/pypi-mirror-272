from ..universal_utils import server_exists, query_server_info, load_commands_from_config, match_command, text_response, config


from . import utils


def handler(message, user_id, platform, channel_id):
    if config.features.get('car_number_forwarding'):
        status = utils.submit_car_number_msg(message, user_id, platform)
        if status:
            return None
    # 进行 v2 api 命令匹配
    command_matched, api = match_command(message, load_commands_from_config(config.commands))
    if command_matched:
        return utils.v2_api_command(message, command_matched, api, platform, user_id, channel_id)

    # 玩家状态
    if config.features.get('player_status', True):
        if message.endswith('服玩家状态'):
            # 如果匹配 *服玩家状态 则查询对应服务器的玩家状态 前提是用户输入的 * 是一个有效的服务器名 否则返回None
            return utils.player_status(user_id, platform, r_) if server_exists(r_ := query_server_info(message[:-4])) else text_response('未找到服务器') if len(message) <= 7 else None

        if message.startswith('玩家状态'):
            # 如果匹配 玩家状态 则查询默认服务器的玩家状态 如果用户输入了服务器名 则查询对应服务器的玩家状态，如果服务器名无效则返回None
            return utils.player_status(user_id, platform) if (arg_ := message[4:].strip()) == '' else (utils.player_status(user_id, platform, r_) if server_exists(r_ := query_server_info(arg_)) else None)

    # 绑定玩家
    if config.features.get('bind_player', True):
        if message.startswith('绑定玩家'):
            # 如果匹配 绑定玩家 则绑定默认服务器的玩家 如果用户输入了服务器名 则绑定对应服务器的玩家，如果服务器名无效则 赋值为 None
            server = utils.get_user_data(platform, user_id)['data']['server_mode'] if message[4:].strip() == '' else (r_ if server_exists(r_ := query_server_info(message[4:])) else None)
            if not server_exists(server):
                return text_response(f'未找到名为 {(message[4:]).strip()} 的服务器信息，请确保输入的是服务器名而不是玩家ID，通常情况发送"绑定玩家"即可')

            res = utils.bind_player_request(platform, user_id, server, True)

            if res.get('status') != 'success':
                # {'status': 'success', 'data': {'verifyCode': 12492}}
                return text_response(res.get('data'))
            # if not res.get('status') == 'failed':
            #     return text_response('未知错误喵')
            return text_response(f'''正在绑定账号，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{res.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证 + 空格 + 玩家ID 来完成本次身份验证\n验证 10000xxxx 国服''')

        if message.startswith('解除绑定'):
            server = utils.get_user_data(platform, user_id)['data']['server_mode'] if message[4:].strip() == '' else (r_ if (config._server_list(r_ := query_server_info(message[4:]))) else None)
            if server_exists(server) is False:
                return text_response(f'未找到名为 {(message[4:]).strip()} 的服务器信息，请确保输入的是服务器名而不是玩家ID，通常情况发送"绑定玩家"即可')
            response = utils.bind_player_request(platform, user_id, server, False)  # 获取响应
            if response.get('status') == 'failed':  # 检查状态
                return text_response(response.get('data'))
            # 如果是200
            return text_response(f'''正在解除，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{response.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证解绑 {server}\n来完成本次身份验证(没错只需要加上 {server} 来确定需要解绑的服务器)''')

        if message.startswith('验证解绑'):
            if not message[4:].strip().isdigit():
                return text_response('请输入解绑时提供的serverID(数字)')
            r = utils.bind_player_verification(platform, user_id, int(message[4:].strip()), utils.get_user_data(platform, user_id)['data']['server_list'][int(message[4:].strip())]['playerId'], False)
            if r.get('status') == 'failed':
                return text_response(r.get('data'))
            return text_response('解绑成功')

        if message.startswith('验证'):
            if not message[2:].strip().isdigit():
                return text_response('请输入正确的玩家ID(数字)')
            if r := utils.bind_player_verification(platform, user_id, utils.get_user_data(platform, user_id)['data']['server_mode'], message[2:].strip(), True).get('status') == 'failed':
                return text_response(r.get('data')) if r.get('data') != '错误: 未请求绑定或解除绑定玩家' else None
            return text_response('绑定成功！现在可以使用"玩家状态"来查询玩家信息')

    # 车牌转发控制
    if config.features.get('switch_car_forwarding', True):
        if message in ['开启车牌转发', '开启个人车牌转发']:
            r = utils.set_car_forward(platform, user_id, True)
            return text_response('已开启车牌转发') if r.get('status') == 'success' else None

        if message in ['关闭车牌转发', '关闭个人车牌转发']:
            r = utils.set_car_forward(platform, user_id, False)
            return text_response('已关闭车牌转发') if r.get('status') == 'success' else None

    # 切换服务器模式
    if config.features.get('change_main_server', True):
        if message.endswith('服模式'):
            if server_exists(r_ := query_server_info(message[:-2])) is False:
                return text_response('未找到服务器') if len(message) <= 5 else None
            if r := utils.set_server_mode(platform, user_id, message[:-2]).get('status') == 'success':
                return text_response('已切换为' + message[:-2] + '模式')
            return text_response(r.get('data')) if len(message) <= 5 else None

        if message.startswith('主服务器'):
            if server_exists(r_ := query_server_info(message[4:].strip())) is False:
                return text_response('未找到服务器') if len(message) <= 7 else None
            if r := utils.set_server_mode(platform, user_id, message[4:].strip()).get('status') == 'success':
                return text_response('主服务器已切换为' + message[4:].strip())
            return text_response(r.get('data')) if ' ' in message else None

    # 设置默认服务器列表
    if config.features.get('change_server_list', True):
        if message.startswith('设置默认服务器'):
            for i in message[7:].strip().split(' '):
                if server_exists(r_ := query_server_info(i)) is False:
                    return text_response(f'未找到服务器 {i}')
            if r := utils.set_default_server(platform, user_id, message[6:].strip()).get('status') == 'success':
                return text_response('默认服务器已设置为' + message[6:].strip())
            return text_response(r.get('data')) if ' ' in message else None

    return None


