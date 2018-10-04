class IBusinessService(object):

    def post(self, **kwargs):
        raise NotImplementedError()

    def get(self, **kwargs):
        raise NotImplementedError()
