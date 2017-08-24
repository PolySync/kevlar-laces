#!/bin/bash

REQUESTING=$1

INDEX=`expr index "$REQUESTING" -`
TAG=${REQUESTING:0:INDEX-1}

FETCH_OUTPUT="$(git fetch)"
if [ $? != 0 ]; then
	echo "ERROR:"
	echo "$FETCH_OUTPUT"
	exit 1
fi

CHECKOUT_OUTPUT="$(git checkout master)"
if [ $? != 0 ]; then
	echo "ERROR:"
	echo "$CHECKOUT_OUTPUT"
	exit 1
fi

FF_MASTER_OUTPUT="$(git merge --ff-only origin/master)"
if [ $? != 0 ]; then
	echo "ERROR:"
	echo "$FF_MASTER_OUTPUT"
	exit 1
fi

MERGE_OUTPUT="$(git merge -S --no-ff origin/devel)"
if [ $? != 0 ]; then
	echo "ERROR:"
	echo "$MERGE_OUTPUT"
	exit 1
fi

TAG_OUTPUT="$(git tag -s $TAG -m $TAG)"
if [ $? != 0 ]; then
	echo "ERROR:"
	echo "$TAG_OUTPUT"
	exit 1
fi

PUSH_OUTPUT="$(git push origin master --tags)"
if [ $? != 0 ]; then
	echo "ERROR:"
	echo "TAG_OUTPUT"
	exit 1
fi

exit 0
