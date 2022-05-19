How to install a different version of ruby than the one you've got… 
	Ø rbenv install x.x.x 

How to see a list of all the ruby versions you can install 
	Ø rbenv install --list

How to CHANGE the global version of ruby 
	Ø rbenv global x.x.x 

https://superuser.com/questions/340490/how-to-install-and-use-different-versions-of-ruby
https://github.com/rbenv/rbenv#installation


How to set-up rbenv 
	Ø export PATH="~/.rbenv/shims:$PATH"




Steps I took to get this all running 

	Ø Sudo apt install ruby-build
	Ø Echo "$(rbenv init - bash)" >> ~/.bashrc
	Ø Rbenv install --list
	Ø Sudo rbenv install 2.6.10
	Ø Rbenv global 2.6.10
	Ø Sudo gem install bundler:1.17.3
	Ø Sudo gem install nokogiri -v '1.10.9' --source 'https://rubygems.org/'
Sudo apt install ruby-dev![image](https://user-images.githubusercontent.com/25730423/169194972-0f76df17-5975-4791-8cdc-3e6378a390e7.png)
