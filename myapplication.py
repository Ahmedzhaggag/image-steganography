def to_binary(data):
    """
    Converts a string or text to binary representation.
    :param data: The string to convert to binary.
    :return: The binary representation of the string.
    """
    return ''.join(format(ord(char), '08b') for char in data)


def hide_message_in_image(image_path, message, output_path):
    """
    Hides the secret message in the image using the least significant bit method.
    
    :param image_path: Path to the image file (BMP or other simple format).
    :param message: The secret message to hide in the image.
    :param output_path: Path to save the modified image with hidden message.
    """
    # Convert message to binary
    binary_message = to_binary(message) + '1111111111111110'  # End of message marker
    
    with open(image_path, 'rb') as image_file:
        # Read the image data as bytes
        image_data = bytearray(image_file.read())
        
        message_index = 0
        
        # The first part of the image data will be the header, which we should not modify
        # We're going to assume the image has a 54-byte header (common for BMP)
        header_size = 54
        pixel_data = image_data[header_size:]  # Skip header, manipulate pixel data
        
        # Iterate over pixel data and hide the message in the least significant bit
        for i in range(len(pixel_data)):
            if message_index < len(binary_message):
                # Set the least significant bit of the byte
                pixel_data[i] = (pixel_data[i] & 0xFE) | int(binary_message[message_index])
                message_index += 1
            else:
                break
        
        # Write back the image with the hidden message (including header)
        with open(output_path, 'wb') as output_image:
            output_image.write(image_data[:header_size])  # Write header unchanged
            output_image.write(pixel_data)  # Write modified pixel data

    print(f"Message hidden successfully in {output_path}")


def extract_message_from_image(image_path):
    """
    Extracts the hidden message from an image by reading the least significant bits.
    
    :param image_path: Path to the image file with a hidden message.
    :return: The extracted secret message.
    """
    with open(image_path, 'rb') as image_file:
        # Read the image data as bytes
        image_data = bytearray(image_file.read())
        
        # The first part of the image data will be the header
        header_size = 54
        pixel_data = image_data[header_size:]  # Skip header, only look at pixel data
        
        binary_message = ''
        
        # Iterate through each byte in the pixel data and extract the least significant bit
        for byte in pixel_data:
            binary_message += str(byte & 1)  # Extract LSB
        
        # The message ends with the marker '1111111111111110'
        end_marker = '1111111111111110'
        message_end_index = binary_message.find(end_marker)
        
        if message_end_index != -1:
            binary_message = binary_message[:message_end_index]
            # Convert the binary message back to text
            message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
            return message
        else:
            print("No hidden message found.")
            return None


# Example usage with user input:
image_path = 'input_image.bmp'  # Your original image file
output_path = 'output_image.bmp'  # Output image with hidden message

# Prompt the user to enter the secret message
user_message = input("Enter the message you want to hide in the image: ")

# Hide the message in the image
hide_message_in_image(image_path, user_message, output_path)

# Extract the hidden message from the modified image
extracted_message = extract_message_from_image(output_path)
if extracted_message:
    print(f"Extracted Message: {extracted_message}")



