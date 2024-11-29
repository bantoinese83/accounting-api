#!/bin/bash

start_zookeeper() {
  echo "Starting Zookeeper..."
  if pgrep -f "zookeeper" > /dev/null; then
    echo "Zookeeper is already running."
  else
    zookeeper-server-start /opt/homebrew/etc/kafka/zookeeper.properties &
    sleep 5
    if pgrep -f "zookeeper" > /dev/null; then
      echo "Zookeeper started successfully."
    else
      echo "Failed to start Zookeeper."
      exit 1
    fi
  fi
}

start_kafka() {
  echo "Starting Kafka..."
  if pgrep -f "kafka" > /dev/null; then
    echo "Kafka is already running."
  else
    kafka-server-start /opt/homebrew/etc/kafka/server.properties &
    sleep 5
    if pgrep -f "kafka" > /dev/null; then
      echo "Kafka started successfully."
    else
      echo "Failed to start Kafka."
      exit 1
    fi
  fi
}

start_zookeeper
start_kafka

echo "Kafka and Zookeeper services have been started."