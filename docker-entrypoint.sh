#!/bin/sh


if [ "$SSH_KEY" ]; then
  echo "$SSH_KEY
      " > /home/app/.ssh/authorized_keys
  if [ "$SSH_KEY2" ]; then
      echo "$SSH_KEY2
      " >> /home/app/.ssh/authorized_keys
  fi
  if [ "$SSH_KEY3" ]; then
      echo "$SSH_KEY3
      " >> /home/app/.ssh/authorized_keys
  fi
  if [ "$SSH_KEY4" ]; then
      echo "$SSH_KEY4
      " >> /home/app/.ssh/authorized_keys
  fi
  if [ "$SSH_KEY5" ]; then
      echo "$SSH_KEY5
      " >> /home/app/.ssh/authorized_keys
  fi
fi

python scrapper.py

# exec gosu /usr/sbin/sshd -D &
# while true; do sleep 1000; done
