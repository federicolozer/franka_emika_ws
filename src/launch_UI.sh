data="$(python3 /home/lozer/franka_emika_ws/src/user_interface/scripts/searchData.py)"
echo "Launching user interface..."
echo "${data}"
wslview ./src/user_interface/scripts/webpage.html