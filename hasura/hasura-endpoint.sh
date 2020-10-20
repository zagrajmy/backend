if [[ $endpoint = "" ]]; then
  if [[ $env = "production" ]]; then
    endpoint="https://db.wiezamaga.net"
  elif [[ $env = "beta" ]]; then
    endpoint="https://db.beta.wiezamaga.net"
  elif [[ $env = "local" ]]; then
    endpoint="http://localhost:8081"
  else
    echo "env='$env'"
    echo "not implemented"
    exit 1
  fi
fi
