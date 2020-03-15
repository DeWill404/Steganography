from PIL import Image
import binascii as t
from stegano import exifHeader as con

class Steg:
  def __init__(self):
    fileName = ""
    message = ""
  
  # Conversion functions
  def rgb2hex (self, r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

  def hex2rgb (self, hexcode):
    temp = []
    temp.append(int(hexcode[1:3], 16))
    temp.append(int(hexcode[3:5], 16))
    temp.append(int(hexcode[5:7], 16))
    return tuple(temp)

  def str2bin (self, message):
    message = message.encode()
    binary = bin(int(t.hexlify(message), 16))
    return binary[2:]

  def bin2str (self, binary):
    message = t.unhexlify('%x' % (int(binary, 2)))
    return message


  # Encoding Message into image hexadecimal
  def encode(self, hexcode, digit):
    if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):
      hexcode = hexcode[:-1] + digit
      return hexcode
    else:
      return None


  # Decodiing Message from image hexadecimal
  def decode(self, hexcode):
    if hexcode[-1] in ('0', '1'):
      return hexcode[-1]
    else:
      return None

  # Getting file extension and base path
  def fileExtractor(self, filename, c):
    if c in filename:
      i = filename.rfind(c)
    return filename[i+1:]


  # Hiding text in image
  def hide(self, filename, folderOut, message):
    self.filename = filename
    self.message = message
    img = Image.open(filename)
    binary = self.str2bin(message) + "1111111111111110"
    # Getting file extension
    temp = "." + self.fileExtractor(filename, '.').lower()
    folderOut = folderOut + "/" + self.fileExtractor(filename, '/')
    # For png & ico images
    if(temp == '.png' or temp == '.ico'):
      if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()
        newData = []
        digit = 0
        temp = ''
        for item in datas:
          if (digit < len(binary)):
            newpix = self.encode(self.rgb2hex(item[0], item[1], item[2]), binary[digit])
            if newpix == None:
              newData.append(item)
            else:
              r, g, b = self.hex2rgb(newpix)
              newData.append((r, g, b, 255))
              digit += 1
          else:
            newData.append(item)
        img.putdata(newData)
        img.save(folderOut)
    # For jpeg & jpg images
    else:
      con.hide(filename, folderOut, message)


  # Retrieving text from images
  def retr(self, filename):
    self.filename = filename
    img = Image.open(filename)
    binary = ''
    # Getting file extension
    temp = "." + self.fileExtractor(filename, '.').lower()
    # For png & ico images
    if(temp == '.png' or temp == '.ico'):
      if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()
        for item in datas:
          digit = self.decode(self.rgb2hex(item[0], item[1], item[2]))
          if digit == None:
            pass
          else:
            binary = binary + digit
            if (binary[-16:] == "1111111111111110"):
              return str(self.bin2str(binary[:-16]))[2:-1]
        return str(self.bin2str(binary))
    # For jpeg & jpg images
    else:
      message = con.reveal(filename)
      message = str(message)[2:-1]
    return message