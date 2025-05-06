import heapq
from collections import defaultdict
import os

class Huffman:
    """
    A class to perform Huffman coding compression and decompression.
    """
    def __init__(self):
        self.original_size = 0
        self.compressed_size = 0
        self.huffman_codes = {}
        self.reverse_codes = {}
    
    def compress_text(self, text):
        """
        Compress the given text using Huffman coding.
        
        Args:
            text (str): The text to compress
            
        Returns:
            bytes: The compressed data as bytes
        """
        # Reset counters
        self.original_size = len(text.encode('utf-8'))
        self.compressed_size = 0
        
        # Build frequency table
        frequency = defaultdict(int)
        for char in text:
            frequency[char] += 1
        
        # Create Huffman codes
        self.huffman_codes = self._build_huffman_tree(frequency)
        self.reverse_codes = {v: k for k, v in self.huffman_codes.items()}
        
        # Encode the text
        encoded_text = ''.join(self.huffman_codes[char] for char in text)
        
        # Add header with code length
        header = len(self.huffman_codes).to_bytes(2, byteorder='big')
        
        # Add code table
        code_table = bytearray()
        for char, code in self.huffman_codes.items():
            # Store character, code length, and code
            char_bytes = char.encode('utf-8')
            code_table.extend(len(char_bytes).to_bytes(1, byteorder='big'))
            code_table.extend(char_bytes)
            code_table.extend(len(code).to_bytes(1, byteorder='big'))
            code_table.extend(int(code, 2).to_bytes((len(code) + 7) // 8, byteorder='big'))
        
        # Convert bit string to bytes
        # Calculate padding needed
        padding = 8 - (len(encoded_text) % 8) if len(encoded_text) % 8 != 0 else 0
        padded_encoded_text = encoded_text + '0' * padding
        
        # Store padding amount in first byte
        padding_info = padding.to_bytes(1, byteorder='big')
        
        # Convert to bytes
        encoded_bytes = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            encoded_bytes.append(int(byte, 2))
        
        # Combine all parts
        compressed_data = bytearray(header)
        compressed_data.extend(code_table)
        compressed_data.extend(padding_info)
        compressed_data.extend(encoded_bytes)
        
        self.compressed_size = len(compressed_data)
        
        return bytes(compressed_data)
    
    def decompress_data(self, compressed_data):
        """
        Decompress the given data using Huffman coding.
        
        Args:
            compressed_data (bytes): The compressed data
            
        Returns:
            str: The decompressed text
        """
        # Read header to get code table size
        code_table_size = int.from_bytes(compressed_data[0:2], byteorder='big')
        
        # Recreate code table
        self.reverse_codes = {}
        pos = 2
        for _ in range(code_table_size):
            char_len = compressed_data[pos]
            pos += 1
            char = compressed_data[pos:pos+char_len].decode('utf-8')
            pos += char_len
            code_len = compressed_data[pos]
            pos += 1
            code_bytes = compressed_data[pos:pos+((code_len+7)//8)]
            pos += (code_len+7)//8
            
            # Convert bytes to bit string
            code = bin(int.from_bytes(code_bytes, byteorder='big'))[2:].zfill(code_len)
            self.reverse_codes[code] = char
        
        # Get padding information
        padding = compressed_data[pos]
        pos += 1
        
        # Get encoded data
        encoded_bytes = compressed_data[pos:]
        
        # Convert bytes to bit string
        encoded_text = ''.join(bin(byte)[2:].zfill(8) for byte in encoded_bytes)
        
        # Remove padding
        encoded_text = encoded_text[:-padding] if padding > 0 else encoded_text
        
        # Decode the text
        decoded_text = ""
        current_code = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded_text += self.reverse_codes[current_code]
                current_code = ""
        
        return decoded_text
    
    def get_compression_stats(self):
        """
        Get statistics about the compression.
        
        Returns:
            dict: Dictionary containing compression statistics
        """
        if self.original_size == 0:
            return {
                "original_size": 0,
                "compressed_size": 0,
                "compression_ratio": 1.0,
                "space_saving": 0.0
            }
        
        compression_ratio = self.original_size / self.compressed_size
        space_saving = (1 - (self.compressed_size / self.original_size)) * 100
        
        return {
            "original_size": self.original_size,
            "compressed_size": self.compressed_size,
            "compression_ratio": compression_ratio,
            "space_saving": space_saving
        }
    
    def _build_huffman_tree(self, frequency):
        """
        Build the Huffman tree and return the codes.
        
        Args:
            frequency (dict): Frequency of each character
            
        Returns:
            dict: Dictionary of Huffman codes for each character
        """
        heap = [[freq, [char, ""]] for char, freq in frequency.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        
        huffman_codes = {char: code for char, code in sorted(heapq.heappop(heap)[1:], key=lambda x: len(x[1]))}
        return huffman_codes