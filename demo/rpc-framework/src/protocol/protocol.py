class Protocol:
    @staticmethod
    def serialize_request(method, params):
        return f"METHOD:{method};PARAMS:{','.join(map(str, params))}"

    @staticmethod
    def deserialize_request(data):
        parts = data.split(';')
        method = parts[0].split(':')[1]
        params = list(map(int, parts[1].split(':')[1].split(',')))
        return method, params

    @staticmethod
    def serialize_response(result=None, error=None):
        if error:
            return f"ERROR:{error}"
        return f"RESULT:{result}"

    @staticmethod
    def deserialize_response(data):
        if data.startswith("ERROR:"):
            return None, data.split(':')[1]
        return int(data.split(':')[1]), None