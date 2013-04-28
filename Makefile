CC = gcc
CFLAGS =  -std=c99 -I. -lbcm2835
DEPS = 
OBJ = Adafruit_DHT.c

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

Adafruit_DHT: $(OBJ)
	gcc -o $@ $^ $(CFLAGS)
