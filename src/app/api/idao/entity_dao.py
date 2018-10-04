class IDao(object):
    def add(self, **kwargs):
        raise NotImplementedError()

    def find(self,  **kwargs):
        raise NotImplementedError()

    def find_all(self,  **kwargs):
        raise NotImplementedError()
