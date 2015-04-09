Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provider "virtualbox" do |vb|
    vb.memory="512"
  end
  config.vm.network :forwarded_port, host: 8080, guest: 8080
  config.vm.provision :shell, inline: <<-SHELL
sudo apt-get update
sudo apt-get install -y emacs24-nox python-pandas python-flask
SHELL
end
