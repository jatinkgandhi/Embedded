Project IDEA:
Fingerprint based multi locker.

|==========|==========|==========|==========|==========|==========|                               _____________
|    1     |    2     |    3     |   4      |    5     |    6     |     ____                     /  FP Sensor /
|          |          |          |          |          |          |    |    |                   /____________/
|==========|==========|==========|==========|==========|==========| ~~~|    |                         | UART/Any bus
|   7      |    8     |    9     |    10    |    11    |    12    | ~~~|  I |                _________|_____
|          |          |          |          |          |          |    |  2 | ==============| Arduino Board | 
|==========|==========|==========|==========|==========|==========|    |  C |               |_______________|
|   13     |   14     |    15    |    16    |    17    |   18     |    |    |  
|          |          |          |          |          |          |    |  E |  
|==========|==========|==========|==========|==========|==========|    |____|  
|    19    |   20     |   21     |    22    |    23    |    24    |       I2C port expander    
|          |          |          |          |          |          |           
|==========|==========|==========|==========|==========|==========|           
......

Use case:
Each user is mapped to specific locker.
Once his fingerprint is found, it opens the locker until he closes or
timeout occurs.

//// Rough pseudo code.., 
fingerprint = getFingerPrint();
locationInDatabase = 0xBAD1D;
if(found == locateFingerprint(fingerprint, &locationInDatabase))
{
	SolenoidGPIO_ID = DatabaseLookup(locationInDatabase);
	I2CPortExpander.setPort(SolenoidGPIO_ID);
	start timer (Lockers[locationInDatabase].timer);
	if(Lockers[locationInDatabase].timedout befoer locker closed)
	{
		RaiseAlarm(LockerID);
	}
	if(Locker[locationInDatabase].isClosed && ! (Locker[locationInDatabase].timedout)
	{
		DisbaleTimer(Locker[locationInDatabase]);
	}
}

