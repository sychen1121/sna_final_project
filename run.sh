program=src/main.py
input_path=input/Gowalla_new/POI/
output_path=output/poi_recommendation/
nproc=8
func=$1

python3 $program $input_path $output_path $nproc $func &

