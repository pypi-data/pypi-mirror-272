# coding: utf-8

"""
    FINTER API

    ## Finter API Document 1. Domain   - production      - https://api.finter.quantit.io/   - staging      - https://staging.api.finter.quantit.io/  2. Authorization <br><br/>(1) 토큰 발급<br/>curl -X POST https://api.finter.quantit.io/login -d {'username': '{finter_user_id}', 'password': '{finter_user_password}'<br> (2) username, password 로그인 (swagger ui 이용 시)<br/>  # noqa: E501

    OpenAPI spec version: 0.298
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class FlexibleFundFields(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'exchange': 'str',
        'universe': 'str',
        'instrument_type': 'str',
        'freq': 'str',
        'position_type': 'str',
        'nickname': 'str',
        'author': 'str',
        'valid_from': 'int',
        'insample': 'str',
        'updated': 'datetime'
    }

    attribute_map = {
        'exchange': 'exchange',
        'universe': 'universe',
        'instrument_type': 'instrument_type',
        'freq': 'freq',
        'position_type': 'position_type',
        'nickname': 'nickname',
        'author': 'author',
        'valid_from': 'valid_from',
        'insample': 'insample',
        'updated': 'updated'
    }

    def __init__(self, exchange=None, universe=None, instrument_type=None, freq=None, position_type=None, nickname=None, author=None, valid_from=None, insample=None, updated=None):  # noqa: E501
        """FlexibleFundFields - a model defined in Swagger"""  # noqa: E501
        self._exchange = None
        self._universe = None
        self._instrument_type = None
        self._freq = None
        self._position_type = None
        self._nickname = None
        self._author = None
        self._valid_from = None
        self._insample = None
        self._updated = None
        self.discriminator = None
        self.exchange = exchange
        self.universe = universe
        if instrument_type is not None:
            self.instrument_type = instrument_type
        if freq is not None:
            self.freq = freq
        if position_type is not None:
            self.position_type = position_type
        self.nickname = nickname
        self.author = author
        self.valid_from = valid_from
        if insample is not None:
            self.insample = insample
        if updated is not None:
            self.updated = updated

    @property
    def exchange(self):
        """Gets the exchange of this FlexibleFundFields.  # noqa: E501


        :return: The exchange of this FlexibleFundFields.  # noqa: E501
        :rtype: str
        """
        return self._exchange

    @exchange.setter
    def exchange(self, exchange):
        """Sets the exchange of this FlexibleFundFields.


        :param exchange: The exchange of this FlexibleFundFields.  # noqa: E501
        :type: str
        """
        if exchange is None:
            raise ValueError("Invalid value for `exchange`, must not be `None`")  # noqa: E501

        self._exchange = exchange

    @property
    def universe(self):
        """Gets the universe of this FlexibleFundFields.  # noqa: E501


        :return: The universe of this FlexibleFundFields.  # noqa: E501
        :rtype: str
        """
        return self._universe

    @universe.setter
    def universe(self, universe):
        """Sets the universe of this FlexibleFundFields.


        :param universe: The universe of this FlexibleFundFields.  # noqa: E501
        :type: str
        """
        if universe is None:
            raise ValueError("Invalid value for `universe`, must not be `None`")  # noqa: E501

        self._universe = universe

    @property
    def instrument_type(self):
        """Gets the instrument_type of this FlexibleFundFields.  # noqa: E501


        :return: The instrument_type of this FlexibleFundFields.  # noqa: E501
        :rtype: str
        """
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, instrument_type):
        """Sets the instrument_type of this FlexibleFundFields.


        :param instrument_type: The instrument_type of this FlexibleFundFields.  # noqa: E501
        :type: str
        """

        self._instrument_type = instrument_type

    @property
    def freq(self):
        """Gets the freq of this FlexibleFundFields.  # noqa: E501


        :return: The freq of this FlexibleFundFields.  # noqa: E501
        :rtype: str
        """
        return self._freq

    @freq.setter
    def freq(self, freq):
        """Sets the freq of this FlexibleFundFields.


        :param freq: The freq of this FlexibleFundFields.  # noqa: E501
        :type: str
        """

        self._freq = freq

    @property
    def position_type(self):
        """Gets the position_type of this FlexibleFundFields.  # noqa: E501


        :return: The position_type of this FlexibleFundFields.  # noqa: E501
        :rtype: str
        """
        return self._position_type

    @position_type.setter
    def position_type(self, position_type):
        """Sets the position_type of this FlexibleFundFields.


        :param position_type: The position_type of this FlexibleFundFields.  # noqa: E501
        :type: str
        """

        self._position_type = position_type

    @property
    def nickname(self):
        """Gets the nickname of this FlexibleFundFields.  # noqa: E501


        :return: The nickname of this FlexibleFundFields.  # noqa: E501
        :rtype: str
        """
        return self._nickname

    @nickname.setter
    def nickname(self, nickname):
        """Sets the nickname of this FlexibleFundFields.


        :param nickname: The nickname of this FlexibleFundFields.  # noqa: E501
        :type: str
        """
        if nickname is None:
            raise ValueError("Invalid value for `nickname`, must not be `None`")  # noqa: E501

        self._nickname = nickname

    @property
    def author(self):
        """Gets the author of this FlexibleFundFields.  # noqa: E501


        :return: The author of this FlexibleFundFields.  # noqa: E501
        :rtype: str
        """
        return self._author

    @author.setter
    def author(self, author):
        """Sets the author of this FlexibleFundFields.


        :param author: The author of this FlexibleFundFields.  # noqa: E501
        :type: str
        """
        if author is None:
            raise ValueError("Invalid value for `author`, must not be `None`")  # noqa: E501

        self._author = author

    @property
    def valid_from(self):
        """Gets the valid_from of this FlexibleFundFields.  # noqa: E501


        :return: The valid_from of this FlexibleFundFields.  # noqa: E501
        :rtype: int
        """
        return self._valid_from

    @valid_from.setter
    def valid_from(self, valid_from):
        """Sets the valid_from of this FlexibleFundFields.


        :param valid_from: The valid_from of this FlexibleFundFields.  # noqa: E501
        :type: int
        """
        if valid_from is None:
            raise ValueError("Invalid value for `valid_from`, must not be `None`")  # noqa: E501

        self._valid_from = valid_from

    @property
    def insample(self):
        """Gets the insample of this FlexibleFundFields.  # noqa: E501


        :return: The insample of this FlexibleFundFields.  # noqa: E501
        :rtype: str
        """
        return self._insample

    @insample.setter
    def insample(self, insample):
        """Sets the insample of this FlexibleFundFields.


        :param insample: The insample of this FlexibleFundFields.  # noqa: E501
        :type: str
        """

        self._insample = insample

    @property
    def updated(self):
        """Gets the updated of this FlexibleFundFields.  # noqa: E501


        :return: The updated of this FlexibleFundFields.  # noqa: E501
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this FlexibleFundFields.


        :param updated: The updated of this FlexibleFundFields.  # noqa: E501
        :type: datetime
        """

        self._updated = updated

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(FlexibleFundFields, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, FlexibleFundFields):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
