def byte_stuffing(data, flag_byte='F', escape_byte='E'):
    stuffed_data = [flag_byte]

    for byte in data:
        if byte == flag_byte or byte == escape_byte:
            stuffed_data.append("|"+escape_byte+"|")
        stuffed_data.append(byte)

    stuffed_data.append("|"+flag_byte+"|")

    return stuffed_data


def main():
    frame_data = list(input("Enter the characters in the frame: "))

    stuffed_frame = byte_stuffing(frame_data)

    print("\nStuffed Frame: ", ''.join(stuffed_frame))


if __name__ == "__main__":
    main()
