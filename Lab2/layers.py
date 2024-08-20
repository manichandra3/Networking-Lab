def custom_encode(strs: list[str]) -> str:
    res = ""
    for s in strs:
        res += str(len(s)) + "#" + s
    return res


def custom_decode(data: str) -> list[str]:
    res = []
    i = 0
    while i < len(data):
        j = i
        while data[j] != '#':
            j += 1
        length = int(data[i:j])
        i = j + 1
        res.append(data[i:i + length])
        i += length
    return res


class OSIModel:
    def __init__(self, message, size):
        self.message = message
        self.size = size

    def application_layer(self):
        header = "AH|"
        payload = [header, self.message]
        new_message = custom_encode(payload)
        print(f"Application Layer: {new_message}")
        print(f"Decoded Message: {custom_decode(new_message)}")
        self.message = new_message
        self.presentation_layer()

    def presentation_layer(self):
        header = "PH|"
        payload = [header, self.message]
        new_message = custom_encode(payload)
        print(f"Presentation Layer: {new_message}")
        print(f"Decoded Message: {custom_decode(new_message)}")
        self.message = new_message
        self.session_layer()

    def session_layer(self):
        header = "SH|"
        payload = [header, self.message]
        new_message = custom_encode(payload)
        print(f"Session Layer: {new_message}")
        print(f"Decoded Message: {custom_decode(new_message)}")
        self.message = new_message
        self.transport_layer()

    def transport_layer(self):
        header = "TH|"
        payload = [header, self.message]
        new_message = custom_encode(payload)
        print(f"Transport Layer: {new_message}")
        print(f"Decoded Message: {custom_decode(new_message)}")
        self.message = new_message
        self.network_layer()

    def network_layer(self):
        header = "NH|"
        payload = [header, self.message]
        new_message = custom_encode(payload)
        print(f"Network Layer: {new_message}")
        print(f"Decoded Message: {custom_decode(new_message)}")
        self.message = new_message
        self.datalink_layer()

    def datalink_layer(self):
        header = "DLH|"
        payload = [header, self.message]
        new_message = custom_encode(payload)
        print(f"Data Link Layer: {new_message}")
        print(f"Decoded Message: {custom_decode(new_message)}")
        self.message = new_message
        self.physical_layer()

    def physical_layer(self):
        header = "PyH|"
        payload = [header, self.message]
        new_message = custom_encode(payload)
        print(f"Physical Layer: {new_message}")
        print(f"Decoded Message: {custom_decode(new_message)}")


# Example usage:
application_message = "MESSAGE"
model = OSIModel(application_message, len(application_message))
model.application_layer()
