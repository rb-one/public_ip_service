from .public_ip_driver import PublicIpDriver


class PublicIpManager(PublicIpDriver):
    def process(self):
        """Use the methods in the child an performs the process"""
        super(PublicIpManager, self).process()
        self.get_local_public_ip()
        self.read_stored_local_public_ip()

        if self.current_local_public_ip != self.stored_local_public_ip:
            self.write_current_public_ip()
            self.send_current_local_public_ip_file_by_ssh()
            self.send_current_local_public_ip_file_by_email()
