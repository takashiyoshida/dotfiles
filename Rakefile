# Overwrite the destination if ppprompted
def overwrite?(destination)
  overwrite = "y"
  if File.exist? destination
    puts "#{destination} already exists"
    print "Overwrite #{File.basename(destination)}? (y/N) [N] "
    overwrite = STDIN.gets.chomp
  end
  return overwrite
end

# Install the source to the destination
def install(source, destination)
  overwrite = overwrite? destination
  if overwrite.downcase == "y"
    FileUtils.copy_entry(source, destination, :preserve=>true, :remove_destination=>true)
    return true
  else
    puts "Skipped installation of #{File.basename(source)}"
    return false
  end
end


desc "Install shell configurations"
task :shell do
  # Install the xterm-24bit.terminfo for Emacs (terminal)
  %{/usr/bin/tic -x -o ${HOME}/.terminfo term/xterm-24bit.terminfo}

  # Install zsh configuration files
  # /etc/zshenv
  # ~/.zshenv
  install("zshenv.zsh", File.join(Dir.home, ".zshenv"))
  # /etc/zprofile
  # ~/.zprofile
  install("zprofile.zsh", File.join(Dir.home, ".zprofile"))
  # /etc/zshrc
  # ~/.zshrc
  install("zshrc.zsh", File.join(Dir.home, ".zshrc"))

  # Install project-related file
  install("projects.zsh", File.join(Dir.home, ".projects.zsh"))

  # Install tmux configuration
  install("tmux.conf", File.join(Dir.home, ".tmux.conf"))

  # Install Emacs and Vim configurations
  install("spacemacs", File.join(Dir.home, ".spacemacs"))
  install("vimrc", File.join(Dir.home, ".vimrc"))
end


desc "Install Hammerspoon configurations"
task :hammerspoon do
  hammerspoon = File.join(Dir.home, ".hammerspoon")
  if not Dir.exist? hammerspoon
    Dir.mkdir(hammerspoon, 0755)
  end
  install(File.join("hammerspoon", "init.lua"), File.join(hammerspoon, "init.lua"))
end


desc "Install gitconfig"
task :git do
  if install("gitconfig", File.join(Dir.home, ".gitconfig"))
    print "What is your GitHub/GitLab name? "
    git_name = STDIN.gets.chomp
    print "What is your GitHub/GitLab email? "
    git_email = STDIN.gets.chomp

    %x{sed -e "s/GIT_USERNAME/#{git_name}/g" -i '' #{File.join(install_dir, ".gitconfig")}}
    %x{sed -e "s/GIT_EMAILADDR/#{git_email}/g" -i '' #{File.join(install_dir, ".gitconfig")}}
  end
end


desc "Install peco-related configurations"
task :peco do
  install("peco", File.join(Dir.home, ".peco"))
end
