#!/bin/bash

echo "使用 yapf 格式化代码..."
yapf -ir -p src

echo "使用 isort 格式化代码..."
isort src
