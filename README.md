# OtoMoToOgloszenia
Skrytp na szukanie ogłoszen na otomoto

Aby skrypt sie wykonywal trzeba dodac do crona polecenie

sudo crontam - e

# Run otomotomegane python script every 5 minutes
*/5 * * * * python3 /home/pi/otomotomegane.py >> /home/pi/log/otomotomegane.log 2>&1


2015-06-10
Trzeba przerobic szukanie bo zmieniala sie strona na Otomoto
