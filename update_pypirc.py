import os
import os.path
from argparse import ArgumentParser
import ConfigParser

PASSWORD = 'password'
USERNAME = 'username'
REPOSITORY = 'repository'
INDEX_SERVERS = 'index-servers'
DISTUTILS = 'distutils'


class UpdatePypircRequest(object):
    def __init__(self, package_index, repository, username, password):
        self.package_index = package_index
        self.repository = repository
        self.username = username
        self.password = password


def _set_servers_in_config(pypirc_config, pypirc_request, servers):
    if pypirc_request.package_index not in servers:
        servers.append(pypirc_request.package_index)
    pypirc_config.set(DISTUTILS, INDEX_SERVERS, '\n'.join(servers))


def _set_index_server_section(pypirc_config, pypirc_request):
    if pypirc_request.package_index not in pypirc_config.sections():
        pypirc_config.add_section(pypirc_request.package_index)
    pypirc_config.set(pypirc_request.package_index, REPOSITORY, pypirc_request.repository)
    pypirc_config.set(pypirc_request.package_index, USERNAME, pypirc_request.username)
    pypirc_config.set(pypirc_request.package_index, PASSWORD, pypirc_request.password)


def _save_config_file(pypirc_config, pypirc_path):
    pypirc_file = open(pypirc_path, 'w')
    pypirc_config.write(pypirc_file)
    pypirc_file.close()


def _get_servers_from_config(pypirc_config):
    if INDEX_SERVERS not in pypirc_config.options(DISTUTILS):
        return []

    index_servers = pypirc_config.get(DISTUTILS, INDEX_SERVERS)
    return [server.strip() for server in
            index_servers.split('\n')
            if server.strip() != '']


def _parse_args_to_update_pypirc_request():
    parser = ArgumentParser()
    parser.add_argument('index_server', type=str, help='Python Package Index server name, i.e. pypi, pypitest, other')
    parser.add_argument('repository', type=str, help='Python Package Index URL, i.e. https://pypi.python.org/pypi')
    parser.add_argument('username', type=str, help='Python Package Index username')
    parser.add_argument('password', type=str, help='Python Package Index password')
    parse_result = parser.parse_args()
    return UpdatePypircRequest(parse_result.index_server, parse_result.repository, parse_result.username,
                               parse_result.password)


def _get_rc_file():
    """Returns rc file path."""
    return os.path.join(os.path.expanduser('~'), '.pypirc')


def main():
    pypirc_request = _parse_args_to_update_pypirc_request()
    pypirc_path = _get_rc_file()

    pypirc_config = ConfigParser.ConfigParser()

    if os.path.isfile(pypirc_path):
        pypirc_config.read(pypirc_path)

    if DISTUTILS not in pypirc_config.sections():
        pypirc_config.add_section(DISTUTILS)

    servers = _get_servers_from_config(pypirc_config)

    _set_servers_in_config(pypirc_config, pypirc_request, servers)

    _set_index_server_section(pypirc_config, pypirc_request)

    _save_config_file(pypirc_config, pypirc_path)


if __name__ == "__main__":
    main()
