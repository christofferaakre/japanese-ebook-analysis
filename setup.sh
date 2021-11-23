#!/usr/bin/env bash
sudo apt install mecab mecab-ipadic libmecab-dev
sudo apt install mecab-ipadic-utf8

sudo apt install git curl
git clone https://github.com/neologd/mecab-ipadic-neologd.git
cd mecab-ipadic-neologd
sudo ./bin/install-mecab-ipadic-neologd -n -p /usr/lib/mecab/dic/mecab-ipadic-neologd
