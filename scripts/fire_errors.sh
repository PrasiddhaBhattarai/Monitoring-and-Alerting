# Hammer the app homepage to probabilistically trigger errors (HTTP 500).

URL1="http://localhost:5050"
URL2="http://localhost:5051"
COUNT=${1:-100}

echo "Hitting ${URL1}, ${URL2} ${COUNT} times…"
for i in $(seq 1 $COUNT); do
  code1=$(curl -s -o /dev/null -w "%{http_code}" "$URL1")
  echo "[$(date '+%H:%M:%S')] #${i}_web -> HTTP $code1"
  code2=$(curl -s -o /dev/null -w "%{http_code}" "$URL2")
  echo "[$(date '+%H:%M:%S')] #${i}_api -> HTTP $code2"
  sleep 0.3
done