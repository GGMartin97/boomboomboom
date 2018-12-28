import time
import smbus


#MAX30102 address
MAX30102_I2CADDR = 0X57

#MAX30102 Registers
REG_INTR_STATUS_1   = 0X00
REG_INTR_STATUS_2   = 0X01
REG_INTR_ENABLE_1   = 0X02
REG_INTR_ENABLE_2   = 0X03
REG_FIFO_WR_PTR     = 0X04
REG_OVF_COUNTER     = 0X05
REG_FIFO_RD_PTR     = 0X06
REG_FIFO_DATA       = 0X07
REG_FIFO_CONFIG     = 0X08
REG_MODE_CONFIG     = 0X09
REG_SPO2_CONFIG     = 0X0A
REG_LED1_PA         = 0X0C
REG_LED2_PA         = 0X0D
REG_PILOT_PA        = 0X10
REG_MULTI_LED_CTRL1 = 0X11
REG_MULTI_LED_CTRL2 = 0X12
REG_TEMP_INTR       = 0X1F
REG_PROX_INT_THRESH = 0X30
REG_REV_ID          = 0XFE
REG_PART_ID         = 0XFF



def maxim_max30102_reset():   
	bus.write_byte_data(MAX30102_I2CADDR,REG_MODE_CONFIG,0X40)

def maxim_max30102_init():    
	bus.write_byte_data(MAX30102_I2CADDR,REG_INTR_ENABLE_1,0xc0)
	bus.write_byte_data(MAX30102_I2CADDR,REG_INTR_ENABLE_2,0x00)
	bus.write_byte_data(MAX30102_I2CADDR,REG_FIFO_WR_PTR,0x00)
	bus.write_byte_data(MAX30102_I2CADDR,REG_OVF_COUNTER,0x00)
	bus.write_byte_data(MAX30102_I2CADDR,REG_FIFO_RD_PTR,0x00)
	bus.write_byte_data(MAX30102_I2CADDR,REG_FIFO_CONFIG,0x0f)
	bus.write_byte_data(MAX30102_I2CADDR,REG_MODE_CONFIG,0x03)
	bus.write_byte_data(MAX30102_I2CADDR,REG_SPO2_CONFIG,0x27)
	bus.write_byte_data(MAX30102_I2CADDR,REG_LED1_PA,0x24)
	bus.write_byte_data(MAX30102_I2CADDR,REG_LED2_PA,0x24)
	bus.write_byte_data(MAX30102_I2CADDR,REG_PILOT_PA,0x7f)

def maxim_max30102_read_fifo():
	temp_red_led = 0
	temp_ir_led  = 0
	ach_i2c_data=[]
	uch_temp=bus.read_byte_data(MAX30102_I2CADDR,REG_INTR_STATUS_1)
	uch_temp=bus.read_byte_data(MAX30102_I2CADDR,REG_INTR_STATUS_2)
	bus.write_byte(MAX30102_I2CADDR,REG_FIFO_DATA)
	time.sleep(0.001)
	print('hello')
	for i in range(0,6):
		ach_i2c_data.append(bus.read_byte_data(MAX30102_I2CADDR,REG_FIFO_DATA))
	un_temp=ach_i2c_data[0]<<16
	temp_red_led=temp_red_led+un_temp
	un_temp=ach_i2c_data[1]<<8
	temp_red_led=temp_red_led+un_temp
	un_temp=ach_i2c_data[2]
	temp_red_led=temp_red_led+un_temp

	un_temp=ach_i2c_data[3]<<16
	temp_ir_led=temp_ir_led+un_temp
	un_temp=ach_i2c_data[4]<<8
	temp_ir_led=temp_ir_led+un_temp
	un_temp=ach_i2c_data[5]
	temp_ir_led=temp_ir_led+un_temp
	return temp_red_led,temp_ir_led






if __name__=="__main__":
	address=MAX30102_I2CADDR
	bus=smbus.SMBus(1)
	maxim_max30102_reset()
	time.sleep(0.5)
	maxim_max30102_init()
	time.sleep(0.5)
	martin1=[]
	martin2=[]
	for h in range(0,500):
		h1,h2=maxim_max30102_read_fifo()
		martin1.append(h1)
		martin2.append(h2)
	print(martin1)
