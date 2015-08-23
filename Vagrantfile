Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision :shell, path: "bootstrap.sh"

  config.vm.network :forwarded_port, guest: 5000, host: 5000, auto_correct: false
end
