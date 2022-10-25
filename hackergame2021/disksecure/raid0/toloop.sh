for i in {0..7}
do
    sudo losetup /dev/loop1$i $i.img
done