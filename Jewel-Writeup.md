



# Code I used to create my payload
Main Resource - https://github.com/masahiro331/CVE-2020-8165

## Steps I took to get this all running 

- sudo apt install ruby-build
- echo "$(rbenv init - bash)" >> ~/.bashrc
- rbenv install --list
- sudo rbenv install 2.6.10
- rbenv global 2.6.10
- sudo gem install bundler:1.17.3
- sudo gem install nokogiri -v '1.10.9' --source 'https://rubygems.org/'
- sudo apt install ruby-dev


## How to install a different version of ruby than the one you've got… 
- rbenv install x.x.x 

## How to see a list of all the ruby versions you can install 
- rbenv install --list

## How to CHANGE the global version of ruby 
- rbenv global x.x.x 

## More Resources
https://superuser.com/questions/340490/how-to-install-and-use-different-versions-of-ruby
https://github.com/rbenv/rbenv#installation
