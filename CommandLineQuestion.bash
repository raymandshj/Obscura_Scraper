echo 'How many places can be found in each country?'
echo 'We should put PlaceAddress column in a new csv file and then try to find each countriy from it'
awk -F '\t' '{print $9}' AO_Data.csv > countries.csv
echo 'Italy'
awk -F'\t' '{NumberCountry+=gsub(/Italy/,"Italy")} END {print NumberCountry}' countries.csv
echo 'France'
awk -F'\t' '{NumberCountry+=gsub(/France/,"France")} END {print NumberCountry}' countries.csv
echo 'England'
awk -F'\t' '{NumberCountry+=gsub(/England/,"England")} END {print NumberCountry}' countries.csv
echo 'United States'
awk -F'\t' '{NumberCountry+=gsub(/United States/,"United States")} END {print NumberCountry}' countries.csv
echo 'Spain'
awk -F'\t' '{NumberCountry+=gsub(/Spain/,"Spain")} END {print NumberCountry} countries.csv
echo 'How many people, on average, have visited the places in each country?'
awk -F '\t' '{print $4 $9}' AO_Data.csv > visited.csv
echo 'Italy'
grep 'Italy' visited.csv | awk '{ totalvisitedvisited += $1 } END { print int (totalvisited/NR) }'
echo 'France'
grep 'France' visited.csv | awk '{ totalvisited += $1 } END { print int (totalvisited/NR) }'
echo 'England'
grep 'England' visited.csv | awk '{ totalvisited += $1 } END { print int (totalvisited/NR) }'
echo 'United States'
grep 'United States' visited.csv | awk '{ totalvisited += $1 } END { print int (totalvisited/NR)' }
echo 'Spain'
grep 'Spain' visited.csv | awk '{ totalvisited += $1 } END { print int (totalvisited/NR) }'
echo 'How many people in totalvisited want to visit the places in each country?'
awk -F '\t' '{print $5 $9}' AO_Data.csv > wanttovisit.csv
echo 'Italy'
grep 'Italy' wanttovisit.csv | awk -F '\t' '{totalwanttovisit+=$1} END {print totalwanttovisit}'
echo 'France'
grep 'France' wanttovisit.csv | awk -F '\t' '{totalwanttovisit+=$1} END {print totalwanttovisit}'
echo 'England'
grep 'England' wanttovisit.csv | awk -F '\t' '{totalwanttovisit+=$1} END {print totalwanttovisit}'
echo 'United States'
grep 'United States' wanttovisit.csv | awk -F '\t' '{totalwanttovisit+=$1} END {print totalwanttovisit}'
echo 'Spain'
grep 'Spain' wanttovisit.csv | awk -F '\t' '{totalwanttovisit+=$1} END {print totalwanttovisit}'