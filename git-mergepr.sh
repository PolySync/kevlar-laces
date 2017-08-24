#!/bin/bash

PRUNE_FLAG=off
REQUESTING=""
DESTINATION=""

if [ "$1" = "--no-prune" ]; then
	PRUNE_FLAG=on
	REQUESTING="$2"
	DESTINATION="$3"
else
	REQUESTING="$1"
	DESTINATION="$2"
fi

CURRENT_BRANCH="$(git symbolic-ref --short HEAD)"

STASH_OUTPUT="$(git stash push)"
if [ $? != 0 ]; then
	echo "ERROR:"
	echo "$STASH_OUTPUT"
	exit 1
fi

FETCH_OUTPUT="$(git fetch --prune)"
if [ $? != 0 ]; then
	echo "ERROR:"
	echo "$FETCH_OUTPUT"
	exit 1
fi

CHECKOUT_OUTPUT="$(git checkout $DESTINATION)"
if [ $? != 0 ]; then
	echo "ERROR:"
	echo "$CHECKOUT_OUTPUT"
	exit 1
fi

MERGE_OUTPUT="$(git merge -S --verify-signatures --no-ff origin/$REQUESTING)"
if [ $? != 0 ]; then
	echo "ERROR:"
	echo "$MERGE_OUTPUT"
	exit 1
fi

PUSH_OUTPUT="$(git push origin/$DESTINATION)"
if [ $? != 0 ]; then
	echo "ERROR:"
	echo "$PUSH_OUTPUT"
	exit 1
fi

if [ "$PRUNE_FLAG" = off ]; then
	PUSH_EMPTY_BRANCH="$(git push origin :$REQUESTING)"
	if [ $? != 0 ]; then
		echo "ERROR:"
		echo "$PUSH_EMPTY_BRANCH"
		exit 1
	fi
fi

CHECKOUT_ORIGINAL_OUTPUT="$(git checkout $CURRENT_BRANCH)"
if [ $? != 0 ]; then
	echo "ERROR:"
	echo "$CHECKOUT_ORIGINAL_OUTPUT"
	exit 1
fi

if [ "$STASH_OUTPUT" != "No local changes to save" ]; then
	POP_STASH="$(git stash pop)"
	if [ $? != 0 ]; then
		echo "ERROR:"
		echo "$POP_STASH"
		exit 1
	fi
fi

exit 0