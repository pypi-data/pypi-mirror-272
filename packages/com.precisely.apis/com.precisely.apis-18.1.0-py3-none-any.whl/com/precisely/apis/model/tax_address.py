"""
    Precisely APIs

    Enhance & enrich your data, applications, business processes, and workflows with rich location, information, and identify APIs.  # noqa: E501

    The version of the OpenAPI document: 18.1.0
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from com.precisely.apis.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
    OpenApiModel
)
from com.precisely.apis.exceptions import ApiAttributeError



class TaxAddress(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
    }

    validations = {
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        return {
            'object_id': (str,),  # noqa: E501
            'display_name': (str,),  # noqa: E501
            'street_side': (str,),  # noqa: E501
            'business_name': (str,),  # noqa: E501
            'address_line1': (str,),  # noqa: E501
            'address_line2': (str,),  # noqa: E501
            'address_line3': (str,),  # noqa: E501
            'city': (str,),  # noqa: E501
            'state_province': (str,),  # noqa: E501
            'county': (str,),  # noqa: E501
            'postal_code': (str,),  # noqa: E501
            'latitude': (str,),  # noqa: E501
            'longitude': (str,),  # noqa: E501
            'status': (str,),  # noqa: E501
            'urbanization_name': (str,),  # noqa: E501
            'formatted_address': (str,),  # noqa: E501
            'main_address_line': (str,),  # noqa: E501
            'address_last_line': (str,),  # noqa: E501
            'place_name': (str,),  # noqa: E501
            'area_name1': (str,),  # noqa: E501
            'area_name2': (str,),  # noqa: E501
            'area_name3': (str,),  # noqa: E501
            'area_name4': (str,),  # noqa: E501
            'post_code': (str,),  # noqa: E501
            'post_code1': (str,),  # noqa: E501
            'post_code_ext': (str,),  # noqa: E501
            'country': (str,),  # noqa: E501
            'address_number': (str,),  # noqa: E501
            'street_name': (str,),  # noqa: E501
            'unit_type': (str,),  # noqa: E501
            'unit_value': (str,),  # noqa: E501
            'distance_units': (str,),  # noqa: E501
            'buffer_width': (str,),  # noqa: E501
            'user_buffer_width': (str,),  # noqa: E501
            'purchase_amount': (str,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'object_id': 'objectId',  # noqa: E501
        'display_name': 'displayName',  # noqa: E501
        'street_side': 'streetSide',  # noqa: E501
        'business_name': 'businessName',  # noqa: E501
        'address_line1': 'addressLine1',  # noqa: E501
        'address_line2': 'addressLine2',  # noqa: E501
        'address_line3': 'addressLine3',  # noqa: E501
        'city': 'city',  # noqa: E501
        'state_province': 'stateProvince',  # noqa: E501
        'county': 'county',  # noqa: E501
        'postal_code': 'postalCode',  # noqa: E501
        'latitude': 'latitude',  # noqa: E501
        'longitude': 'longitude',  # noqa: E501
        'status': 'status',  # noqa: E501
        'urbanization_name': 'urbanizationName',  # noqa: E501
        'formatted_address': 'formattedAddress',  # noqa: E501
        'main_address_line': 'mainAddressLine',  # noqa: E501
        'address_last_line': 'addressLastLine',  # noqa: E501
        'place_name': 'placeName',  # noqa: E501
        'area_name1': 'areaName1',  # noqa: E501
        'area_name2': 'areaName2',  # noqa: E501
        'area_name3': 'areaName3',  # noqa: E501
        'area_name4': 'areaName4',  # noqa: E501
        'post_code': 'postCode',  # noqa: E501
        'post_code1': 'postCode1',  # noqa: E501
        'post_code_ext': 'postCodeExt',  # noqa: E501
        'country': 'country',  # noqa: E501
        'address_number': 'addressNumber',  # noqa: E501
        'street_name': 'streetName',  # noqa: E501
        'unit_type': 'unitType',  # noqa: E501
        'unit_value': 'unitValue',  # noqa: E501
        'distance_units': 'distanceUnits',  # noqa: E501
        'buffer_width': 'bufferWidth',  # noqa: E501
        'user_buffer_width': 'userBufferWidth',  # noqa: E501
        'purchase_amount': 'purchaseAmount',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """TaxAddress - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            object_id (str): [optional]  # noqa: E501
            display_name (str): [optional]  # noqa: E501
            street_side (str): [optional]  # noqa: E501
            business_name (str): [optional]  # noqa: E501
            address_line1 (str): [optional]  # noqa: E501
            address_line2 (str): [optional]  # noqa: E501
            address_line3 (str): [optional]  # noqa: E501
            city (str): [optional]  # noqa: E501
            state_province (str): [optional]  # noqa: E501
            county (str): [optional]  # noqa: E501
            postal_code (str): [optional]  # noqa: E501
            latitude (str): [optional]  # noqa: E501
            longitude (str): [optional]  # noqa: E501
            status (str): [optional]  # noqa: E501
            urbanization_name (str): [optional]  # noqa: E501
            formatted_address (str): [optional]  # noqa: E501
            main_address_line (str): [optional]  # noqa: E501
            address_last_line (str): [optional]  # noqa: E501
            place_name (str): [optional]  # noqa: E501
            area_name1 (str): [optional]  # noqa: E501
            area_name2 (str): [optional]  # noqa: E501
            area_name3 (str): [optional]  # noqa: E501
            area_name4 (str): [optional]  # noqa: E501
            post_code (str): [optional]  # noqa: E501
            post_code1 (str): [optional]  # noqa: E501
            post_code_ext (str): [optional]  # noqa: E501
            country (str): [optional]  # noqa: E501
            address_number (str): [optional]  # noqa: E501
            street_name (str): [optional]  # noqa: E501
            unit_type (str): [optional]  # noqa: E501
            unit_value (str): [optional]  # noqa: E501
            distance_units (str): [optional]  # noqa: E501
            buffer_width (str): [optional]  # noqa: E501
            user_buffer_width (str): [optional]  # noqa: E501
            purchase_amount (str): [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, *args, **kwargs):  # noqa: E501
        """TaxAddress - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            object_id (str): [optional]  # noqa: E501
            display_name (str): [optional]  # noqa: E501
            street_side (str): [optional]  # noqa: E501
            business_name (str): [optional]  # noqa: E501
            address_line1 (str): [optional]  # noqa: E501
            address_line2 (str): [optional]  # noqa: E501
            address_line3 (str): [optional]  # noqa: E501
            city (str): [optional]  # noqa: E501
            state_province (str): [optional]  # noqa: E501
            county (str): [optional]  # noqa: E501
            postal_code (str): [optional]  # noqa: E501
            latitude (str): [optional]  # noqa: E501
            longitude (str): [optional]  # noqa: E501
            status (str): [optional]  # noqa: E501
            urbanization_name (str): [optional]  # noqa: E501
            formatted_address (str): [optional]  # noqa: E501
            main_address_line (str): [optional]  # noqa: E501
            address_last_line (str): [optional]  # noqa: E501
            place_name (str): [optional]  # noqa: E501
            area_name1 (str): [optional]  # noqa: E501
            area_name2 (str): [optional]  # noqa: E501
            area_name3 (str): [optional]  # noqa: E501
            area_name4 (str): [optional]  # noqa: E501
            post_code (str): [optional]  # noqa: E501
            post_code1 (str): [optional]  # noqa: E501
            post_code_ext (str): [optional]  # noqa: E501
            country (str): [optional]  # noqa: E501
            address_number (str): [optional]  # noqa: E501
            street_name (str): [optional]  # noqa: E501
            unit_type (str): [optional]  # noqa: E501
            unit_value (str): [optional]  # noqa: E501
            distance_units (str): [optional]  # noqa: E501
            buffer_width (str): [optional]  # noqa: E501
            user_buffer_width (str): [optional]  # noqa: E501
            purchase_amount (str): [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")
