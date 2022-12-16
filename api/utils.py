from flask_restx import reqparse


class RequestParser(reqparse.RequestParser):

    def __init__(self, argument_class=reqparse.Argument,
                 result_class=reqparse.ParseResult, arguments={}):
        super().__init__(argument_class=reqparse.Argument,
                         result_class=reqparse.ParseResult)
        self.add_arguments(arguments)
        return

    def add_argument(self, *args, **kwargs):
        return super().add_argument(*args, store_missing=False, **kwargs)

    def add_arguments(self, args):
        for key, value in args.items():
            self.add_argument(key, **value)
