import heapq
from collections import defaultdict
import os
# Function to perform Huffman Coding
class Huffman:
    def __init__(self):
        self.original = 0
        self.compressed_byte = 0
        self.reverse_huff_codes = ""
        self.decoded_text = ""
        self.file_path = ""
        self.text_area = ""
    def huffman_coding(self, text):
        # Calculate frequency of each character
        self.original = len(text.encode('utf-8'))
        self.compressed_byte = 0
        frequency = defaultdict(int)
        for char in text:
            frequency[char] += 1
        # Create a priority queue (min-heap) based on character frequencies
        heap = [[weight, [char, ""]] for char, weight in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            # Pop two nodes with lowest frequencies
            low1 = heapq.heappop(heap)
            low2 = heapq.heappop(heap)

            # Merge them and update their codes
            for pair in low1[1:]:
                pair[1] = '0' + pair[1]
            for pair in low2[1:]:
                pair[1] = '1' + pair[1]

            # Add the merged node back to the heap
            heapq.heappush(heap, [low1[0] + low2[0]] + low1[1:] + low2[1:])

        # Get the Huffman codes
        huff_codes = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
        huffman_dict = {char: code for char, code in huff_codes}

        encoded_str = ''.join(huffman_dict[char] for char in text)
        # Reverse the Huffman codes for decoding
        reverse_huff_codes = {v: k for k, v in huffman_dict.items()}
        #Decoding the Huffman Coded Generated
        self.decoded_text = ""
        self.current_bits = ""
        reverse_codes = {v: k for k, v in huffman_dict.items()}

        #Travese through each bit
        for bit in encoded_str:
            self.current_bits += bit
            if self.current_bits in reverse_codes:
                self.decoded_text += reverse_codes[self.current_bits]
                self.current_bits = ""

        # Return the Huffman codes and reverse codes
        return huffman_dict, self.reverse_huff_codes


    # Function to encode text using Huffman codes
    def encode_text(self, text, huff_codes):
        encoded_text = ''.join(huff_codes[char] for char in text)
        return encoded_text

    # Function to convert the encoded text (binary string) to bytes
    def binary_string_to_bytes(self, binary_string):
        # Ensure the binary string length is a multiple of 8 by padding if necessary
        padding = 8 - len(binary_string) % 8
        binary_string = '0' * padding + binary_string

        # Convert the binary string into bytes
        byte_array = bytearray()
        for i in range(0, len(binary_string), 8):
            byte_array.append(int(binary_string[i:i+8], 2))
            self.compressed_byte+=1
        return byte_array

    # Function to convert bytes back to a binary string
    def bytes_to_binary_string(self, byte_array):
        binary_string = ''.join(f'{byte:08b}' for byte in byte_array)
        return binary_string
    # Function to decode the binary string back to text using reverse Huffman codes
    def decode_text(self, binary_string):
        self.decoded_text = []
        current_code = ""
        
        # Read each bit from the binary string and try to match it with Huffman codes
        for bit in binary_string:
            current_code += bit
            if current_code in self.reverse_huff_codes:
                self.decoded_text.append(self.reverse_huff_codes[current_code])
                current_code = ""
        
        return ''.join(self.decoded_text)

    # Function to open file and return content as a string
    def open_file(self, file_path):
        self.file_path = file_path
        if self.file_path:  # Check if a file was selected
            with open(self.file_path, "r") as file:
                content = file.read()
                # Now process the content for Huffman Coding
                self.process_text(content)

    # Function to process text with Huffman coding and display the result
    def process_text(self, content):
        huff_codes, self.reverse_huff_codes = self.huffman_coding(content)
        
        # Convert the Huffman codes to a string for display
        huff_code_str = "\n".join([f"{char}: {code}" for char, code in huff_codes.items()])
        
        # Encode the text using the Huffman codes
        encoded_text = self.encode_text(content, huff_codes)
        
        # Convert the encoded text (binary string) to bytes
        encoded_bytes = self.binary_string_to_bytes(encoded_text)
        
        # Clear the text widget and insert the Huffman codes
        text_area = f"Huffman Codes:\n\n{huff_code_str}\n"
        
        # compression_detail.config(text=f"self.original {self.original} bytes | Compressed: {self.compressed_byte} bytes | Ratio: {(self.compressed_byte/self.original)*100}")

    # Function to save the compressed data to a binary file with a fixed name ('compressed.bin')
    def save_compressed_data(self, encoded_bytes):
        # Get the current working directory
        current_directory = os.getcwd()

        # Define the file path for saving the compressed data as 'compressed.bin'
        save_path = os.path.join(current_directory, "compressed.bin")
        
        # Save the binary file
        with open(save_path, "wb") as file:
            file.write(encoded_bytes)

        print(f"Compressed data saved to: {save_path}")

    # Function to open and decode the binary file
    def decode_bin_file(self):
        # Ask the user for a binary file to decode
        if self.file_path:
            with open(self.file_path, "rb") as file:
                binary_data = file.read()

                # Convert bytes back to a binary string
                binary_string = self.bytes_to_binary_string(binary_data)
                return binary_string
    def get_compression_stats(self):
        """
        Get statistics about the compression.
        
        Return:
            dict: Dictionary containing compression statistics    
        """
        if self.original== 0:
            return{
                "original_size":0,
                "compressed_size": 0,
                "compression_ratio": 100.0
            }
        # Calculate compression ratio as compressed_size/original_size as a percentage
        compression_ratio = (self.compressed_byte / self.original) * 100

        return {
            "original_size": self.original,
            "compressed_size":self.compressed_byte,
            "compression_ratio": compression_ratio
        }
if __name__ == "__main__":
    huff = Huffman()
    huff.open_file("newtext1.txt")
    print(huff.get_compression_stats())
    