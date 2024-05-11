from cloudframework.RESTFul import RESTFul
class API(RESTFul):

    def main(self):

        # You can control CORS Access
        if not self.sendCorsHeaders('GET'): return

        # region GET endpoint from self.params. 'default' by default
        endpoint = "default"
        if self.params: endpoint = self.params[0]
        # endregion

        # region call ENDPOINT_+endpoint()
        if callable(getattr(self, "ENDPOINT_"+endpoint.replace('-', '_'))):
            eval('self.ENDPOINT_'+endpoint.replace('-', '_')+'()')
        else:
            return self.setErrorFromCodeLib('not-found', '/'+self.core.system.url['parts'][0]+'/'+endpoint+' does not exist')
        # endregion

    def ENDPOINT_default(self):
        """
        Default return data
        :return:
        """
        self.addReturnData('Hello World')
