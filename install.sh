#!/bin/bash

print_usage(){
  echo "install kevlar-laces"
  echo ""
  echo "USAGE: ./install.sh [--dev]"
  echo ""
  echo "Pass the '--dev' flag in order to keep the secure-git scripts"
  echo "in this directory and create symlinks to them in '~/.local/bin/'."
  echo "By default this script will copy the scripts to this destination."
  echo "Use this option if you plan to customize or alter these commands."
}

DEV_FLAG=off
while [ $# -ne 0 ]
do
  case "$1" in
    -h | -help )
      print_usage
      exit 0
      ;;
    --dev )
      DEV_FLAG=on
      shift
      ;;
    * )
      echo "ERROR: unable to parse options."
      print_usage
      exit -1
      ;;
  esac
done

DEST_DIR=$HOME/.local/bin
echo "Ensuring $DEST_DIR exists"
mkdir -p $DEST_DIR

if [ $DEV_FLAG = on ]; then
  CMD='ln -sf'
  MESSAGE="Creating symlink for"
else
  CMD='cp'
  MESSAGE="Copying subcommand"
fi

for subcommand in `ls git-*`
do
  echo "$MESSAGE $subcommand"
  eval "$CMD `pwd`/$subcommand $DEST_DIR"
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

echo "Installation successful. To learn about usage of this tool, run any of
the subcommands with the '-h' flag, e.g. 'git merge-pr -h'.

For even more information, please consult the README."
