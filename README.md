# Part 2: Air Quality Monitor with Azure IoT Edge and IoT Central




## References

[Tutorial: Create and connect a client application to your Azure IoT Central application (Python)](https://docs.microsoft.com/en-us/azure/iot-central/core/tutorial-connect-device-python)




https://stackoverflow.com/questions/50337042/how-to-generate-a-proof-of-possesion-for-a-x509-certificate-using-openssl


https://github.com/Azure/azure-iot-sdk-c/blob/master/tools/CACertificates/CACertificateOverview.md

https://docs.microsoft.com/en-us/azure/iot-edge/how-to-auto-provision-x509-certs


https://docs.microsoft.com/en-us/azure/iot-edge/how-to-create-test-certificates


https://docs.microsoft.com/en-us/azure/iot-edge/how-to-auto-provision-x509-certs


I got the answer with the Azure support team.

1. Generate root key and X509 cert

    ```bash
    openssl req -x509 -newkey rsa:2048 -keyout root_private.pem -nodes -out root_cert.pem
    ```
2. Generate the verification cert...

    **Create verification key**

    ```bash
    openssl genrsa -out verification.key 2048
    ```
    **Create the verification cert**

    When creating the verification cert, I need to specify the verification code obtained (7A69A4702DA903A41C3A5BC5575A8E3F49BEC5E5BA2D4CE1) as the "Common Name" certificate field.

    ```bash
    openssl req -new -key verification.key -out verification.csr
    ```
3. Create the proof of possession certificate with the following command:

    ```bash
    openssl x509 -req -in verification.csr -CA root_cert.pem -CAkey root_private.pem -CAcreateserial -out verificationCert.pem -days 1024 -sha256
    ```