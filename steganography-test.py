from steganography.steganography import Steganography

input_file = "location of the input file"
output_file = "location of the output file"
hidden_material = "location of what you are trying to hide"

Steganography.encode(input_file,output_file,hidden_material)

Steganography.decode(output_file)