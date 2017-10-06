#!/bin/bash

DEST_DIR=$HOME/.local/bin
echo "Ensuring $DEST_DIR exists"
mkdir -p $DEST_DIR

for subcommand in `ls git-*`
do
  echo "Creating symlink for $subcommand"
  ln -sf `pwd`/$subcommand $DEST_DIR
done

output=$(echo $PATH | grep -F $DEST_DIR)

if [ $? != 0 ]
then
  echo "Could not find $DEST_DIR in PATH. Adding to ~/.bashrc"
  echo ""
  echo "export PATH=\$PATH:$DEST_DIR"
  echo "export PATH=\$PATH:$DEST_DIR" >> $HOME/.bashrc
  eval "export PATH=$PATH:$DEST_DIR"
fi

if [ "$1" != --no-override ]
then
echo "Overriding existing git push, pull, and fetch commands to use secure versions"
echo "
# override existing git push, pull, fetch to use secure versions
kevlar_git () {
  prefix=\"\"
  cmd=\$1
  shift
  if [ \"\$cmd\" == \"push\" ] || [ \"\$cmd\" == \"pull\" ] || [ \"\$cmd\" == \"fetch\" ]; then
    prefix=\"secure-\"
  fi
  \"\`which git\`\" \"\$prefix\$cmd\" \"\$@\"
}
alias git='kevlar_git'" >> $HOME/.bashrc

  if [ $? != 0 ]
  then
    echo "Could not write git command overrides to ~/.bashrc"
    echo "git fetch, pull, and push will not automatically use secure versions"
  fi
fi

source $HOME/.bashrc

echo "Installation successful. To learn about usage of this tool, run any of
the subcommands with the '-h' flag, e.g. 'git merge-pr -h'.

For even more information, please consult the README."
