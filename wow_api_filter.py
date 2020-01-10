import re
import requests

api_flags = {
        "blizzardui"  : {
                "desc"              : "This function is not a C API but a Lua function declared in Blizzard's default user interface. Its "
                                      "implementation can be viewed by extracting the addon data using the Addon Kit provided by Blizzard.",
                "authorize_in_addon": False},
        "confirmation": {
                "desc"              : "This function does not prompt the user for confirmation before its results take effect -- that behavior is "
                                      "provided by the default UI, and this function is called from the confirmation dialog",
                "authorize_in_addon": True},
        "deprecated"  : {
                "desc"              : "This function is deprecated and is no longer in use",
                "authorize_in_addon": False},
        "framexml"    : {
                "desc"              : "This function is defined by the default user interface in Lua. You can find the definition by examining the "
                                      "FrameXML code for the default UI,",
                "authorize_in_addon": False},
        "hardware"    : {
                "desc"              : "This function requires a key or mouse press in order to be used, but may not be protected.",
                "authorize_in_addon": False},
        "internal"    : {
                "desc"              : "This function does nothing in the standard game client and is used by Blizzard for internal purposes",
                "authorize_in_addon": False},
        "luaapi"      : {
                "desc"              : "This function is defined in the Lua standard libraries",
                "authorize_in_addon": True},
        "maconly"     : {
                "desc"              : "This function is designed for the Mac OS X client only",
                "authorize_in_addon": False},
        "nocombat"    : {
                "desc"              : "This function cannot be called during combat",
                "authorize_in_addon": True},
        "protected"   : {
                "desc"              : "This function is protected and can only be called by the Blizzard user interface",
                "authorize_in_addon": False},
        "review"      : {
                "desc"              : "This documentation is either in the process of being created, or needs to be reviewed for accuracy. Please "
                                      "feel free to share any findings by clicking on the 'Edit' tab at the top of the content area or by posting "
                                      "your findings on the forums.",
                "authorize_in_addon": True},  # To be confirmed
        "server"      : {
                "desc"              : "This function must query the remote server, and any results will not be immediately available to the game "
                                      "client. Please see the function's documentation for more information about how to retrieve any results.",
                "authorize_in_addon": False},
        }

file_suffix = {True: "valid", False: "invalid"}

authorized_list = list()
unauthorised_list = list()

for api_category, details in api_flags.items():
    if details["authorize_in_addon"]:
        authorized_list.append(api_category)
    else:
        unauthorised_list.append(api_category)

valid_lines = list()
invalid_lines = list()
base_regex = re.compile(r"^-- #.*") # header comment line

# TODO: make a HTTP request to http://wowprogramming.com/docs/api_categories.html and parse the HTML file
#
r = requests.get('http://wowprogramming.com/docs/api_categories.html')
print(r.status_code)
#   200
print(r.headers['content-type'])
print(r.text)

wow_api_full_description_file = "WoW_API_full.txt"
with open(wow_api_full_description_file) as f:
    lines = f.readlines()
    for line in lines:
        if base_regex.match(line):
            # header category line
            valid_lines.append(line)
            invalid_lines.append(line)
            continue
        # if invalid_lines_regex.match(line):
        for unauth in unauthorised_list:
            if unauth in line:
                # print("invalid line matched ! {}".format(line))
                invalid_lines.append(line)
                continue
        # not an invalid line
        valid_lines.append(line)
        continue

    with open("WoW_API_valid.txt", "w+") as o:
        o.writelines(valid_lines)
    with open("WoW_API_invalid.txt", "w+") as o:
        o.writelines(invalid_lines)

    # for api_category, details in api_flags.items():
        # if details["authorize_in_addon"]:
        #     file_name = "WoW_API_{}_{}.txt".format(file_suffix[details["authorize_in_addon"]], api_category)
        # else:
        #     file_name = "WoW_API_{}_{}.txt".format(file_suffix[details["authorize_in_addon"]], api_category)
        # file_name = "WoW_API_{}.txt".format(file_suffix[details["authorize_in_addon"]])



