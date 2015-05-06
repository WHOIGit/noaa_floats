Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provider "virtualbox" do |vb|
    vb.memory="1024"
  end
  config.vm.network :forwarded_port, host: 8080, guest: 8080
  config.vm.network :forwarded_port, host: 5433, guest: 5432
  config.vm.provision :shell, inline: <<-SHELL
sudo apt-get update
# python numpy/scipy/pandas and flask/sqlalchemy
sudo apt-get install -y python-pandas python-flask python-sqlalchemy python-pip
# postgres 9.3
sudo apt-get install -y postgresql-9.3 postgresql-contrib-9.3 python-psycopg2
sudo -u postgres createuser floats
sudo -u postgres createdb -O floats floats
sudo -u postgres psql -c "ALTER USER floats WITH ENCRYPTED PASSWORD 'floats';"
sudo sed -i /etc/postgresql/9.3/main/postgresql.conf -e 's/^#listen_addresses/listen_addresses/'
# postgis
sudo apt-get install -y postgis postgresql-9.3-postgis-2.1
sudo -u postgres psql -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;" floats
# restart postgres
sudo service postgresql restart
# geoalchemy2
sudo pip install geoalchemy2
SHELL
end
