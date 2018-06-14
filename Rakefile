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


desc "Install zsh configurations"
task :zsh do
  install_dir = get_install_dir
  install_file("zshrc.zsh", File.join(install_dir, ".zshrc"))

  dotfiles = File.join(install_dir, ".dotfiles")
  if not Dir.exist? dotfiles
    Dir.mkdir(dotfiles, 0755)
  end
  Dir.foreach("scripts") do | item |
    if item == "." or item == ".."
      next
    end
    install_file(File.join("scripts", item), File.join(dotfiles, item))
  end
end


desc "Install tmux.conf"
task :tmux do
  install_dir = get_install_dir
  install_file("tmux.conf", File.join(install_dir, ".tmux.conf"))
end
