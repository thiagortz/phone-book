class IValidation(object):
    def draft4_validate(self, **kwargs):
        raise NotImplementedError()

    def validate(self, **kwargs):
        raise NotImplementedError()
