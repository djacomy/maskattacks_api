import constant

from maskattaks.serializer.orga import (AddressSerializer, UserSerializer, OrganisationSerializer,
                                         TransporterSerializer,  OtherSerializer,
                                         ManufactorSerializer, CapacitySerializer, RangeSerializer)

from maskattaks.repository import reference as ref_repository
from maskattaks.util.validator import get_error_messages

ref_fields = {"role": "orga_role", "status": "orga_status",
              "availability": "orga_availability"}


def _check_ref(input_value, field, errors):
    ref = ref_repository.get_reference_from_code_or_libelle(input_value)
    if not ref:
        error = get_error_messages(constant.UNKNOWN_VALUE, input_value, field)
        errors.append(error)
        return
    return ref.id


def _check_params(params, resource_fields, model_name, required_fields=None, ref_fields=None):
    errors = []
    obj = {}

    req_fields = required_fields or []
    for field in resource_fields:
        if params.get(field) is None and field in req_fields:
            errors.append(get_error_messages(constant.FIELD_REQUIRED, field, model_name))

        if not ref_fields or field not in ref_fields:
            # no ref variables ou field not belong to ref variables
            obj[field] = params.get(field, None)
            continue

        obj[field] = params.get(field, None)
        if params.get(field) is not None:
            value = _check_ref(params.get(field), field, errors)
            obj[field] = value

    return obj, errors


def check_organisation(params):
    ref_fields = {"role": "orga_role", "status": "orga_status",
                  "availability": "orga_availability"}

    obj, errors = _check_params(params, OrganisationSerializer.resource_fields, "organization",
                                required_fields=OrganisationSerializer.required,
                                ref_fields= ref_fields)

    roles = ref_repository.get_roles()
    check_data = {"tra": "transporter",
                  "cus": "customer",
                  "pro": "provider",
                  "man": "manufactor"}
    check_func = {"user": check_user,
                  "address": check_address,
                  "tra": check_transporter,
                  "cus": check_customer,
                  "pro": check_provider,
                  "man": check_manufactor}

    # Mandatory fields
    for field in ["user", "address"]:
        if params.get(field) is None:
            errors.append(get_error_messages(constant.FIELD_REQUIRED, field, "organisation"))
            continue

        obj_data, errors_data = check_func[field](params.get(field))
        obj[field] = obj_data
        errors.extend(errors_data)

    if obj["role"] is None:
        return obj, errors

    # conditional field
    data_code = roles[obj["role"]]
    if params.get(check_data[data_code]) is None:
        errors.append(get_error_messages(constant.FIELD_REQUIRED, check_data[data_code], "organisation"))
        return obj, errors

    obj_data, errors_data = check_func[data_code](params.get(check_data[data_code]))
    obj[check_data[data_code]] = obj_data
    errors.extend(errors_data)
    return obj, errors


def check_user(params):
    return _check_params(params, UserSerializer.resource_fields, "user",
                         required_fields=UserSerializer.required)


def check_address(params):
    return _check_params(params, AddressSerializer.resource_fields, "address",
                         required_fields=AddressSerializer.required)


def check_provider(params):
    ref_fields = {"type": "provider_type", "subtype": "provider_subtype"}
    return _check_params(params, OtherSerializer.resource_fields, "provider",
                         required_fields=OtherSerializer.required,
                         ref_fields=ref_fields)


def check_customer(params):
    ref_fields = {"type": "provider_type", "subtype": "provider_subtype"}
    return _check_params(params, OtherSerializer.resource_fields, "customer",
                         required_fields=OtherSerializer.required,
                         ref_fields=ref_fields)


def check_manufactor(params):
    ref_fields = {"type": "manufactor_type",
                  "capacity": "manufactor_capacity",
                  "skill_level": "skill_level",
                  "quality_need": "quality_need",
                  "contract_type": "contract_type"
                  }
    return _check_params(params, ManufactorSerializer.resource_fields, "manufactor",
                         required_fields=ManufactorSerializer.required,
                         ref_fields=ref_fields)


def check_transporter(params):
    """
    :param params:
    :return:
    """
    ref_fields = {
        "capacity": {"type": "capacity_type", "value": "capacity_value"},
        "range": {"type": "capacity_type", "value": "capacity_value"}
    }

    obj, errors =  _check_params(params, TransporterSerializer.resource_fields, "provider")
    obj_capacity, errors_capacity =  _check_params(params.get("range"),
                                                ["type", "value"],
                                                "transporter.range",
                                                required_fields=  CapacitySerializer.required,
                                                ref_fields=ref_fields.get("range"))
    errors +=errors_capacity
    obj.update(obj_capacity)
    obj_range, errors_range = _check_params(params.get("capacity"), ["type", "value"],
                                            "transporter.cacacity",
                                            required_fields=RangeSerializer.required,
                                            ref_fields=ref_fields.get("range"))
    errors += errors_range
    obj.update(obj_range)
    return obj, errors


