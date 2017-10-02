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

echo "Installation successfull. To learn about usage of this tool, run any of
the subcommands with the '-h' flag, e.g. 'git merge-pr -h'.

For even more information, please consult the README."
