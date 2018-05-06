import numpy
import sys
import serial
import time



SET_REF = 0x01
REQ_POS = 0x02
SEND_POS = 0x03

ERR_ID = 10
ERR_HEAD = 11
ERR_CH = 12

ID = 0x17 # unque per motor controller

def makeHead(id):
	buffr = ""
	buffr = buffr + chr(0xFF) + chr(0xFF) + chr(id)
	return buffr

def makeCheckSum(Buffr):
	d = 0
	for i in range (2,len(Buffr)):
		d = d + ord(Buffr[i])
	d = d & 0xFF
	return chr(d)

def makeReqPos(buffr):
	buffr = buffr + chr(0x02) + chr(0x02);
	Ch = makeCheckSum(buffr)
	buffr = buffr + (Ch)
	return buffr

def makeRef(ID,theta):
	buff = makeHead(ID)
	buff = buff + chr(0x04) # 4 more to read
	buff = buff + chr(0x01) # set ref
	thetaInt = int(numpy.floor(theta/0.005))# needs to be 16 bits
	print(thetaInt)
	thetaLSB = chr(thetaInt & 0xFF)
	thetaMSB = chr((thetaInt>>8) & 0xFF)
	buff = buff + thetaMSB + thetaLSB
	buff = buff + makeCheckSum(buff)
	return buff

def getMSG():
	readBuff = serial.read()
	if(readBuff[0] != readBuff[1] != 0xFF):
		return (1,ERR_HEAD)
	tempBuff = readBuff[0:len(readBuff)-1]
	ck = makeCheckSum(tempBuff)
	if(ck != readBuff[len(readBuff) -1]):#checkSum
		return (1,ERR_CK)
	# all checks complete
	if(buff[2] != ID):
		return (1,ERR_ID) # proper messege but not to us
	
	if(buff[3] == SET_REF):
		thetaiMSB = buff[5]
		thetaiLSB = buff[6]
		thetai = int((thetaiMSB << 8) | thetaiLSB) # 16 bit
		theta = float(thetai * 1.0) * 0.005
		return (0,theta)

def sendMSG(buff):
	ser.write(buff)


ser = serial.Serial(
    port='/dev/ttyS0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=1)


ser.flush()
print("connected to: " + ser.portstr)

curBuff = makeHead(ID)
curBuff = makeReqPos(curBuff) #makeRef(ID, 60)#makeReqPos(curBuff)
sendMSG(curBuff)
while 1:
	toRead = ser.inWaiting()
	if(toRead):
		tdata = ser.read(toRead)
		print(tdata)
		print(toRead)
	time.sleep(.1)              # Sleep (or inWaiting() doesn't give the correct value)
	#data_left = ser.inWaiting()  # Get the number of characters ready to be read
	#tdata += ser.read(data_left) # Do the read and combine it with the first character
	#if(tdata):
	#yt	print(tdata)



