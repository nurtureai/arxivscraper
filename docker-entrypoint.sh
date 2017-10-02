#!/bin/sh
set -e

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

python --version
echo $1 "$2" "$3" "$4"
if [ $1 = "run" ]; then
  python3 bin/scraper.py $2 $3 $4
elif [ $1 = "sh" ]; then
  echo "Shell..."
  /bin/sh
elif [ $1 = "serve" ]; then
  gunicorn -c gunicorn.ini.py serve:app
else
  echo "nothing todo"
  exit 1
fi

# exec gosu /usr/sbin/sshd -D &
# while true; do sleep 1000; done

set +e
