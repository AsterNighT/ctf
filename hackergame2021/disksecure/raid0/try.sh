sudo mdadm --create -c 128 -l 0 -n 8 /dev/md1 /dev/loop10 /dev/loop11 /dev/loop12 /dev/loop13 /dev/loop14 /dev/loop15 /dev/loop16 /dev/loop17 
sudo mount /dev/md1 /mnt/raid0
sudo mdadm --stop /dev/md1