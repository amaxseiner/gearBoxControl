import numpy
SET_REF = 0x01
REQ_POS = 0x02
SEND_POS = 0x03

ERR_ID = 10
ERR_HEAD = 11
ERR_CH = 12

ID = 9 # unque per motor controller
def makeHead(id):
	buffr = ""
	buffr = buffr + char(0xFF) + char(0xFF) + char(id)
	return buffr

def makeCheckSum(Buffr):
	for i in range (2,size(Buffr)):
		d = d + Buffr[i]
	d = d & 0xFF
	return char(d)

def makeReqPos(buffr):
	buffr = buffr + char(0x02) + char(0x02);
	Ch = getCheckSum(buffr)
	buff = buffr + char(Ch)
	return buffr

def makeRef(ID,theta):
	buff = makeHead(ID)
	buff = buff + char(0x04) # 4 more to read
	buff = buff + char(0x01) # set ref
	thetaInt = int(floor(theta/0.005))# needs to be 16 bits
	thetaLSB = char(thetaInt & 0xFF)
	thetaMSB = char((thetaInt>>8) & 0xFF)
	buff = buff + char(thetaMSB) + char(thetaLSB)
	buff = buff + makeCheckSum(buff)
	return buff

def getMSG():
	readBuff = serial.read()
	if(readBuff[0] != readBuff[1] != 0xFF):
		return (1,ERR_HEAD)
	tempBuff = readBuff(0:size(readBuff)-1)
	ck = makeCheckSum(tempBuff)
	if( ck != readBuff[size(readBuff) -1):
		return (1,ERR_CK)
	# all checks complete
	if(buff[2] != ID):
		return (1,ERR_ID) # proper messege but not to us
	
	if(buff[3] == SET_REF):
		thetaiMSB = buff[5]
		thetaiLSB = buff[6]
		thetai = int((thetaiMSB << 8) || thetaiLSB) # 16 bit
		theta = float(thetai * 1.0) * 0.005
		return (0,theta)
	
		
