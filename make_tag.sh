#!/bin/bash
echo
echo "这个脚本将帮助你添加一个新的tag"
echo "如果是master分支添加的tag，阿里云会自动构建镜像"
echo
echo
echo "正在获取Remote git上最近的5个Tag ..."
git ls-remote --tags| awk '{print $2}' | sort --version-sort | tail -n 5

read -p "添加一个最新的tag: v" git_tag

git tag release-v$git_tag || exit
git push origin release-v$git_tag

echo "Tag release-v$git_tag 已经同步到Remote"