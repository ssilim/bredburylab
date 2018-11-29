import time as ctime
from jim.config import *
from jim.exceptions import *
from errors import MandatoryKeyError, ResponseCodeError, ResponseCodeLenError, UsernameToLongError

class MaxLenghtField:
    # Дескриптор проверки длинны полей
    def __init__(self, name, max_len):
        self.name = '_' + name
        self.max_len = max_len

    def __set__(self, instance, value):
        if len(value) > self.max_len:
            raise ToLongError(self.name, value, self.max_len)
        else:
            setattr(instance, self.name, value)

    def __get__(self, instance, owner):
        getattr(instance, self.name)


class Jim:
    def to_dict(self):
        return {}

    @staticmethod
    def try_create(jim_class, input_dict):
        try:
            # JimMessage(**input_dict)
            return jim_class(**input_dict)
        except KeyError:
            raise WrongParamsError(input_dict)

    @staticmethod
    def from_dict(input_dict):

        # должно быть response или action
        # если action
        if ACTION in input_dict:
            # достаем действие
            action = input_dict.pop(ACTION)
            # действие должно быть в списке действий
            if action in ACTIONS:
                if action == PRESENCE:
                    return Jim.try_create(JimPresence, input_dict)
                elif action == MSG:
                    try:
                        input_dict['from_'] = input_dict['from']
                    except KeyError:
                        raise WrongParamsError(input_dict)
                    del input_dict['from']
                    return Jim.try_create(JimMessage, input_dict)
            else:
                raise WrongActionError(action)
        elif RESPONSE in input_dict:
            return Jim.try_create(JimResponse, input_dict)
        else:
            raise WrongDictError(input_dict)


class JimAction(Jim):

    def __init__(self, action, time=None):
        self.action = action
        if time:
            self.time = time
        else:
            self.time = ctime.time()


    def to_dict(self):
        result = super().to_dict()
        result[ACTION] = self.action
        result[TIME] = self.time
        return result


class JimMessage(JimAction):
    to = MaxLenghtField('to', USERNAME_MAX_LENGTH)
    from_ = MaxLenghtField('from', USERNAME_MAX_LENGTH)
    message = MaxLenghtField('message', MESSAGE_MAX_LENGTH)

    def __init__(self, to, from_, message, time=None):
        self.to = to
        self.from_ = from_
        self.message = message
        super().__init__(MSG, time=time)

    def to_dict(self):
        result = super().to_dict()
        result[TO] = self.to
        result[FROM] = self.from_
        result[MESSAGE] = self.message
        return result


class JimPresence(JimAction):
    def __init__(self, accoint_name, time=None):
        self.account_name = accoint_name
        super().__init__(PRESENCE, time)

    def to_dict(self):
        result = super().to_dict()
        result[ACCOUNT_NAME] = self.account_name
        return result


class ResponceField:
    def __init__(self, name):
        self.name = '_' + name

    def __set__(self, instance, value):
        if value not in RESPONSE_CODES:
            raise ResponseCodeError(value)
        setattr(instance, self.name, value)

    def __get__(self, instance, owner):
        getattr(instance, self.name)



class JimResponse(Jim):
    def __init__(self, response, error=None, alert=None):
        self.response = response
        self.error = error
        self.alert = alert

    def to_dict(self):
        result = super().to_dict()
        result[RESPONSE] = self.response
        if self.error:
            result[ERROR] = self.error
        if self.alert:
            result[ALERT] = self.alert
        return result