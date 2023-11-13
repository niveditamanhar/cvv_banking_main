import hashlib
import re

#To Encrypt any string
def encrypt(rawString):
	return hashlib.md5(rawString.strip().encode()).hexdigest()


#To check the input is only number
def isNumber(inputData):
	return (bool(re.match('^[0-9]+$', str(inputData))))

#To check the input is only positive number
def isPositiveNumber(inputData):
	inputNumber = float(inputData)
	if inputNumber > 0:
		return bool(True)
	else:		
		return bool(False)

#To check the input is valid email
def isValidEmail(email):
	regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
	return (bool(re.search(regex, email)))

	

