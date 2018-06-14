def get_install_dir()
  install_dir = Dir.home
  if ENV.has_key? "DOTFILES_DEBUG"
    install_dir = File.join(Dir.getwd, "test")
  end
  return install_dir
end


def overwrite?(destination)
  overwrite = "y"
  if File.exist? destination
    puts "#{destination} already exists"
    print "Overwrite #{File.basename(destination)}? (y/n) [n] "
    overwrite = STDIN.gets.chomp
  end
  return overwrite
end


def install_file(source, destination)
  overwrite = overwrite? destination
  if overwrite.downcase == "y"
    FileUtils.copy_entry(source, destination, :preserve=>true, :remove_destination=>true)
  else
    puts "Skipped installation of #{source}"
  end
end
