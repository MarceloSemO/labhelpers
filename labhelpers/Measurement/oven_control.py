import pyvisa

#Method to finalize a command string by adding the checksum and start-of-heading
#characters
def checksum_writer(string):
    #Start a list of ascii values with 1, the start-of-heading character, at index
    #position 0.
    ascii_array=[1]
    #Run through each character in the string
    for char in string:
    #Convert each to it’s ascii value
        ascii_array.append(ord(char))
    #Return the final command string, with the start-of-heading character, the string,
    #and the checksum, equal to the hexadecimal value of the sum of the ascii values
    #mod 256. Note that Python adds a ’ox’ prefix to hex values, hence the omission
    #of the first two characters of the checksum, and all letters must additionally by
    #capitalized because that’s how the controller likes it
    return chr(1)+string+str(hex(sum(ascii_array)%256))[2:].upper()


if __name__ == '__main__':
    inst = pyvisa.ResourceManager().open_resource('ASRL3::INSTR')
    cmd = checksum_writer('j00CB')
    print(cmd)
    inst.query(cmd)


