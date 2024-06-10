import base64
import hashlib

def encode_payload(payload, salt_key, salt_index):
  """
  Encodes a payload using a salt key and salt index.

  Args:
    payload: The payload to encode (string).
    salt_key: The secret salt key to use for encoding (string).
    salt_index: An integer to add variation to the salt.

  Returns:
    The encoded payload (string).
  """
  # Combine the salt key and salt index to create a unique salt value.
  salt = salt_key + str(salt_index)

  # Hash the salt using SHA-256 to create a secure hash value.
  hashed_salt = hashlib.sha256(salt.encode()).hexdigest()

  # Combine the payload and the hashed salt to prepare for encoding.
  combined_data = payload.encode() + hashed_salt.encode()

  # Encode the combined data using base64 encoding.
  encoded_payload = base64.b64encode(combined_data).decode()

  # Return the encoded payload.
  return encoded_payload

def decode_payload(encoded_payload, salt_key, salt_index):
  """
  Decodes an encoded payload using a salt key and salt index.

  Args:
    encoded_payload: The encoded payload to decode (string).
    salt_key: The secret salt key to use for decoding (string).
    salt_index: The integer used during encoding to create the salt.

  Returns:
    The decoded payload (string), or an error message on decode failure.
  """
  try:
    # Attempt to base64 decode the encoded payload.
    decoded_data = base64.b64decode(encoded_payload.encode())
  except:
    # Return error message for base64 decode failure.
    return ("Invalid encoded payload (base64 decode failed).")

  # Recreate the salt using the provided salt key and salt index.
  salt = salt_key + str(salt_index)

  # Hash the recreated salt to compare with the hashed salt in the payload.
  expected_hashed_salt = hashlib.sha256(salt.encode()).hexdigest()

  # Extract the hashed salt from the end of the decoded data.
  actual_hashed_salt = decoded_data[-64:].decode()

  # Compare the expected hashed salt with the one extracted from the payload.
  if expected_hashed_salt != actual_hashed_salt:
    # Return error message for incorrect salt or index.
    return "Error: Incorrect salt key or salt index used for decoding."

  # Separate the payload from the decoded data by removing the hashed salt.
  return decoded_data[:-64].decode()

if __name__ == "__main__":
    # Example usage
    payload = "This is a secret message"
    salt_key = "my_salt"
    salt_index = 123

    encoded_payload = encode_payload(payload, salt_key, salt_index)
    print(encoded_payload)

    decoded_payload = decode_payload(encoded_payload, salt_key, salt_index)
    print(decoded_payload)

    # Test with incorrect salt index
    incorrect_salt_index = 456
    incorrect_decoded_payload = decode_payload(encoded_payload, salt_key, incorrect_salt_index)
    print(incorrect_decoded_payload)

    # Test with incorrect salt key
    incorrect_salt_key = "wrong_salt"
    incorrect_decoded_payload = decode_payload(encoded_payload, incorrect_salt_key, salt_index)
    print(incorrect_decoded_payload)
