from cryptography.fernet import Fernet as en    # Package to encrypt data
import base64       # Package to generate key from

class Encrypt:
  def __init__(self, message, password):
    self.message = message
    self.password = password


  # GETTING SECTION
  def getPassword(self):
    return self.password

  def getMessage(self):
    return self.message


  # SETTING SECTION
  def setPassword(self, password):
    self.password = password

  def setMessage(self, message):
    self.message = message


  # KEY GENERATION SECTION
  def keyGenerator (self, n):
    # First we have to convert it into str of 32 char
        # for getting key
    length = len(n)
    if (length < 32) :
      half = (32-length)//2 + 1
      temp = " "
      if(32-length > 1):
        for i in range(half):
          temp = temp + str(i%10)
        n = temp[::-1] + n + temp
      else:
        n = n + temp
    n = n[0:32]  
    n = base64.urlsafe_b64encode(n.encode())
    key = n                           # Storing key
    encryptSuit = en(key)             # Creating encrypting Suit
    return encryptSuit


  # ENRYPTION SECTION
  def encryptMessage(self):
    self.setMessage(self.getMessage().encode())                           # Encoding message to bytes
    encryptionSuit = self.keyGenerator(self.getPassword())
    encryptedText =  encryptionSuit.encrypt(self.getMessage())            # Encrypting Text
    return str(encryptedText)[2:-1]                                       # Converting to string


  # DECRYPTION SECTION
  def decryptMessage(self):
    self.setMessage(self.getMessage().encode())                           # Encoding message to bytes
    try:
      encryptionSuit = self.keyGenerator(self.getPassword())
      decryptedText = encryptionSuit.decrypt(self.getMessage())             # Decrpyting Text
      return str(decryptedText)[2:-1]                                       # Converting to string
    except:
      return "!-)=~"
