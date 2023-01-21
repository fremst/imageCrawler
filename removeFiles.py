import ftplib
import os


def get_config_data():
    _config_data = {
        'ftp_ip': None,
        'ftp_port': None,
        'ftp_id': None,
        'ftp_pwd': None,
        'ftp_folder': None,
        'ftp_url': None,
    }
    try:
        with open(os.getcwd() + '/config.dat') as file:
            input_data = file.read().splitlines()
    except FileNotFoundError:
        print('config.dat 파일을 찾을 수 없습니다.')
        exit(0)

    for key in _config_data:
        for elem in input_data:
            if elem.startswith(key):
                _config_data[key] = elem.split(key + ":")[1].strip()
    if ~_config_data['ftp_folder'].endswith('/'):
        _config_data['ftp_folder'] = _config_data['ftp_folder'] + '/'
    if ~_config_data['ftp_url'].endswith('/'):
        _config_data['ftp_url'] = _config_data['ftp_url'] + '/'
    _config_data['ftp_url'] = _config_data['ftp_url'] + _config_data['ftp_folder']
    return _config_data


if __name__ == '__main__':

    config_data = get_config_data()
    session = ftplib.FTP()
    session.connect(config_data['ftp_ip'], int(config_data['ftp_port']))
    session.login(config_data['ftp_id'], config_data['ftp_pwd'])
    session.encoding = 'utf-8'
    file = open(os.getcwd() + '/removeUids.dat', 'r')
    uid = None
    for uid in file.readlines():
        uid = uid.strip()
        try:
            for file_name in session.nlst(config_data['ftp_folder']):
                if file_name.startswith(config_data['ftp_folder'] + uid + '_'):
                    session.delete(file_name)
                    print(file_name + ': 파일 삭제 성공!')
        except Exception as e:
            print('[' + uid + '] 삭제 실패')
            print(e)
    file.close()
