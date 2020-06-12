import os
import random
import string
import json
from optparse import OptionParser

iothub_name = "kumbaya-hub"

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def create_device():
    device_id = randomString(10)
    print('create device ' +  device_id)
    create_device_stream = os.popen('az iot hub device-identity create -n ' + iothub_name + ' -d ' + device_id + ' --ee')
    print(create_device_stream.read())
    return device_id

def save_information_in_sketch(device_id):
    get_sas_token_stream = os.popen('az iot hub generate-sas-token -d ' + device_id + ' -n ' + iothub_name + ' --du 31556952')
    response = json.loads(get_sas_token_stream.read())

    f = open("./prototype-software/src/secrets.h", "w")
    f.write("#define WIFI_NAME \"Bbox-9D9A7C8C\"\n#define WIFI_PASSWORD \"947D524F7612A393519AEC5476C6E7\"\n#define DEVICE_ID \"" + device_id + "\"\n#define AZURE_HOSTNAME \"" + iothub_name + ".azure-devices.net\"\n")
    f.write("#define AZURE_USERNAME \"" + iothub_name +  ".azure-devices.net/" + device_id + "/?api-version=2018-06-30\"\n#define AZURE_PASSWORD \"" + response["sas"] + "\"\n#define AZURE_FEEDBACK_TOPIC \"devices/" + device_id + "/messages/events/\"\n")
    f.write("#define AZURE_LED_TOPIC \"devices/" + device_id + "/messages/devicebound/#\"\n#define USER_ID \"" + options.user_id + "\"\n#define DEVEL\n")
    f.close()


def upload_sketch(board_name, bus_name):
    stream_create = os.popen('cd prototype-software && git pull origin master')
    stream_create.read()

    last_tag_stream = os.popen('cd prototype-software && git describe --tags --abbrev=0')
    last_tag = last_tag_stream.read()

    switch_branch = os.popen('cd prototype-software && git checkout ' + last_tag)
    switch_branch.read()

    libraries = ['MQTT', 'WiFiNINA']

    for library in libraries:
        install_library_stream = os.popen('cd prototype-software && arduino-cli lib install ' + library)
        print('Library ' + library + ' is installed')

    device_id = create_device()

    save_information_in_sketch(device_id)

    print('Compile for ' + board_name)
    compile_sketch_stream = os.popen('cd prototype-software && arduino-cli compile --fqbn ' + board_name + ' ./src')
    print(compile_sketch_stream.read())

    print('Upload Sketch to ' + bus_name)
    upload_sketch_stream = os.popen('cd prototype-software && arduino-cli upload --fqbn ' + board_name + ' ./src --port ' + bus_name)
    upload_sketch_stream.read()
    print('Sketch uploaded to ' + bus_name)


if __name__ == "__main__":
    device_connected = False

    parser = OptionParser()
    parser.add_option("-u", "--user_id", dest="user_id",
                      help="User id", metavar="USER_ID")

    (options, args) = parser.parse_args()

    if options.user_id == None:
        print(parser.print_help())
        exit(1)

    while True:
        stream = os.popen('arduino-cli board list')
        output = stream.read()

        output = output.split('\n')[1:]

        output = list(filter(len, output))

        output = list(filter(lambda item: item.find('Unknown') == -1, output))

        if len(output) > 0 and device_connected == False:
            device_connected = True
            for item in output:
                tmp = item.split(' ')
                bus_name = tmp[0]
                board_name = tmp[-2]
                board_type = tmp[-1]
                print(bus_name, board_name, board_type)

                if os.path.isdir('./prototype-software'):
                    print('software')
                    upload_sketch(board_name, bus_name)
                else:
                    print('no software')
                    stream_create = os.popen('git clone git@github.com:KumbayaHHS/prototype-software.git')
                    upload_sketch(board_name, bus_name)

        elif len(output) == 0 :
            device_connected = False
