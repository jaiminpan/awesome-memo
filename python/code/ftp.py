#!/usr/bin/env python
#coding=utf-8

import ftplib
import os

import logging

LOG = logging.getLogger()

class FtpDriver(object):
    """ftp class for file manipulation."""

    def __init__(self, conf={}):
        """Constructor."""
        self.host = conf.get('host', None)
        self.port = conf.get('port', 21)
        self.username = conf.get('username', None)
        self.password = conf.get('password', None)
        self.timeout = conf.get('timeout', 999)
        self.buffer_size = conf.get('buffer_size', 8*1024)
        self.read_size = conf.get('read_size', 1024*1024)
        self.mode = conf.get('mode', 'port')  # or passive

        self.ftp = None

    def connect(self):
        """connect to ftp server."""

        if self.ftp:
            LOG.warn("ftp instance exist, no need to connect.")
            return

        try:
            ftp = ftplib.FTP()
            ftp.connect(self.host, self.port, self.timeout)
            msg = '[Ftp--conncet] conncet success! \
                host: %(host)s ,port: %(port)s and timeout: %(timeout)s' \
                % {'host': self.host, 'port': self.port, 'timeout': self.timeout}
            LOG.debug(msg)
        except Exception as e:
            err_msg = '[Ftp--conncet] conncet failed! \
                host: %(host)s ,port: %(port)s and timeout: %(timeout)s' \
                % {'host': self.host, 'port': self.port, 'timeout': self.timeout}
            LOG.error(err_msg)
            LOG.error("[Ftp--conncet] conncet failed error msg - %s" % e)
            raise e
        else:
            try:
                ftp.login(self.username, self.password)
                ftp.set_pasv(self.mode != 'port')
                LOG.debug('[Ftp--login] login success! username: %(username)s'
                          % {'username': self.username})
            except Exception as e:
                LOG.error('[Ftp--login] login failed! username: %(username)s,'
                          'password: %(password)s'
                          % {'username': self.username, 'password': self.password})
                LOG.error('[Ftp--login] login failed error msg - %s' % e)
                raise e
            else:
                self.ftp = ftp

    def disconnect(self):
        """disconnect from ftp server."""

        if self.ftp:
            self.ftp.quit()
            LOG.debug('[Ftp--disconnect] disconnect success!')
            self.ftp = None
        else:
            msg = '[Ftp--disconnect] disconnect failed! ftp not found'
            self._exception_handler(msg)

    def is_connect(self):
        return self.ftp is not None

    def upload(self, breakpoint=False, **kwargs):
        """upload file to ftp server."""

        if self.ftp:
            # filepath = kwargs.get('filepath', None)
            local_path = kwargs.get('local_path', None)
            # remote_path = kwargs.get('remote_path', None)

            # if file exists
            if not local_path:
                msg = '[Ftp--upload] local file path is None'
                LOG.error(msg)
                raise KeyError(msg)
            if not os.path.exists(local_path):
                msg = '[Ftp--upload] local file does not exists'
                self._exception_handler(msg)

            file_name = local_path

            if local_path:
                local = self._split_path(local_path)
                file_name = local[1]

            remote_file = file_name

            '''
            if remote_path :
                remote = self._split_path(remote_path)
                remote_dir = remote[0]

                if remote_dir :
                    try :
                        self.ftp.cwd(remote_dir)
                    except ftplib.error_perm as err :
                        print '[Ftp--upload] Failed to change directory. \
                            remote directory: %(remote_dir)s' % {'remote_dir': remote_dir}
                        print '[Ftp--upload] upload failed error msg - %s' % err
                        raise  err

                if remote[1] :
                    remote_file = remote[1]
            '''

            if not breakpoint:
                self._normal_upload(file_path=local_path,
                                    file_name=remote_file)
            else:
                self._breakpoint_upload(file_path=local_path,
                                        file_name=remote_file,
                                        callback=None)
            LOG.debug('[Ftp--upload] upload success!')
        else:
            msg = '[Ftp--upload] upload failed! ftp not found'
            self._exception_handler(msg)

    def _normal_upload(self, file_path, file_name):
        LOG.info('[Ftp--upload--normal] upload file begin, using normal mode,'
                 ' file_path: %(file_path)s, file_name: %(file_name)s'
                 % {'file_path': file_path, 'file_name': file_name})

        f = open(file_path, "rb")
        #file_name = os.path.split(file_path)[-1]
        try:
            self.ftp.storbinary('STOR %s'%file_name, f, self.buffer_size)
        except ftplib.error_perm as err:
            LOG.error('[Ftp--upload--normal] upload failed!'
                      'file_path: %(file_path)s'
                      % {'file_path': file_path})
            LOG.error('[Ftp--upload--normal] upload failed error msg - %s' % err)
            raise  err

        LOG.info('[Ftp--upload--normal] upload file end, using normal mode,'
                 'file_path: %(file_path)s, file_name: %(file_name)s'
            % {'file_path': file_path, 'file_name': file_name})

    def _breakpoint_upload(self, file_path, file_name, callback=None):
        LOG.info('[Ftp--upload--breakpoint] upload file begin, using '
                 'breakpoint mode,file_path: '
                 '%(file_path)s, file_name: %(file_name)s'
                 % {'file_path': file_path, 'file_name': file_name})

        remote_file = file_name
        remote_file_size = 0L
        try :
            remote_file_size = self.ftp.size(remote_file)
        except Exception as e:
            pass

        if remote_file_size is None:
            remote_file_size = 0L

        local_file_size = os.stat(file_path).st_size
        LOG.debug('[Ftp--upload--breakpoint] uploading file, using '
                  'breakpoint mode, remote_file_size: %(remote_file_size)s, '
                  'local_file_size: %(local_file_size)s'
                  % {'remote_file_size': remote_file_size,
                     'local_file_size': local_file_size})

        if remote_file_size == local_file_size :
            LOG.debug('[Ftp--upload--breakpoint] uploading file, remote '
                      'file size is equal with local file size, '
                      'remote_file_size: %(remote_file_size)s, '
                      'local_file_size: %(local_file_size)s'
                      % {'remote_file_size': remote_file_size,
                         'local_file_size': local_file_size})
            return

        if remote_file_size < local_file_size:
            local_file = open(file_path, 'rb')
            local_file.seek(remote_file_size)
            self.ftp.voidcmd('TYPE I')
            data_sock = ''
            esize = ''
            try:
                LOG.debug('[Ftp--upload--breakpoint] uploading file,'
                          ' remote_file: %(remote_file)s'
                          % {'remote_file': remote_file})
                data_sock, esize = self.ftp.ntransfercmd("STOR "+remote_file,
                                                         remote_file_size)

            except Exception as e:
                msg = '[Ftp--upload--breakpoint] uploading file, ftp.ntransfercmd ' \
                      'throws exception, error msg - %s' % e
                self._exception_handler(msg)

            cmp_size = remote_file_size
            while True:
                buf = local_file.read(self.read_size)
                if not len(buf):
                    LOG.debug('[Ftp--upload--breakpoint] no data break')
                    break
                data_sock.sendall(buf)
                if callback:
                    callback(buf)
                cmp_size += len(buf)
                LOG.debug('[Ftp--upload--breakpoint] uploading %.2f%%'
                          % (float(cmp_size)/local_file_size*100))
                if cmp_size == local_file_size:
                    LOG.debug('[Ftp--upload--breakpoint] upload finish, '
                              ' remote_file: %(remote_file)s'
                              % {'remote_file': remote_file})
                    break
            data_sock.close()
            LOG.debug('[Ftp--upload--breakpoint] close data handle')
            local_file.close()
            LOG.debug('[Ftp--upload--breakpoint] close local file handle')
            self.ftp.voidcmd('NOOP')
            LOG.debug('[Ftp--upload--breakpoint] keep alive cmd success')
            self.ftp.voidresp()
            LOG.debug('[Ftp--upload--breakpoint] No loop cmd')

        LOG.info('[Ftp--upload--breakpoint] upload file end, using breakpoint mode,'
                 ' file_path: %(file_path)s, file_name: %(file_name)s'
                 % {'file_path': file_path, 'file_name': file_name})

    def download(self, breakpoint=False, local_path="", remote_path=""):
        """download file from ftp server."""
        if self.ftp:
            #filepath = kwargs.get('filepath', None)
            # local_path = kwargs.get('local_path', None)
            # remote_path = kwargs.get('remote_path', None)

            LOG.debug("called to download local_path[%s] remote_path[%s]"
                      % (local_path, remote_path))
            # if file exists
            if not remote_path:
                msg = '[Ftp--download] remote file path is None'
                LOG.error(msg)
                raise KeyError(msg)

            file_name = remote_path

            if remote_path:
                remote = self._split_path(remote_path)
                if remote[1]:
                    file_name = remote[1]

            local_file = file_name

            if not self._remote_file_exists(file_name):
                msg = '[Ftp--download] remote file does not exists'
                self._exception_handler(msg)

            if local_path:
                local = self._split_path(local_path)
                local_dir = local[0]
                local_file_name = local[1]

                if local_dir:
                    if not os.path.exists(local_dir):
                        msg = '[Ftp--download] local directory does not exists, \
                            local directory: %(local_dir)s' % {'local_dir': local_dir}
                        self._exception_handler(msg)

                if not local_file_name:
                    local_file = local_dir + file_name
                else:
                    local_file = local_path
            try:
                if not breakpoint:
                    self._normal_download(file_path=local_file, file_name=file_name)
                else:
                    self._breakpoint_download(file_path=local_file, file_name=file_name,
                                              callback=None)
            except Exception as e:
                LOG.error("download failed.[%s]" % e.message)
                self.disconnect()

            LOG.debug('[Ftp--download] download success!')

        else:
            msg = '[Ftp--download] download failed ! ftp not connected.'
            self._exception_handler(msg)

    def _normal_download(self, file_path, file_name):
        LOG.info("[Ftp--download--normal] download file begin, using normal mode,"
                 "file_path: %(file_path)s, file_name: %(file_name)s"
                 % {'file_path': file_path, 'file_name': file_name})

        f = open(file_path, "wb").write
        try:
            self.ftp.retrbinary("RETR %s"%file_name, f, self.buffer_size)
        except ftplib.error_perm as err:
            LOG.error('[Ftp--download--normal] download failed! '
                      'file_path: %(file_path)s' % {'file_path': file_path})
            LOG.error('[Ftp--download--normal] download failed error msg - %s' % err)
            raise err

        LOG.info('[Ftp--download--normal] download file end, using normal mode,'
                 'file_path: %(file_path)s, file_name: %(file_name)s'
                 % {'file_path': file_path, 'file_name': file_name})

    def _breakpoint_download(self, file_path, file_name, callback=None):
        LOG.info('[Ftp--download--breakpoint] download file begin, using breakpoint mode, '
                 'file_path: %(file_path)s, file_name: %(file_name)s'
                 % {'file_path': file_path, 'file_name': file_name})

        remote_file_size = self.get_file_size(file_name)
        if not remote_file_size :
            remote_file_size = 0L

        # check local file isn't exists and get the local file size
        local_file_size = 0L
        if os.path.exists(file_path):
            local_file_size = os.stat(file_path).st_size

        if local_file_size > remote_file_size:
            LOG.debug('[Ftp--download--breakpoint] downloading file, '
                      'local file is bigger than remote file, '
                      'delete the old local file. '
                      ' file_path: %(file_path)s, file_name: %(file_name)s'
                      % {'file_path': file_path, 'file_name': file_name})
            os.remove(file_path)
            local_file_size = 0L

        if remote_file_size == local_file_size:
            LOG.debug('[Ftp--download--breakpoint] downloading file, '
                      'remote file size is equal with local file size, '
                      'remote_file_size: %(remote_file_size)s, '
                      'local_file_size: %(local_file_size)s'
                      % {'remote_file_size': remote_file_size,
                         'local_file_size': local_file_size})
            return

        cmp_size = local_file_size
        self.ftp.voidcmd('TYPE I')
        conn = self.ftp.transfercmd('RETR '+file_name, local_file_size)
        local_write = open(file_path, 'ab')
        while True:
            data = conn.recv(self.buffer_size)
            if not data:
                break
            local_write.write(data)
            cmp_size += len(data)
            LOG.debug('[Ftp--download--breakpoint] downloading %.2f%%'
                      % (float(cmp_size)/remote_file_size*100))

        conn.close()
        LOG.debug('[Ftp--download--breakpoint] close data connection')
        local_write.close()
        LOG.debug('[Ftp--download--breakpoint] close local file write')
        self.ftp.voidcmd('NOOP')
        LOG.debug('[Ftp--download--breakpoint] keep alive cmd success')
        self.ftp.voidresp()
        LOG.debug('[Ftp--download--breakpoint] No loop cmd')

        LOG.info('[Ftp--download--breakpoint] download file end, '
                 'using breakpoint mode, file_path: %(file_path)s, '
                 'file_name: %(file_name)s'
                 % {'file_path': file_path, 'file_name': file_name})

    def get_list(self):
        """get list file from ftp server."""
        return self.ftp.nlst()

    def get_list_detail(self):
        """get list file detail from ftp server."""
        return self.ftp.dir()

    def file_exists(self, file_name):
        """whether a file exists in the ftp server."""
        self._remote_file_exists(file_name=file_name)

    def get_file_size(self, file_name):
        """get the file size from the ftp server."""
        return self.ftp.size(file_name)

    def _split_path(self, path):
        position=path.rfind('/')
        return (path[:position+1], path[position+1:])

    def _remote_file_exists(self, file_name):
        file_list = self.ftp.nlst()
        for remote_file_name in file_list :
            if remote_file_name == file_name :
                return True

        return False

    def _exception_handler(self, msg):
        LOG.error(msg)
        raise FtpException(msg)

    def test(self):
        print 'dir: ', self.ftp.dir()
        print 'nlst: ', self.ftp.nlst()

class FtpException(Exception):
    message = "unknow ftp exception"

    def __init__(self, _message=None):
        if _message:
            self.message = _message

        super(FtpException, self).__init__(self.message)


if __name__ == '__main__':
    testconf = {
        'host': "localhost",
        'port': "21",
        'username': "test",
        'password': "test"
    }
    ftp_driver = FtpDriver(conf=testconf)
    #ftp_driver = FtpDriver(host='localhost', port=21, username='test', password='test', timeout=600)
    ftp_driver.connect()
    ftp_driver.upload(breakpoint=False, local_path='/home/test/aa')
    #ftp_driver.upload(breakpoint=False, local_path='/home/eclipse-jee-luna-SR2-linux-gtk-x86_64.tar.gz')
    ftp_driver.download(breakpoint=True, remote_path='/home/test/aaa', local_path='/home/test/dow')
    #ftp_driver.test()
    #print ftp_driver.get_file_size('aaa')
    #print ftp_driver.get_list()
    #print ftp_driver.get_list_detail()
    ftp_driver.disconnect()
