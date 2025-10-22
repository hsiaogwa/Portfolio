def getCode(string: str) -> str:
	encoded_chars = [[]]
	for index in string:
		if index % 2 == 0:
			encoded_chars[0].append(format(ord(string[index]), 'x'))
		else:
			encoded_chars[1].append(format(ord(string[index]), 'x'))
	return encoded_chars[0] + encoded_chars[1]