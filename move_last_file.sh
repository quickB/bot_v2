#!/bin/bash

last_file=$(ls image/ | grep jpeg | tail -1)
mv image/$last_file image/last/$last_file
echo $last_file
