def validateReg(username,email):
	import re
	regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
	if len(username)<8:
		return "Enter correct Username more than 8 Characters"
	else:
		pass
	if(re.search(regex,email)):
		pass
	else:
		return "Enter Correct mail id "


