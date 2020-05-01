# update-manager

This software will be a background task on the Kumba. It will have the following features:
- Configure the prototype for first use:
    - By creating an X.509 certificate
    - By adding the certificate to the Azure IoT Hub
- Update/Reinitialize the prototype:
    - Updating the Wi-Fi connection information.
    - Updating the user's information, in particular, the user's id.
    - Updating the internal software to the latest version.
    
Our software will use [arduino-cli](https://github.com/arduino/arduino-cli), this allows the detection of an arduino card, updating it, among other things.

The last tag of the Github [prototype-software](https://github.com/KumbayaHHS/prototype-software) repository will be considered as the last update by the software. This allows for automation in the update process.
