import sys

from cfx_middleware.classes.ParserResult import ParserResult
from cfx_middleware.exceptions.NotDictException import NotDictException, is_dict
from cfx_middleware.exceptions.MethodNotValid import MethodNotValid, validate_method
from cfx_middleware.helpers.utils import class_to_json, json_to_dict, all_methods
from cfx_middleware.rabbit.send_rabbit import send_message


def parser_result(parser_result_data):

    if isinstance(parser_result_data, str):
        if not parser_result_data:
            print("You provided an empty JSON, please review your code")
            sys.exit(1)

        parser_result_data = json_to_dict(parser_result_data)

    if not parser_result_data:
        print("You provided an empty dict, please review your code")
        sys.exit(1)

    data_object = validate_parser_result(parser_result_data)

    if data_object.method != "*":
        method_to_execute = globals()[data_object.method]
        return method_to_execute(data_object)
    else:
        data_object.method = all_methods()
        return send_parser(data_object)


def validate_parser_result(parser_result: dict):
    try:
        # Validate that data provided is Dict
        is_dict(parser_result)
        # Validate that method provided exists
        if parser_result["Method"] != "*":
            validate_method(parser_result["Method"])

        return ParserResult(**parser_result)
    except ValueError as ve:
        print("Value Error: " + str(ve))
        sys.exit(1)
    except TypeError as te:
        print("Type Error: " + str(te))
        sys.exit(1)
    except NotDictException as nde:
        print("Dict Error: " + str(nde))
        sys.exit(1)
    except MethodNotValid as mnv:
        print("Method Error: " + str(mnv))
        sys.exit(1)


def send_parser(parser_result: ParserResult):
    data_converted = class_to_json(parser_result)
    send_message(data_converted)
    print("Parser Result send to Queue")
    return True


def validate_units(parser_result: ParserResult):
    data_converted = class_to_json(parser_result)
    send_message(data_converted)
    print("Method to execute validate_units")
    return True


def units_inspected(parser_result: ParserResult):
    data_converted = class_to_json(parser_result)
    send_message(data_converted)
    print("Method to execute units_inspected")
    return True


def units_departed(parser_result: ParserResult):
    data_converted = class_to_json(parser_result)
    send_message(data_converted)
    print("Method to execute units_departed")
    return True


def state_change(parser_result: ParserResult):
    data_converted = class_to_json(parser_result)
    send_message(data_converted)
    print("Method to execute state_change")
    return True


if __name__ == "__main__":
    success = parser_result(
        {
            "SerialNumber": "P69660003012311280100684",
            "Sequence": "None",
            "Assembly": "6966-0003-01",
            "RouteStep": "AOI_T",
            "WorkOrder": "None",
            "Step": "2",
            "Line": "L16",
            "IsPanel": True,
            "PassFail": 1,
            "User": "SAUL RUIZ",
            "StartTime": "2023-11-29T10:24:31",
            "EndTime": "2023-11-29T10:24:46",
            "MachineId": "AOI-L16",
            "IoTId": "84968468",
            "ProgramName": "6966-0003-01_BOT",
            "LogFileName": "None",
            "Remarks": "None",
            "IsBirth": True,
            "Parameters": {"RecipeName": "6966-0003-01_BOT", "RecipeRevision": "None"},
            "TestResults": "None",
            "Method": "units_inspected",
            "ChildSerialNumbers": [
                {
                    "SerialNumber": "",
                    "Sequence": 1,
                    "TestResult": [
                        {
                            "TestName": "ST5901_Polarity3_Polarity_AI2-3D-1_AI2_3D_ConfidenceLevel",
                            "Sequence": 5,
                            "PassFail": "OK",
                            "LowLimit": "1",
                            "HighLimit": "100",
                            "Value": "82.3721508947464",
                            "IsCritical": True,
                            "Defect": "None",
                            "ErrorCode": "None",
                            "ErrorLocation": "None",
                            "ErrorMessage": "None",
                            "Parameters": "None",
                        },
                    ],
                    "PassFail": 1,
                },
            ],
        }
    )

    print(f"Success {success}")
