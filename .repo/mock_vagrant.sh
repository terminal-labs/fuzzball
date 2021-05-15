useradd -m vagrant
mkdir -p /home/vagrant
touch /home/vagrant/.bashrc

mkdir -p /vagrant
cp -a . /vagrant/
chmod 777 -R /vagrant
chown -R vagrant /vagrant

usermod -aG sudo vagrant
