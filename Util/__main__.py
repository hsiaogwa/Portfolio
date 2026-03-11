sh1 = ['?', 'help', 'q', 'encode']

while True:
	sh: str = input("$ util >>> ")
	rt = sh1.index(sh.split(' ')[0]) if sh.split(' ')[0] in sh1 else -1
	if rt == 2:
		print("Exiting Util module.")
		break
	if rt >= 3:
		args = sh.split(' ')[1:]
		bash = __import__(f"Util.{sh1[rt]}", fromlist=['bash']).bash
		bash(args)
	if rt == -1:
		print("Unknown command. Type 'help' or '?' for assistance.")
