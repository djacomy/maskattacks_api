

PARAM_REQUIRED = "PARAM_REQUIRED"
FIELD_REQUIRED = "FIELD_REQUIRED"
UNKNOWN_VALUE = "UNKNOWN_VALUE"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
BAD_MATERIAL_PRODUCT = "BAD_MATERIAL_PRODUCT"
BAD_FINAL_PRODUCT = "BAD_FINAL_PRODUCT"
BAD_EQUIVALENCE_PARAM = "BAD_EQUIVALENCE_PARAM"
NO_STOCK = "NO_STOCK"
NOT_ENOUGH_STOCK = "NOT_ENOUGH_STOCK"

ERROR_MESSAGES = {
    PARAM_REQUIRED: "{} is required",
    FIELD_REQUIRED: "{} of {} is required",
    UNKNOWN_VALUE: "Value {} is unknown for the field {}",
    UNKNOWN_RESOURCE: "Unknown ressource",
    BAD_MATERIAL_PRODUCT: "{} is not a material product.",
    BAD_FINAL_PRODUCT: "{} is not a final product.",
    BAD_EQUIVALENCE_PARAM: "{} argument: Missing field {}.",
    NO_STOCK: "No stock for reference {}",
    NOT_ENOUGH_STOCK: "Not enough stock for reference {}"
}


