# Overwrite the destination if prompted
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
def install_file(source, destination)
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
  os_type = %x{uname -s}.strip()
  if os_type == "Darwin"
    # Install the xterm-24bit.terminfo for Emacs (terminal)
    %{/usr/bin/tic -x -o ${HOME}/.terminfo term/xterm-24bit.terminfo}
  end

  # Install zsh configuration files
  # /etc/zshenv
  # ~/.zshenv
  install_file("zshenv.zsh", File.join(Dir.home, ".zshenv"))
  # /etc/zprofile
  # ~/.zprofile
  install_file("zprofile.zsh", File.join(Dir.home, ".zprofile"))
  # /etc/zshrc
  # ~/.zshrc
  install_file("zshrc.zsh", File.join(Dir.home, ".zshrc"))

  # Install project-related file
  install_file("projects.zsh", File.join(Dir.home, ".projects.zsh"))

  # Install secrets file
  install_file("secrets.zsh", File.join(Dir.home, ".secrets.zsh"))

  # Install tmux configuration
  install_file("tmux.conf", File.join(Dir.home, ".tmux.conf"))

  # Install Emacs and Vim configurations
  install_file("spacemacs", File.join(Dir.home, ".spacemacs"))
  install_file("vimrc", File.join(Dir.home, ".vimrc"))
end


desc "Install Hammerspoon configurations"
task :hammerspoon do
  hammerspoon = File.join(Dir.home, ".hammerspoon")
  if not Dir.exist? hammerspoon
    Dir.mkdir(hammerspoon, 0755)
  end
  install_file(File.join("hammerspoon", "init.lua"), File.join(hammerspoon, "init.lua"))
end


desc "Install gitconfig"
task :git do
  if install_file("gitconfig", File.join(Dir.home, ".gitconfig"))
    print "What is your GitHub/GitLab name? "
    git_name = STDIN.gets.chomp
    print "What is your GitHub/GitLab email? "
    git_email = STDIN.gets.chomp

    %x{sed -i -E "s/GIT_USERNAME/#{git_name}/" #{File.join(Dir.home, ".gitconfig")}}
    %x{sed -i -E "s/GIT_EMAILADDR/#{git_email}/" #{File.join(Dir.home, ".gitconfig")}}

    os_type = %x{uname -s}.strip()
    if os_type == "Darwin"
      # Configure macOS specific Git configurations
      %x{echo >> #{File.join(Dir.home, ".gitconfig")}}

      %x{git config --global diff.tool Kaleidoscope}
      %x{echo >> #{File.join(Dir.home, ".gitconfig")}}

      %x{git config --global difftool.prompt "false"}
      %x{echo >> #{File.join(Dir.home, ".gitconfig")}}

      %x{git config --global difftool.Kaleidoscope.cmd 'ksdiff --partial-changeset --relative-path \"$MERGED\" -- \"$LOCAL\" \"$REMOTE\"'}
      %x{echo >> #{File.join(Dir.home, ".gitconfig")}}

      %x{git config --global merge.tool Kaleidoscope}
      %x{echo >> #{File.join(Dir.home, ".gitconfig")}}

      %x{git config --global mergetool.prompt "false"}
      %x{echo >> #{File.join(Dir.home, ".gitconfig")}}

      %x{git config --global mergetool.Kaleidoscope.cmd 'ksdiff --merge --output \"$MERGED\" --base \"$BASE\" -- \"$LOCAL\" --snapshot \"$REMOTE\" --snapshot'}
      %x{git config --global mergetool.Kaleidoscope.trustExitCode "true"}
      %x{echo >> #{File.join(Dir.home, ".gitconfig")}}

      %x{git config --global credential.helper "osxkeychain"}
      %x{echo >> #{File.join(Dir.home, ".gitconfig")}}
    end

    # Configure ghq
    %x{git config --global ghq.root ${HOME}/Projects/src}
  end
end


desc "Install peco-related configurations"
task :peco do
  install_file("peco", File.join(Dir.home, ".peco"))
end
