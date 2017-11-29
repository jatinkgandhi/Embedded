#!/bin/bash

FACTOR=1000;

WaitUntilCPUCoolsDown()
{
        TEMP=$(cat /sys/class/thermal/thermal_zone0/temp)

        while [ "$TEMP" -gt 43000 ]
        do
                DT=$(($TEMP/$FACTOR));
                echo "CPU IS SUPER HOT....: $DT °C"
                sleep 5
                TEMP=$(cat /sys/class/thermal/thermal_zone0/temp)

        done

        #echo "CPU Cooled Down To $TEMP"
}


while true
do
        WaitUntilCPUCoolsDown;
done
